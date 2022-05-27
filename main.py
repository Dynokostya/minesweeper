import configparser
import os
import random
import tkinter
import tkinter.messagebox
import tkinter.simpledialog
import pandas as pd


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mine Sweeper")
        self.rows = 10
        self.cols = 10
        self.mines = 10
        self.field = []
        self.buttons = []
        self.colors = ['#fc8383', '#6161c2', '#79c9a8', '#f285eb', '#000084', '#840000', '#008284', '#840084',
                       '#000000']
        self.game_over = False
        self.custom_sizes = []

        self.log_window = User()
        self.result_window = ResultWindow()
        self.global_result_window = GlobalResults()
        self.score = None

        self.create_menu()
        self.prepare_window()

    def create_menu(self):
        menu_bar = tkinter.Menu(self)
        menu_size = tkinter.Menu(self, tearoff=0)
        user = tkinter.Menu(self, tearoff=0)

        menu_bar.add_cascade(label="User", menu=user)
        user.add_command(label="Login", command=lambda: self.user_login())
        user.add_command(label="Save Game", command=lambda: self.save_game())
        user.add_command(label="Find results", command=lambda: self.show_results())
        user.add_command(label="Show global results", command=lambda: self.show_global())
        user.add_command(label="Exit", command=lambda: self.exit_app())

        menu_bar.add_cascade(label="Size", menu=menu_size)
        menu_size.add_command(label="Easy (9x9 with 10 mines)", command=lambda: self.set_size(9, 9, 10))
        menu_size.add_command(label="Normal (16x16 with 40 mines)", command=lambda: self.set_size(16, 16, 40))
        menu_size.add_command(label="Hard (16x30 with 90 mines)", command=lambda: self.set_size(16, 30, 90))
        menu_size.add_command(label="Custom", command=self.set_custom_size)

        custom_sizes = self.custom_sizes
        menu_size.add_separator()
        for x in range(len(custom_sizes)):
            menu_size.add_command(
                label=str(custom_sizes[x][0]) + "x" + str(custom_sizes[x][1]) + " with " + str(
                    custom_sizes[x][2]) + "mines",
                command=lambda customsizes=custom_sizes: self.set_size(customsizes[x][0], customsizes[x][1],
                                                                       customsizes[x][2]))

        self.config(menu=menu_bar)
        self.custom_sizes = custom_sizes

    def exit_app(self):
        msgbox = tkinter.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application?',
                                                icon='warning')
        if msgbox == 'yes':
            self.destroy()
            quit()
        else:
            return 0

    def prepare_window(self):
        tkinter.Button(self, text="Restart", command=self.restart_game).grid(row=0, column=0, columnspan=self.cols,
                                                                             sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.buttons = []
        for x in range(self.rows):
            self.buttons.append([])
            for y in range(self.cols):
                b = tkinter.Button(self, text=" ", width=2, command=lambda x=x, y=y: self.click_on(x, y))
                b.bind("<Button-3>", lambda e, x=x, y=y: self.on_right_click(x, y))
                b.grid(row=x + 1, column=y, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
                self.buttons[x].append(b)

    def prepare_game(self):
        field = []
        for x in range(self.rows):
            field.append([])
            for y in range(self.cols):
                # add button and init value for game
                field[x].append(0)
        for _ in range(self.mines):
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            # prevent spawning mine on top of each other
            while field[x][y] == -1:
                x = random.randint(0, self.rows - 1)
                y = random.randint(0, self.cols - 1)
            field[x][y] = -1
            if x != 0:
                if y != 0:
                    if field[x - 1][y - 1] != -1:
                        field[x - 1][y - 1] = int(field[x - 1][y - 1]) + 1
                if field[x - 1][y] != -1:
                    field[x - 1][y] = int(field[x - 1][y]) + 1
                if y != (self.cols - 1):
                    if field[x - 1][y + 1] != -1:
                        field[x - 1][y + 1] = int(field[x - 1][y + 1]) + 1
            if y != 0:
                if field[x][y - 1] != -1:
                    field[x][y - 1] = int(field[x][y - 1]) + 1
            if y != (self.cols - 1):
                if field[x][y + 1] != -1:
                    field[x][y + 1] = int(field[x][y + 1]) + 1
            if x != (self.rows - 1):
                if y != 0:
                    if field[x + 1][y - 1] != -1:
                        field[x + 1][y - 1] = int(field[x + 1][y - 1]) + 1
                if field[x + 1][y] != -1:
                    field[x + 1][y] = int(field[x + 1][y]) + 1
                if y != (self.cols - 1):
                    if field[x + 1][y + 1] != -1:
                        field[x + 1][y + 1] = int(field[x + 1][y + 1]) + 1
        self.field = field

    def restart_game(self):
        self.game_over = False
        # destroy all - prevent memory leak
        for x in self.winfo_children():
            if type(x) != tkinter.Menu:
                x.destroy()
        self.prepare_window()
        self.prepare_game()

    def set_custom_size(self):
        r = tkinter.simpledialog.askinteger("Custom size", "Enter amount of rows")
        c = tkinter.simpledialog.askinteger("Custom size", "Enter amount of columns")
        m = tkinter.simpledialog.askinteger("Custom size", "Enter amount of mines")
        while m > r * c:
            m = tkinter.simpledialog.askinteger("Custom size", "Maximum mines for this dimension is: " + str(
                r * c) + "\nEnter amount of mines")
        self.custom_sizes.insert(0, (r, c, m))
        self.custom_sizes = self.custom_sizes[0:5]
        self.set_size(r, c, m)
        self.create_menu()

    def set_size(self, r, c, m):
        self.rows = r
        self.cols = c
        self.mines = m
        self.restart_game()

    def click_on(self, x, y):
        if len(self.field) == 0:
            self.prepare_game()
        if self.game_over:
            return
        self.buttons[x][y]["text"] = str(self.field[x][y])
        if self.field[x][y] == -1:
            self.buttons[x][y]["text"] = "*"
            self.buttons[x][y].config(background='red', disabledforeground='black')
            self.game_over = True
            tkinter.messagebox.showinfo("Game Over", "You have lost.")
            # now show all other mines
            for _x in range(self.rows):
                for _y in range(self.cols):
                    if self.field[_x][_y] == -1:
                        self.buttons[_x][_y]["text"] = "*"
        else:
            self.buttons[x][y].config(disabledforeground=self.colors[self.field[x][y]])
        if self.field[x][y] == 0:
            self.buttons[x][y]["text"] = " "
            # now repeat for all buttons nearby which are 0...
            self.auto_click_on(x, y)
        self.buttons[x][y]['state'] = 'disabled'
        self.buttons[x][y].config(relief=tkinter.SUNKEN)
        self.check_win()

    def auto_click_on(self, x, y):
        if self.buttons[x][y]["state"] == "disabled":
            return 0
        if self.field[x][y] != 0:
            self.buttons[x][y]["text"] = str(self.field[x][y])
        else:
            self.buttons[x][y]["text"] = " "
        self.buttons[x][y].config(disabledforeground=self.colors[self.field[x][y]])
        self.buttons[x][y].config(relief=tkinter.SUNKEN)
        self.buttons[x][y]['state'] = 'disabled'
        if self.field[x][y] == 0:
            if x != 0 and y != 0:
                self.auto_click_on(x - 1, y - 1)
            if x != 0:
                self.auto_click_on(x - 1, y)
            if x != 0 and y != (self.cols - 1):
                self.auto_click_on(x - 1, y + 1)
            if y != 0:
                self.auto_click_on(x, y - 1)
            if y != (self.cols - 1):
                self.auto_click_on(x, y + 1)
            if x != (self.rows - 1) and y != 0:
                self.auto_click_on(x + 1, y - 1)
            if x != (self.rows - 1):
                self.auto_click_on(x + 1, y)
            if x != (self.rows - 1) and y != (self.cols - 1):
                self.auto_click_on(x + 1, y + 1)

    def on_right_click(self, x, y):
        if self.game_over:
            return
        if self.buttons[x][y]["text"] == "?":
            self.buttons[x][y]["text"] = " "
            self.buttons[x][y]["state"] = "normal"
        elif self.buttons[x][y]["text"] == " " and self.buttons[x][y]["state"] == "normal":
            self.buttons[x][y]["text"] = "?"
            self.buttons[x][y]["state"] = "disabled"

    def check_win(self):
        win = True
        for x in range(self.rows):
            for y in range(self.cols):
                if self.field[x][y] != -1 and self.buttons[x][y]["state"] == "normal":
                    win = False

        if win and (self.log_window.user_name is None):
            tkinter.messagebox.showinfo("Game Over", "You have won.")

        elif win and (self.log_window.user_name is not None):
            dec = tkinter.messagebox.askquestion("Game Over", "You have won. Do you want to save your score?")
            if dec == "yes":
                self.score = self.log_window.user_score
                self.score += self.rows * self.cols * self.mines * 0.02
                idx = self.log_window.data.index[self.log_window.data['login'] == self.log_window.user_name].tolist()[0]
                self.log_window.data.loc[idx, "score"] = self.score
                self.log_window.data.loc[idx, "games_won"] += 1
                res = "Custom"
                if self.rows < 9 and self.cols < 9:
                    res = "Easy"
                elif self.rows < 16 and self.cols < 16:
                    res = "Normal"
                elif self.rows < 16 and self.cols < 30:
                    res = "Hard"

                games_won = int(self.log_window.data.loc[idx, "games_won"])
                if games_won > 10:
                    for i in range(1, 10):
                        self.log_window.data.loc[idx, str(i)] = self.log_window.data.loc[idx, str(i + 1)]
                    self.log_window.data.loc[idx, '10'] = res
                else:
                    self.log_window.data.loc[idx, str(games_won)] = res

                self.log_window.data.to_csv("users.csv", index=False)

    def user_login(self):
        self.log_window.user_login.delete(0, 'end')
        self.log_window.user_password.delete(0, 'end')
        self.log_window.deiconify()

    def load_game(self, user_name):
        # global rows, cols, mines, custom_sizes
        config = configparser.ConfigParser()
        file_name = "config_" + user_name + ".ini"
        config.read(file_name)
        self.rows = config.getint("game", "rows")
        self.cols = config.getint("game", "cols")
        self.mines = config.getint("game", "mines")
        field_temp = config.get("data", "field").split()
        buttons_text_temp = config.get("data", "buttons_text").split()
        buttons_state_temp = config.get("data", "buttons_state").split()
        self.field = []
        for i in range(self.rows):
            self.field.append([])
            for j in range(self.cols):
                self.field[i].append(0)

        self.game_over = False
        # destroy all - prevent memory leak
        for x in self.winfo_children():
            if type(x) != tkinter.Menu:
                x.destroy()

        tkinter.Button(self, text="Restart", command=self.restart_game).grid(row=0, column=0, columnspan=self.cols,
                                                   sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.buttons = []
        for x in range(self.rows):
            self.buttons.append([])
            for y in range(self.cols):
                b = tkinter.Button(self, text=" ", width=2, command=lambda x=x, y=y: self.click_on(x, y))
                b.bind("<Button-3>", lambda e, x=x, y=y: self.on_right_click(x, y))
                b.grid(row=x + 1, column=y, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
                self.buttons[x].append(b)

        x = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.field[i][j] = int(field_temp[x], 2) - 50
                self.buttons[i][j]['text'] = int(buttons_text_temp[x])
                self.buttons[i][j]['state'] = buttons_state_temp[x]
                x += 1

        for x in range(self.rows):
            for y in range(self.cols):
                self.buttons[x][y].config(background='SystemButtonFace')
                if self.buttons[x][y]['text'] == 0:
                    self.buttons[x][y]['text'] = " "
                if self.buttons[x][y]["state"] == "disabled":
                    if self.field[x][y] == 0:
                        self.buttons[x][y]['text'] = " "
                    else:
                        self.buttons[x][y]["text"] = str(self.field[x][y])
                    self.buttons[x][y].config(disabledforeground=self.colors[self.field[x][y]])
                    self.buttons[x][y].config(relief=tkinter.SUNKEN)
            # if self.buttons[x][y]['state'] == 'disabled':
            #     self.buttons[x][y].config(disabledforeground=self.colors[self.field[x][y]])
            #     self.buttons[x][y].config(relief=tkinter.SUNKEN)
            # self.buttons[x][y].config(relief=tkinter.SUNKEN)
        # amount_of_sizes = config.getint("sizes", "amount")
        # for x in range(amount_of_sizes):
        #     self.custom_sizes.append((config.getint("sizes", "row" + str(x)), config.getint("sizes", "cols" + str(x)),
        #                               config.getint("sizes", "mines" + str(x))))

    def save_game(self):
        if self.game_over:
            tkinter.messagebox.showinfo("Error!", "You cannot save this game!")
            return 0
        user_name = self.log_window.user_name
        if user_name is None:
            tkinter.messagebox.showinfo("Error!", "You haven't authorized!")
            return 0
        if len(self.field) == 0:
            tkinter.messagebox.showinfo("Error!", "You haven't started the game!")
            return 0

        # global rows, cols, mines
        # configuration
        config = configparser.ConfigParser()
        config.add_section("game")
        config.set("game", "rows", str(self.rows))
        config.set("game", "cols", str(self.cols))
        config.set("game", "mines", str(self.mines))
        # config.add_section("sizes")
        # config.set("sizes", "amount", str(min(5, len(self.custom_sizes))))
        # for x in range(min(5, len(self.custom_sizes))):
        #     config.set("sizes", "row" + str(x), str(self.custom_sizes[x][0]))
        #     config.set("sizes", "cols" + str(x), str(self.custom_sizes[x][1]))
        #     config.set("sizes", "mines" + str(x), str(self.custom_sizes[x][2]))
        config.add_section("data")
        config.set("data", "field", "")
        config.set("data", "buttons_text", "")
        config.set("data", "buttons_state", "")
        for i in range(self.rows):
            for j in range(self.cols):
                info = config.get("data", "field")
                config.set("data", "field", info + "{0:b} ".format(self.field[i][j] + 50))
                info = config.get("data", "buttons_text")

                dat = self.buttons[i][j]['text']
                if dat == ' ':
                    dat = '0'
                config.set("data", "buttons_text", info + dat + " ")

                info = config.get("data", "buttons_state")
                dat = self.buttons[i][j]['state']
                if dat == '':
                    dat = '0'
                config.set("data", "buttons_state", info + dat + " ")

        file_name = "config_" + user_name + ".ini"
        with open(file_name, "w") as file:
            config.write(file)
        file.close()
        idx = self.log_window.data.index[self.log_window.data['login'] == self.log_window.user_name].tolist()[0]
        self.log_window.data.loc[idx, 'last_save'] = file_name
        self.log_window.data.to_csv('users.csv', index=False)
        tkinter.messagebox.showinfo("Info", "Game has been saved!")

    def show_results(self):
        self.result_window.clear_all()
        self.result_window.deiconify()

    def show_global(self):
        self.global_result_window.show_global_results()
        self.global_result_window.deiconify()


class User(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.withdraw()
        self.geometry("350x150")

        # the label for user_name
        tkinter.Label(self, text="Login:").place(x=20, y=20)
        tkinter.Label(self, text="Password:").place(x=20, y=60)
        self.user_login = tkinter.Entry(self, width=30)
        self.user_login.place(x=100, y=20)
        self.user_password = tkinter.Entry(self, show="*", width=30)
        self.user_password.place(x=100, y=60)
        self.login_button = tkinter.Button(self, width=10, text="Login", command=self.user_check)
        self.login_button.place(x=235, y=100)
        self.close_button = tkinter.Button(self, width=10, text="Close", command=self.withdraw)
        self.close_button.place(x=100, y=100)

        self.data = pd.DataFrame(data=[], columns=["login",
                                                   "password",
                                                   "last_save",
                                                   "score",
                                                   "games_won",
                                                   '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.data = pd.read_csv("users.csv", index_col=False)
        self.user_name = None
        self.user_score = None
        self.current_user = None

    def user_check(self):
        user_log = self.user_login.get()
        user_password = self.user_password.get()
        if user_log == "" or user_password == "":
            tkinter.messagebox.showinfo("Error!", "You haven't typed something")
            return 0

        self.current_user = self.data[self.data["login"] == user_log]
        if self.current_user.empty:
            msgbox = tkinter.messagebox.askquestion("Info", "There is no user with this name\n"
                                                            "Do you want to register new?")
            if msgbox == "yes":
                new_user = pd.Series(data={"login": user_log,
                                           "password": user_password,
                                           "last_save": None,
                                           "score": 0,
                                           "games_won": 0})
                self.data = self.data.append(new_user, ignore_index=True)
                self.data.to_csv("users.csv")
                self.user_name = user_log
            else:
                self.withdraw()
        else:
            password = str(self.data[self.data["login"] == user_log]["password"].tolist()[0])
            self.user_score = self.data[self.data["login"] == user_log]["score"].tolist()[0]
            if user_password != password:
                tkinter.messagebox.showinfo("Error!", "Password is wrong!")
                return 0
            self.user_name = user_log
            if os.path.exists("config_" + self.user_name + ".ini"):
                dec = tkinter.messagebox.askquestion("Info", "You have logged successfully! Do you want to load last "
                                                             "save?")
                if dec == "yes":
                    app.load_game(self.user_name)
            else:
                tkinter.messagebox.showinfo("Info", "You have logged successfully!")
            self.withdraw()


class ResultWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.geometry("350x420")
        self.title("Last Results")

        # the label for user_name
        tkinter.Label(self, text="Login:").place(x=20, y=20)
        self.user_login = tkinter.Entry(self, width=30)
        self.user_login.place(x=100, y=20)
        self.find_button = tkinter.Button(self, width=10, text="Find", command=self.show_user_results)
        self.find_button.place(x=235, y=50)
        self.close_button = tkinter.Button(self, width=10, text="Close", command=self.withdraw)
        self.close_button.place(x=100, y=50)

        self.current_user = None

        self.label_name = tkinter.Label(self, text="")
        self.label_res_1 = tkinter.Label(self, text="")
        self.label_res_2 = tkinter.Label(self, text="")
        self.label_res_3 = tkinter.Label(self, text="")
        self.label_res_4 = tkinter.Label(self, text="")
        self.label_res_5 = tkinter.Label(self, text="")
        self.label_res_6 = tkinter.Label(self, text="")
        self.label_res_7 = tkinter.Label(self, text="")
        self.label_res_8 = tkinter.Label(self, text="")
        self.label_res_9 = tkinter.Label(self, text="")
        self.label_res_10 = tkinter.Label(self, text="")

        self.label_name.place(x=20, y=80)
        self.label_res_1.place(x=20, y=110)
        self.label_res_2.place(x=20, y=140)
        self.label_res_3.place(x=20, y=170)
        self.label_res_4.place(x=20, y=200)
        self.label_res_5.place(x=20, y=230)
        self.label_res_6.place(x=20, y=260)
        self.label_res_7.place(x=20, y=290)
        self.label_res_8.place(x=20, y=320)
        self.label_res_9.place(x=20, y=350)
        self.label_res_10.place(x=20, y=380)

    def show_user_results(self):
        for i in range(1, 11):
            getattr(self, "label_res_{:}".format(i))['text'] = ""
        user_name = self.user_login.get()
        self.current_user = app.log_window.data[app.log_window.data["login"] == user_name]
        if self.current_user.empty:
            tkinter.messagebox.showinfo("Error!", "There is no user with this name!")
            return 0

        self.label_name['text'] = "10 last wins of user \"" + user_name + "\":"
        idx = app.log_window.data.index[app.log_window.data['login'] == user_name].tolist()[0]
        games_won = int(app.log_window.data.loc[idx, "games_won"])
        if games_won > 10:
            j = 10
            for i in range(1, 11):
                getattr(self, "label_res_{:}".format(i))['text'] = app.log_window.data.loc[idx, str(j)]
                j -= 1
        else:
            for i in range(1, games_won + 1):
                getattr(self, "label_res_{:}".format(i))['text'] = app.log_window.data.loc[idx, str(games_won)]
                games_won -= 1

    def clear_all(self):
        for i in range(1, 11):
            getattr(self, "label_res_{:}".format(i))['text'] = ""
        self.user_login.delete(0, 'end')
        self.label_name['text'] = "No user loaded!"


class GlobalResults(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.geometry("350x380")
        self.title("Global Results")

        tkinter.Label(self, text="Global results").place(x=130, y=20)

        self.label_user_1 = tkinter.Label(self, text="")
        self.label_user_2 = tkinter.Label(self, text="")
        self.label_user_3 = tkinter.Label(self, text="")
        self.label_user_4 = tkinter.Label(self, text="")
        self.label_user_5 = tkinter.Label(self, text="")
        self.label_user_6 = tkinter.Label(self, text="")
        self.label_user_7 = tkinter.Label(self, text="")
        self.label_user_8 = tkinter.Label(self, text="")
        self.label_user_9 = tkinter.Label(self, text="")
        self.label_user_10 = tkinter.Label(self, text="")

        self.label_user_1.place(x=20, y=40)
        self.label_user_2.place(x=20, y=70)
        self.label_user_3.place(x=20, y=100)
        self.label_user_4.place(x=20, y=130)
        self.label_user_5.place(x=20, y=160)
        self.label_user_6.place(x=20, y=190)
        self.label_user_7.place(x=20, y=220)
        self.label_user_8.place(x=20, y=250)
        self.label_user_9.place(x=20, y=280)
        self.label_user_10.place(x=20, y=310)

        self.label_result_1 = tkinter.Label(self, text="")
        self.label_result_2 = tkinter.Label(self, text="")
        self.label_result_3 = tkinter.Label(self, text="")
        self.label_result_4 = tkinter.Label(self, text="")
        self.label_result_5 = tkinter.Label(self, text="")
        self.label_result_6 = tkinter.Label(self, text="")
        self.label_result_7 = tkinter.Label(self, text="")
        self.label_result_8 = tkinter.Label(self, text="")
        self.label_result_9 = tkinter.Label(self, text="")
        self.label_result_10 = tkinter.Label(self, text="")

        self.label_result_1.place(x=290, y=40)
        self.label_result_2.place(x=290, y=70)
        self.label_result_3.place(x=290, y=100)
        self.label_result_4.place(x=290, y=130)
        self.label_result_5.place(x=290, y=160)
        self.label_result_6.place(x=290, y=190)
        self.label_result_7.place(x=290, y=220)
        self.label_result_8.place(x=290, y=250)
        self.label_result_9.place(x=290, y=280)
        self.label_result_10.place(x=290, y=310)

        self.close_button = tkinter.Button(self, width=10, text="Close", command=self.withdraw)
        self.close_button.place(x=250, y=340)

    def show_global_results(self):
        for i in range(1, 11):
            getattr(self, "label_user_{:}".format(i))['text'] = ''
            getattr(self, "label_result_{:}".format(i))['text'] = ''
        results = app.log_window.data.loc[:, ["login", "score"]].values.tolist()
        results = dict(i for i in results)
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

        i = 1
        for user, value in results.items():
            getattr(self, "label_user_{:}".format(i))['text'] = user
            getattr(self, "label_result_{:}".format(i))['text'] = value
            i += 1


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
