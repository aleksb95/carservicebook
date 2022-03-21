
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
        
        self.master=master
        # Erstelle Objekt vom Typ Inpektionsheft
        self.Inspektionsheft = IB.Inspectionbook()
        self.List_of_new_Service_Datas=[]
        self.example_contact=False
        
        master.geometry("900x600")
        master.title("Servicebook V1.0")
        style_master = ttk.Style()
        style_master.configure('TFrame')

        self.create_widgets()

        self.grid()

    # Function to Load a Existing Service Book

    def Load_inspectionbook(self):
        
        if self.example_contact is True:
            self.Inspektionsheft.ServicebookDatas=[]
            file = open("Reset_Contact", "rb")
            self.Inspektionsheft.append(pickle.load(file)) #List of Objects
        DataSet = self.Inspektionsheft.get_Inspectionbook()
        # pickle Datei öffnen und jedes Objekt aufrufen
        for i in self.TreeView.get_children():
            self.TreeView.delete(i)

        i = 0
        for _ in self.Inspektionsheft.ServicebookDatas:
            # Data=next(DataSet)

            self.TreeView.insert(parent='', index=i, text='', values=(
                next(DataSet), next(DataSet), next(DataSet), next(DataSet)))
        pass

    

    def create_widgets(self):
        self.bind_all("<Key-q>", lambda e: root.destroy())
        # Erstelle Upper Button Frame
        
        Upper_Button_Frame = ttk.Frame(self.master)

        Upper_Button_Frame.grid(row=0, column=0,columnspan=2, sticky="nsew")
        
        #Function for loading the reset Contact List for Testing
        def Load_Reset_Inspectionbook():
            self.example_contact=True
            self.Load_inspectionbook()
            self.example_contact=False
        #Adding upper Buttons
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
        TreeView_Frame = ttk.Frame(self.master)
        TreeView_Frame.grid(row=1, column=0,rowspan=1, sticky="NSEW")
        
        self.TreeView = ttk.Treeview(TreeView_Frame, show="headings", height=25)
        self.TreeView.grid(row=0, column=0, sticky="NSEW", padx=5, ipady=10)
        self.TreeView['columns'] = ("Kategorie", "Bauteil",
                               "Kilometerstand", "Anmerkungen")

        # Bind Load Function to Button command
        
        Lade_Button['command'] =Load_Reset_Inspectionbook

        

        self.TreeView.column("Kategorie", width=120, anchor=tk.W, minwidth=50)
        self.TreeView.column("Bauteil", width=120, anchor=tk.W, minwidth=50)
        self.TreeView.column("Kilometerstand", width=120, anchor=tk.W, minwidth=50)
        self.TreeView.column("Anmerkungen", width=120, anchor=tk.W, minwidth=50)

        self.TreeView.heading("Kategorie", text="Kategorie", anchor=tk.W)
        self.TreeView.heading("Bauteil", text="Bauteil", anchor=tk.W)
        self.TreeView.heading("Kilometerstand", text="Kilometerstand", anchor=tk.W)
        self.TreeView.heading("Anmerkungen", text="Anmerkungen", anchor=tk.W)

        def click(e):
            # open new Top Level Window with all of the information
            print(
                "Doppelklick!!! Hier soll sich ein TopLevel Fenster öffnen um den kompletten Eintrag anzuzeigen")
            pass
        def empty_all_labels():
                Entry_Kilometer.delete(0,'end') #syntax from delete is start index to last index (first to last     )
                Entry_Notizen.delete(0,'end')
        def select_click(e):
            selected = self.TreeView.focus()
            if selected != "":
                self.click_fill_fields(self.TreeView)
                # Here now take selection Objects and search Object in Inspectionbook
                empty_all_labels()
                # Filter all Informations from the Object
                contact_data = self.TreeView.item(selected, 'values')
                print(contact_data)
                for ServiceData in self.Inspektionsheft.ServicebookDatas:
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
        Scrollbar.grid(row=0, column=1, sticky="nsw")
        Scrollbar["command"] = self.TreeView.yview
        self.TreeView["yscrollcommand"] = Scrollbar.set

        # Erstelle Frame für Bearbeitungslabel
        Style_Labels = ttk.Style()
        Style_Labels.configure('Labels.TFrame', background='blue')
        Right_Frame_for_Label = ttk.Frame(self.master)
        
        Right_Frame_for_Label.grid(column=1, row=1,rowspan=2, sticky="nsew")

        Right_Frame_for_Label.columnconfigure(1, weight=2)

        #########-----Kategorien Label und Listbox-----##########
        Label_Kategorie = ttk.Label(Right_Frame_for_Label, text="Kategorie")

        Label_Kategorie.grid(row=1, column=0, ipadx=10, sticky="nw")
        Entry_Kategorie = tk.Listbox(Right_Frame_for_Label, height=5, width=25)
        Entry_Kategorie.grid(row=1, column=1, sticky="new", pady=10, padx=5)

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

        Button_Frame = ttk.Frame(self.master)
        Button_Frame.grid(row=2, column=1,rowspan=1, sticky="sew")
        
        Button_Save = ttk.Button(Button_Frame, text="Save")
        Button_Save.grid(row=0, column=1, sticky="nsew",padx=10,pady=20)
        
        def new_service(e):
            index_category=Entry_Kategorie.curselection()
            selection_category=Entry_Kategorie.get(index_category)
            self.New_Mode(selection_category,"Kolben",Entry_Kilometer.get(),Entry_Notizen.get())
            self.Load_inspectionbook()
        
        
        
        Button_New = ttk.Button(Button_Frame, text="Add New Data")
        Button_New.grid(row=0, column=2, sticky="nsew",padx=10,pady=20)
        Button_New.bind("<ButtonRelease-1>",new_service)
        
        Button_Delete = ttk.Button(Button_Frame, text="Delete")
        Button_Delete.grid(row=0, column=3, sticky="nsew",padx=10,pady=20)

        self.TreeView.bind("<Double-Button-1>", click)
        self.TreeView.bind("<ButtonRelease-1>", select_click)

        self.master.grid_columnconfigure(0,weight=6)
        self.master.grid_columnconfigure(1,weight=1)
        #self.grid_columnconfigure(2,weight=1)
        self.master.grid_rowconfigure(1,weight=1)
        
        
        TreeView_Frame.grid_columnconfigure(0,weight=5)
        #TreeView_Frame.grid_columnconfigure(1,weight=2)
        #TreeView_Frame.grid_rowconfigure(1,weight=1)
        TreeView_Frame.grid_rowconfigure(0,weight=1)
        Button_Frame.grid_columnconfigure(1,weight=1)
        Button_Frame.grid_columnconfigure(2,weight=1)
        Button_Frame.grid_columnconfigure(3,weight=1)
        

    def click_fill_fields(self, TreeView):
        showinfo(title="Information", message="Fields will be filled")

    def find_index(self, Category, ListBox):
        ItemList = ListBox.get(0, "end")
        print(ItemList)
        return ItemList.index(Category)

    def New_Mode(self,category_selected,part,kilometers=0,notice="",):
        "This Routine takes all values which are given and creates a new service data set. When the datas are collected they will be passed to the Inspectionbook class, where a new instance will be added to the pickle file"
        Category=category_selected
        parts=part
        km=int(kilometers)
        note=notice
        # Pass te information to the self.Inspectionbook and add the service data to it (Add function in inspectionbook)
        self.InspectionData=IB.Inspectiondata(category_selected,parts,km,note)
        #Add Inspectiondataset to Inspectionbook
        self.InspectionData.AddDatainInspectionbook(self.Inspektionsheft)



        pass
    





if __name__ == '__main__':
    ########Open Main Window ########
    root = tk.Tk()

    ########Create a Main Object for Functionality ########
    main = Main(root)

    ########Run Main Loop ########
    root.mainloop()
