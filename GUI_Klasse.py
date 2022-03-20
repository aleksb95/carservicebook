
#!/usr/bin/python3
from ast import List
from colorsys import rgb_to_hls
from curses import termattrs
from operator import index
from tkinter.messagebox import showinfo
from turtle import bgcolor, color, width
import Inspektionsheft_Klasse as IB
from textwrap import fill
import tkinter as tk
import tkinter.ttk as ttk
import pickle


class Main(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # Erstelle Objekt vom Typ Inpektionsheft
        self.Inspektionsheft = IB.Inspectionbook()
        # master.geometry("900x600")
        style_master = ttk.Style()
        style_master.configure('TFrame', background='black')

        self.create_widgets()

        self.grid()

    # Function to Load a Existing Service Book

    def Load_inspectionbook(self, TreeView):

        file = open("Reset_Contact", "rb")
        self.Inspektionsheft.append(pickle.load(file))
        DataSet = self.Inspektionsheft.get_Inspectionbook()
        # pickle Datei öffnen und jedes Objekt aufrufen
        for i in TreeView.get_children():
            TreeView.delete(i)
        i = 0
        for _ in self.Inspektionsheft.Inspektionshefts:
            # Data=next(DataSet)

            TreeView.insert(parent='', index=i, text='', values=(
                next(DataSet), next(DataSet), next(DataSet), next(DataSet)))
        pass

    

    def create_widgets(self):
        self.bind_all("<Key-q>", lambda e: root.destroy())
        # Erstelle Upper Button Frame
        Style = ttk.Style()
        Style.configure('TFrame', background='black')
        Upper_Button_Frame = ttk.Frame(self, style='TFrame')

        Upper_Button_Frame.grid(row=0, column=0, sticky="nsew")

        def Load_Inspectionbook(object):
            self.Load_inspectionbook(object)
        Lade_Button = ttk.Button(
            Upper_Button_Frame, text="Lade Inspektionsheft")
        Lade_Button.grid(row=0, column=0, sticky=tk.W+tk.E, pady=10, padx=5)
        Quit_Button = ttk.Button(
            Upper_Button_Frame, text="Beenden", command=self._root().destroy)
        Quit_Button.grid(row=0, column=1, sticky=tk.W+tk.E, pady=10, padx=5)
        # Upper_Button_Frame.columnconfigure(0,weight=1)
        # Upper_Button_Frame.columnconfigure(1,weight=7)

        

        # Erstelle Frame für Treeview
        style_treeview = ttk.Style()
        style_treeview.configure('Tree.TFrame', background='red')
        TreeView_Frame = ttk.Frame(self, style='Tree.TFrame')
        TreeView_Frame.grid(row=1, column=0, sticky="nsew")
        TreeView = ttk.Treeview(TreeView_Frame, show="headings", height=25)
        TreeView.grid(row=0, column=0, sticky="NSE", padx=5, ipady=10)
        TreeView['columns'] = ("Kategorie", "Bauteil",
                               "Kilometerstand", "Anmerkungen")

        # Bind Load Function to Button command
        Lade_Button['command'] = lambda object=TreeView: self.Load_inspectionbook(
            object)

        TreeView_Frame.rowconfigure(1, weight=1)

        TreeView.column("Kategorie", width=120, anchor=tk.W, minwidth=50)
        TreeView.column("Bauteil", width=120, anchor=tk.W, minwidth=50)
        TreeView.column("Kilometerstand", width=120, anchor=tk.W, minwidth=50)
        TreeView.column("Anmerkungen", width=120, anchor=tk.W, minwidth=50)

        TreeView.heading("Kategorie", text="Kategorie", anchor=tk.W)
        TreeView.heading("Bauteil", text="Bauteil", anchor=tk.W)
        TreeView.heading("Kilometerstand", text="Kilometerstand", anchor=tk.W)
        TreeView.heading("Anmerkungen", text="Anmerkungen", anchor=tk.W)

        def click(e):
            # open new Top Level Window with all of the information
            print(
                "Doppelklick!!! Hier soll sich ein TopLevel Fenster öffnen um den kompletten Eintrag anzuzeigen")
            pass
        def empty_all_labels():
                Entry_Kilometer.delete(0,'end') #syntax from delete is start index to last index (first to last     )
                Entry_Notizen.delete(0,'end')
        def select_click(e):
            selected = TreeView.focus()
            if selected != "":
                self.click_fill_fields(TreeView)
                # Here now take selection Objects and search Object in Inspectionbook
                empty_all_labels()
                # Filter all Informations from the Object
                contact_data = TreeView.item(selected, 'values')
                print(contact_data)
                for ServiceData in self.Inspektionsheft.Inspektionshefts:
                    if ServiceData.Kategorie == contact_data[0] and ServiceData.Bauteil == contact_data[1] \
                            and ServiceData.Notizen == contact_data[3] and ServiceData.Kilometerstand == int(contact_data[2]):
                        print("found")
                        index_for_catergory = self.find_index(
                            ServiceData.Kategorie, Entry_Kategorie)
                        Entry_Kategorie.select_set(index_for_catergory)
                        # The Parts will be shown depending on the selection in the Category,\
                        #  but for now there will be shown Checkboxes which will be checked
                        Entry_Kilometer.insert(0, ServiceData.Kilometerstand)
                        Entry_Notizen.insert(0, ServiceData.Notizen)

        # Erstellen der Scrollbar
        Scrollbar = tk.Scrollbar(TreeView_Frame)
        Scrollbar.grid(row=0, column=1, sticky="nesw")
        Scrollbar["command"] = TreeView.yview
        TreeView["yscrollcommand"] = Scrollbar.set

        # Erstelle Frame für Bearbeitungslabel
        Style_Labels = ttk.Style()
        Style_Labels.configure('Labels.TFrame', background='blue')
        Right_Frame_for_Label = ttk.Frame(self, style='Labels.TFrame')
        Right_Frame_for_Label.columnconfigure(1, weight=1)
        Right_Frame_for_Label.grid(column=1, row=1, sticky="new")

        Right_Frame_for_Label.columnconfigure(1, weight=1)

        #########-----Kategorien Label und Listbox-----##########
        Label_Kategorie = ttk.Label(Right_Frame_for_Label, text="Kategorie")

        Label_Kategorie.grid(row=1, column=0, ipadx=10, sticky="nw")
        Entry_Kategorie = tk.Listbox(Right_Frame_for_Label, height=5, width=25)
        Entry_Kategorie.grid(row=1, column=1, sticky="nw", pady=10, padx=5)

        Kategorien = ["Motor", "Antrieb", "Aufhängung",
                      "Bremsen/Reifen", "Beleuchtung", "Anderes"]
        for Kategorie in Kategorien:
            Entry_Kategorie.insert(tk.END, Kategorie)

        # Erstellen der Scrollbar für Kategorien
        Scrollbar_Kategorie = tk.Scrollbar(Right_Frame_for_Label)
        Scrollbar_Kategorie.grid(row=1, column=2, sticky="nsw", pady=10)
        Scrollbar_Kategorie["command"] = Entry_Kategorie.yview
        Entry_Kategorie["yscrollcommand"] = Scrollbar_Kategorie.set

        ##########Bauteil Label und ?????#########
        Label_Bauteil = ttk.Label(Right_Frame_for_Label, text="Bauteil")
        Label_Bauteil.grid(row=2, column=0, sticky="new")
        Listbox_Bauteile = tk.Listbox()

        Label_Kilometer = ttk.Label(
            Right_Frame_for_Label, text="Kilometerstand")
        Label_Kilometer.grid(row=3, column=0, sticky="new", pady=10, ipadx=10)
        Entry_Kilometer = ttk.Entry(
            Right_Frame_for_Label, text="Kilometerstand eingeben", width=25)
        Entry_Kilometer.grid(row=3, column=1, pady=10, padx=5, sticky="new")

        Label_Notizen = ttk.Label(Right_Frame_for_Label, text="Anmerkungen")
        Label_Notizen.grid(row=4, column=0, sticky="nw", pady=10, ipadx=10)
        Entry_Notizen = ttk.Entry(Right_Frame_for_Label, width=25)
        Entry_Notizen.grid(row=4, column=1, sticky="new", pady=10, padx=5)

        s = ttk.Style()
        s.configure('s.TFrame', background='green')

        Button_Frame = ttk.Frame(self, style='s.TFrame')
        Button_Frame.grid(row=2, column=1, sticky="nsew")
        Button_Save = ttk.Button(Button_Frame, text="Save")
        Button_Save.grid(row=5, column=0, sticky="nsw")
        
        def new_service(e):
            index_category=Entry_Kategorie.curselection()
            selection_category=Entry_Kategorie.get(index_category)
            self.New_Mode(selection_category,"Kolben",Label_Kilometer.get(),Label_Notizen.cget("text"))
        
        
        
        Button_New = ttk.Button(Button_Frame, text="Edit")
        Button_New.grid(row=5, column=1, sticky="nsw")
        Button_New.bind("<ButtonRelease-1>",new_service)
        Button_Delete = ttk.Button(Button_Frame, text="Delete")
        Button_Delete.grid(row=5, column=2, sticky="nsw")

        TreeView.bind("<Double-Button-1>", click)
        TreeView.bind("<ButtonRelease-1>", select_click)

        # # self.grid_columnconfigure(0,weight=1)
        # # self.grid_columnconfigure(1,weight=1)
        # # self.grid_columnconfigure(2,weight=1)
        # # self.grid_rowconfigure(0,weight=1)
        # # self.grid_rowconfigure(1,weight=1)
        # TreeView_Frame.grid_columnconfigure(0,weight=3)
        # TreeView_Frame.grid_columnconfigure(1,weight=1)
        # TreeView_Frame.grid_rowconfigure(1,weight=1)
        # TreeView_Frame.grid_rowconfigure(0,weight=1)
        # Right_Frame_for_Label.grid_columnconfigure(0,weight=1)
        # Right_Frame_for_Label.grid_columnconfigure(1,weight=1)
        # Right_Frame_for_Label.grid_rowconfigure(0,weight=1)
        # Button_Frame.grid_columnconfigure

    def click_fill_fields(self, TreeView):
        showinfo(title="Information", message="Fields will be filled")

    def find_index(self, Category, ListBox):
        ItemList = ListBox.get(0, "end")
        print(ItemList)
        return ItemList.index(Category)

    def New_Mode(self,category_selected,part,kilometers,notice,):
        "This Routine takes all values which are given and creates a new service data set. When the datas are collected they will be passed to the Inspectionbook class, where a new instance will be added to the pickle file"
        Category=category_selected
        parts=part
        km=kilometers
        note=notice
        pass


if __name__ == '__main__':
    ########Open Main Window ########
    root = tk.Tk()

    ########Create a Main Object for Functionality ########
    main = Main(root)

    ########Run Main Loop ########
    root.mainloop()
