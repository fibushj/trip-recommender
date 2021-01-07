#TODO: refactor reg and login, refactor utils, show reviews in profile, del(/update) reviews in profile, add review in double click, statistics?,
from ctypes import windll
from functools import partial
from tkinter import *
from tkinter import ttk

import tkcalendar as tkcalendar
from ttkwidgets import TickScale

from gui.location_window import LocationWindow
from gui.myFilterList import MyFilterList
from gui.profile_window import ProfileWindow

HEIGHT = 960
WIDTH = 1366
FRAME_BG = '#80c1ff'

class MainGUI:
    reg_window=None
    login_window=None
    def __init__(self, database):
        windll.shcore.SetProcessDpiAwareness(1) # fix blurred fonts

        self.window = Tk()
        self.window.title("Around The World")
        self.window.geometry(str(WIDTH) + 'x' + str(HEIGHT))

        left_frame = Frame(self.window, bg=FRAME_BG, bd=3)
        left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        # Create Tab Control
        left_tabs_control = ttk.Notebook(left_frame)
        # Create first tab in left frame- search by feature tab
        self.create_f_search_tab(left_frame,left_tabs_control)
        # Create second tab in left frame- search by radius tab
        self.create_radius_search_tab(left_frame,left_tabs_control)
        left_tabs_control.pack(expand=True, fill=BOTH)

        # Create right frame
        right_frame = Frame(self.window, bg=FRAME_BG, bd=10)
        right_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
        self.create_locations_view(right_frame)

        menu_widget = Menu(self.window)
        self.is_logged_in=True
        menu_widget.add_command(label="Profile", command=self.log_in_screen if (not self.is_logged_in) else self.view_profile)
        menu_widget.add_command(label="Statistics", command=self.statistics_screen)
        menu_widget.add_command(label="Quit", command=self.window.destroy)

        # display the menu
        self.window.config(menu=menu_widget)

    #TODO: implement!
    def validate_and_login(self,login_window,get_username, get_password):
        print("username entered :", get_username())
        print("password entered :", get_password())
        login_window.destroy()
        return

    def log_in_screen(self):
        # destroy registration windows if exists
        if(self.reg_window):
            self.reg_window.destroy()
        self.login_window = Toplevel()
        self.login_window.title("Login")
        self.login_window.geometry("210x250")
        Label(self.login_window, text="Please enter login details:").pack()
        Label(self.login_window, text="").pack()
        Label(self.login_window, text="Username").pack()
        username = StringVar()
        username_login_entry = Entry(self.login_window, textvariable=username)
        username_login_entry.pack()
        Label(self.login_window, text="").pack()
        Label(self.login_window, text="Password").pack()
        password = StringVar()
        password__login_entry = Entry(self.login_window, textvariable=password, show='*')
        password__login_entry.pack()
        Label(self.login_window, text="").pack()
        validate_and_login = partial(self.validate_and_login,self.login_window, username.get, password.get)
        Button(self.login_window, text="Log In", width=10, height=1,command=validate_and_login).pack()

        reg_labelframe=ttk.Labelframe(self.login_window,text="OR")
        reg_labelframe.pack(ipadx=20, ipady=5)
        Button(reg_labelframe, text="Register", width=10, height=1, command=self.reg_screen).pack()

        self.login_window.mainloop()

    #TODO: implement!
    def validate_and_register(self, reg_window, get_username, get_password, get_birthday):
        print("username entered :", get_username())
        print("password entered :", get_password())
        print("birthday entered :", get_birthday())

        reg_window.destroy()
        return

    def reg_screen(self):
        # destroy login windows if exists
        if(self.login_window):
            self.login_window.destroy()
        self.reg_window = Toplevel()
        self.reg_window.title("Register")
        self.reg_window.geometry("210x320")
        Label(self.reg_window, text="Please enter registration details:").pack()
        Label(self.reg_window, text="").pack()
        Label(self.reg_window, text="Username").pack()
        username = StringVar()
        username_login_entry = Entry(self.reg_window, textvariable=username)
        username_login_entry.pack()
        Label(self.reg_window, text="").pack()
        Label(self.reg_window, text="Password").pack()
        password = StringVar()
        password__login_entry = Entry(self.reg_window, textvariable=password, show='*')
        password__login_entry.pack()
        Label(self.reg_window, text="").pack()

        Label(self.reg_window, text="Birthday").pack()
        birthday_picker = tkcalendar.DateEntry(self.reg_window, width=12, year=2000, month=1, day=1, date_pattern="dd-mm-y",
                        background='darkblue', foreground='white', borderwidth=2)
        birthday_picker.pack()

        Label(self.reg_window, text="").pack()

        validate_and_register = partial(self.validate_and_register, self.reg_window, username.get, password.get, birthday_picker.get_date)
        Button(self.reg_window, text="Register", width=10, height=1, command=validate_and_register).pack()

        reg_labelframe = ttk.Labelframe(self.reg_window, text="OR")
        reg_labelframe.pack(ipadx=20, ipady=5)
        Button(reg_labelframe, text="Log In", width=10, height=1, command=self.log_in_screen).pack()

        self.reg_window.mainloop()

    def statistics_screen(self):
        self.login_window = Toplevel()
        self.login_window.title("Statistics")
        self.login_window.geometry("210x250")


    def create_locations_view(self, containing_frame):
        self.locations_view = ttk.Treeview(containing_frame, selectmode='browse')
        self.locations_view['show'] = 'headings'
        self.locations_view["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        self.locations_view.column("#0", width=0, minwidth=0, stretch=YES)
        self.locations_view.column("1", width=160, minwidth=80, stretch=YES)
        self.locations_view.column("2", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("3", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("4", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("5", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("6", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("7", width=80, minwidth=50, stretch=YES)

        self.locations_view.heading("1", text="Name", anchor=W)
        self.locations_view.heading("2", text="Latitude", anchor=W)
        self.locations_view.heading("3", text="Longitude", anchor=W)
        self.locations_view.heading("4", text="Category", anchor=W)
        self.locations_view.heading("5", text="Sub Category", anchor=W)
        self.locations_view.heading("6", text="Country", anchor=W)
        self.locations_view.heading("7", text="Rating", anchor=W)

        # TODO JHONNY: insert all results that match the user's input, in this format:
        folder1 = self.locations_view.insert("", 1, None, values=(
            "Pic de Font Blanca", "42.64991", "1.53335", "...", "...", "Europe/Andorra", "4.5"))
        self.locations_view.bind("<Double-1>", self.location_double_click)
        self.locations_view.pack(expand=True, fill=BOTH)

    #TODO: implement!
    def view_profile(self):
        profile_window = ProfileWindow()

    def run(self):
        self.window.mainloop()

    def create_filter_list(self,frame, source):
        filter_list = MyFilterList(frame, source=source, display_rule=lambda item: item,
                                   filter_rule=lambda item, text: text.lower() in item.lower())
        filter_list.pack(expand=True, fill=X)

        def show_result(event=None):
            item = filter_list.selection()
            if item: filter_list.set_entry_text(item)

        # Show the result of the calculation on Return or double-click
        filter_list.bind("<Return>", show_result)
        filter_list.bind("<Double-Button-1>", show_result)
        return filter_list


    # Create second tab in left frame- search by radius tab
    def create_trip_filter(self,frame):
        trip_frame = Frame(frame, bg=FRAME_BG, bd=3)
        trip_frame.pack(expand=True, fill=X)
        trip_type_val = StringVar()
        trip_season_val = StringVar()
        trip_type_options = ["Family", "Couples", "Solo"]
        trip_season_options = ["Spring", "Summer", "Fall", "Winter"]
        trip_type_dropmenu = ttk.OptionMenu(trip_frame, trip_type_val, "Trip type", "All", *trip_type_options)
        trip_season_dropmenu = ttk.OptionMenu(trip_frame, trip_season_val, "Trip season", "All", *trip_season_options)
        trip_type_dropmenu.config(width=10)
        trip_season_dropmenu.config(width=10)
        trip_type_dropmenu.pack(side="left", padx=3, expand=True, fill=X)
        trip_season_dropmenu.pack(side="right", padx=3, expand=True, fill=X)
        # trip_type_dropmenu.bind("<Return>", print_something)


    # Create first tab in left frame- search by feature tab
    def create_f_search_tab(self,left_frame,left_tabs_control):
        f_search_tab = Frame(left_frame, bg=FRAME_BG, bd=3)
        left_tabs_control.add(f_search_tab, text='Search By Country')

        country_frame = Frame(f_search_tab, bg=FRAME_BG, bd=3)
        country_frame.pack(expand=True, fill=X)
        country_label = Label(country_frame, text="Country:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all countries full name
        country_list_items = ["Denmark", "France", "Germany", "Israel", "United States", "United Kingdom"]
        country_filter_list = self.create_filter_list(country_frame, country_list_items)

        f_class_frame = Frame(f_search_tab, bg=FRAME_BG, bd=3)
        f_class_frame.pack(expand=True, fill=X)
        f_class_label = Label(f_class_frame, text="Feature Class:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all feature classes full name
        f_class_list_items = ["country, state, region...", "stream, lake...", "parks,area..."]
        f_class_filter_list = self.create_filter_list(f_class_frame, f_class_list_items)

        f_code_frame = Frame(f_search_tab, bg=FRAME_BG, bd=3)
        f_code_frame.pack(expand=True, fill=X)
        f_code_label = Label(f_code_frame, text="Feature Code:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all feature codes full name that match the selected feature code
        f_code_list_items = ["Will change according to the feature class"]
        f_code_filter_list = self.create_filter_list(f_code_frame, f_code_list_items)

        trip_filter = self.create_trip_filter(f_search_tab)

        #TODO JHONNY: query to get results using all filters and insert to locations_view
        f_submit_button = Button(f_search_tab, text="Search", width=20, command=lambda: None)
        f_submit_button.pack(expand=True)


    def create_radius_search_tab(self,left_frame,left_tabs_control):
        radius_search_tab = Frame(left_frame, bg=FRAME_BG, bd=3)
        left_tabs_control.add(radius_search_tab, text='Search By Radius')

        lat_frame = Frame(radius_search_tab, bg=FRAME_BG, bd=3)
        lat_frame.pack(expand=True, fill=X)
        lat_label = Label(lat_frame, text="Latitude:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        lat_entry = Entry(lat_frame)
        lat_entry.pack(expand=True, fill=X)

        lon_frame = Frame(radius_search_tab, bg=FRAME_BG, bd=3)
        lon_frame.pack(expand=True, fill=X)
        lon_label = Label(lon_frame, text="Longitude:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        lon_entry = Entry(lon_frame)
        lon_entry.pack(expand=True, fill=X)

        radius_frame = Frame(radius_search_tab, bg=FRAME_BG, bd=3)
        radius_frame.pack(expand=True, fill=X)
        radius_label = Label(radius_frame, text="Radius:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        ttk.Style().configure('Horizontal.TScale', background=FRAME_BG) # define a style object for the scale widget
        radius_slider = TickScale(radius_frame, from_=0, to=1000,style="Horizontal.TScale", orient=HORIZONTAL, digits=0)
        radius_slider.pack(expand=True, fill=X)

        f_class_frame = Frame(radius_search_tab, bg=FRAME_BG, bd=3)
        f_class_frame.pack(expand=True, fill=X)
        f_class_label = Label(f_class_frame, text="Feature Class:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all feature classes full name
        f_class_list_items = ["country, state, region...", "stream, lake...", "parks,area..."]
        f_class_filter_list = self.create_filter_list(f_class_frame, f_class_list_items)

        f_code_frame = Frame(radius_search_tab, bg=FRAME_BG, bd=3)
        f_code_frame.pack(expand=True, fill=X)
        f_code_label = Label(f_code_frame, text="Feature Code:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all feature codes full name that match the selected feature code
        f_code_list_items = ["Will change according to the feature class"]
        f_code_filter_list = self.create_filter_list(f_code_frame, f_code_list_items)

        trip_filter = self.create_trip_filter(radius_search_tab)

        #TODO JHONNY: query to get results using all filters and insert to locations_view
        radius_submit_button = Button(radius_search_tab, text="Search", width=20, command=lambda: None)
        radius_submit_button.pack(expand=True)

    def location_double_click(self, event):
        item = self.locations_view.selection()[0]
        item_name = self.locations_view.item(item)["values"][0]
        LocationWindow(item,item_name)


