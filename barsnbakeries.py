from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import font
import pg8000

class LoginBox:
    def __init__(self, window):
        self.window = window

        self.window.title('Login')
        self.window.grid()

        # styling
        self.font = font.Font(family = 'Arial', size = 12)
        Style().configure('TButton', font = self.font)
        Style().configure('TLabel', font = self.font)

        self.user_label = Label(window, text='Flowers Username: ')
        self.user_label.grid(column = 0, row = 0)
        self.user_input = Entry(window, width = 20, font = self.font)
        self.user_input.grid(column = 1, row = 0)

        self.pw_label = Label(window, text='Password: ')
        self.pw_label.grid(column = 0, row = 1)
        self.pw_input = Entry(window, width = 20, show='*', font = self.font)
        self.pw_input.grid(column = 1, row = 1)

        self.button_frame = Frame(window)
        self.button_frame.grid(column = 0, columnspan = 2, row = 2)

        self.ok_button = Button(self.button_frame, text='OK', command=self.ok_action)
        self.ok_button.grid(column = 0, row = 0)

        self.cancel_button = Button(self.button_frame, text='Cancel', command=quit)
        self.cancel_button.grid(column = 1, row=0)

        self.window.bind('<Return>', self.enter_action)
        self.user_input.focus_set()

    def enter_action(self, event):
        self.ok_action()

    def ok_action(self):
        try:        
            credentials = {'user'     : self.user_input.get(),
                           'password' : self.pw_input.get(),
                           'database' : 'csci403',
                           'host'     : 'flowers.mines.edu' }
            self.db = pg8000.connect(**credentials)
            self.window.destroy()
        except pg8000.Error as e:
            messagebox.showerror('Login Failed', e.args[2])

class BarsnBakeries:
    def __init__(self, window, db):
        self.window = window
        self.window.title('Bars n\' Bakeries')
        self.window.grid()

        self.db = db
        self.cursor = db.cursor()
        
        # Font
        self.font = font.Font(family = 'Arial', size = 12)
        Style().configure('TButton', font = self.font)
        Style().configure('TLabel', font = self.font)

        # Search bar, no pun intended
        self.search_frame = Frame(window)
        self.search_frame.grid(row = 0, column = 0)
        self.search_label = Label(self.search_frame, text = 'Search: ')
        self.search_label.grid(row = 0, column = 0)
        self.search_text = Entry(self.search_frame, width = 40, font = self.font)
        self.search_text.grid(row = 0, column = 1)
        self.search_button = Button(self.search_frame, text = 'Search', command = self.search_action)
        self.search_button.grid(row = 0, column = 2)

        # Results
        self.results_frame = Frame(window)
        self.results_frame.grid(row = 1, column = 0)
        self.results_sb = Scrollbar(self.results_frame)
        self.results_sb.pack(side = RIGHT, fill = Y)
        self.results_lb = Listbox(self.results_frame, height = 10, width = 80, font = self.font, exportselection = 0)
        self.results_lb.pack()
        self.results_lb.config(yscrollcommand = self.results_sb.set)
        self.results_sb.config(command = self.results_lb.yview)
        self.current_search_results = []
        self.edit_frame = Frame(window)
        self.edit_frame.grid(row = 2, column = 0, padx = 10, pady = 10)
        

        # search results listbox callbacks
        self.results_lb.bind('<<ListboxSelect>>')

    def search_action(self):
        search_string = self.search_text.get()
        self.results_lb.delete(0, self.results_lb.size())
        self.current_search_results = self.search(search_string)
        for name, address, stars in self.current_search_results:
            s = name + ' - ' + address + ' (' + str(stars) + ')'
            self.results_lb.insert(END, s)

    def recreate_edit_frame(self):
        self.edit_frame.destroy()
        self.edit_frame = Frame(window)
        self.edit_frame.grid(row = 2, column = 0, padx = 10, pady = 10)

    def search(self, search_string):
        query = """SELECT name, address, stars
                   FROM barsnbakeries
                   WHERE lower(name) LIKE lower(%s)
                   AND service = \"bar\""""

        search_string = '%' + search_string + '%'
        try:
            self.cursor.execute(query, (search_string, ))

            resultset = self.cursor.fetchall()
            return resultset

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None

lb = Tk()
lbapp = LoginBox(lb)
lb.mainloop()

window = Tk()
bnb = BarsnBakeries(window, lbapp.db)
window.mainloop()