
#!/usr/bin/python3
from colorsys import rgb_to_hls
from curses import termattrs
from tkinter.messagebox import showinfo
from turtle import bgcolor, color, width
import Inspektionsheft_Klasse as IB
from textwrap import fill
import tkinter as tk
import tkinter.ttk as ttk
import pickle
class Main(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        
        #Erstelle Objekt vom Typ Inpektionsheft
        self.Inspektionsheft=IB.Inspectionbook()
        
        self.create_widgets()
        self.grid()
    
    # Function to Load a Existing Service Book    
    def Load_inspectionbook(self,TreeView):
        
        file=open ("Reset_Contact", "rb")
        self.Inspektionsheft.append(pickle.load(file))
        DataSet=self.Inspektionsheft.get_Inspectionbook()
        #pickle Datei öffnen und jedes Objekt aufrufen
        for i in TreeView.get_children():
            TreeView.delete(i)
        i=0
        for _ in self.Inspektionsheft.Inspektionshefts:
            #Data=next(DataSet)
            
            TreeView.insert(parent='', index=i, text='', values=(next(DataSet), next(DataSet), next(DataSet),next(DataSet)))         
        pass    

    
    def create_widgets(self):
        self.bind_all("<Key-q>", lambda e: root.destroy())
        #Erstelle Upper Button Frame
        Upper_Button_Frame=ttk.Frame(self)
        
        Upper_Button_Frame.grid(row=0,column=0,sticky="nsew")
        
        def Load_Inspectionbook(object ):
            self.Load_inspectionbook(object)
        Lade_Button=ttk.Button(Upper_Button_Frame,text="Lade Inspektionsheft")
        Lade_Button.grid(row=0,column=0,sticky=tk.W+tk.E,pady=10,padx=5)
        Quit_Button=ttk.Button(Upper_Button_Frame,text="Beenden", command=self._root().destroy)
        Quit_Button.grid(row=0,column=1,sticky=tk.W+tk.E,pady=10,padx=5)
        # Upper_Button_Frame.columnconfigure(0,weight=1)
        # Upper_Button_Frame.columnconfigure(1,weight=7)    

        #Erstelle Frame für Treeview
        TreeView_Frame=ttk.Frame(self)
        TreeView_Frame.grid(row=1,column=0,sticky="nsew")
        TreeView=ttk.Treeview(TreeView_Frame,show="headings")
        TreeView.grid(row=0,column=0,sticky="NSEW",padx=5,ipady=10)
        TreeView['columns']=("Kategorie","Bauteil","Kilometerstand","Anmerkungen")
        
        # Bind Load Function to Button command
        Lade_Button['command']= lambda object=TreeView: self.Load_inspectionbook(object)
        
        TreeView_Frame.rowconfigure(1,weight=1)


        TreeView.column("Kategorie",width=120, anchor=tk.W, minwidth=50)
        TreeView.column("Bauteil",width=120, anchor=tk.W, minwidth=50)
        TreeView.column("Kilometerstand",width=120, anchor=tk.W, minwidth=50)
        TreeView.column("Anmerkungen",width=120, anchor=tk.W, minwidth=50)

        TreeView.heading("Kategorie",text="Kategorie",anchor=tk.W)
        TreeView.heading("Bauteil",text="Bauteil",anchor=tk.W)
        TreeView.heading("Kilometerstand",text="Kilometerstand",anchor=tk.W)
        TreeView.heading("Anmerkungen",text="Anmerkungen",anchor=tk.W)
        def click(e):
            #open new Top Level Window with all of the information
            print("Doppelklick!!! Hier soll sich ein TopLevel Fenster öffnen um den kompletten Eintrag anzuzeigen")
            pass

        def select_click(e):
            selected=TreeView.focus()
            if selected!="":
                self.click_fill_fields(TreeView)
                #Here now take selection Objects and search Object in Inspectionbook
                
                #Filter all Informations from the Object
                contact_data=TreeView.item(selected,'values')
                print(contact_data)
                for ServiceData in self.Inspektionsheft.Inspektionshefts:
                    if ServiceData.Kategorie==contact_data[0] and ServiceData.Bauteil==contact_data[1] \
                        and ServiceData.Notizen==contact_data[3] and ServiceData.Kilometerstand==int(contact_data[2]) :
                        print("Kategorie passt")
            
        TreeView.bind("<Double-Button-1>", click)
        TreeView.bind("<ButtonRelease-1>", select_click)
        # Erstellen der Scrollbar
        Scrollbar=tk.Scrollbar(TreeView_Frame)
        Scrollbar.grid( row=0,column=1, sticky="nsw")
        Scrollbar["command"]=TreeView.yview
        TreeView["yscrollcommand"]=Scrollbar.set


        # Erstelle Frame für Bearbeitungslabel
        Right_Frame_for_Label=ttk.Frame(self)
        Right_Frame_for_Label.grid(column=1,row=1, sticky="nse")
        Right_Frame_for_Label.rowconfigure(1,weight=1)
        Right_Frame_for_Label.rowconfigure(2,weight=1)
        Right_Frame_for_Label.rowconfigure(3,weight=1)
        Right_Frame_for_Label.rowconfigure(4,weight=1)
        Right_Frame_for_Label.rowconfigure(5,weight=1)

        Right_Frame_for_Label.columnconfigure(1,weight=1)
        ##########Kategorien Label und Listbox##########
        Label_Kategorie=ttk.Label(Right_Frame_for_Label,text="Kategorie")
        Label_Kategorie.grid(row=1, column=0,ipadx=10,sticky="nw")
        Entry_Kategorie=tk.Listbox(Right_Frame_for_Label,height=5,width=25)
        Entry_Kategorie.grid(row=1,column=1,columnspan=2,sticky="n",pady=10,padx=5)
        
        Kategorien=["Motor","Antrieb","Aufhängung","Bremsen/Reifen","Beleuchtung","Anderes"]
        for Kategorie in Kategorien:    
            Entry_Kategorie.insert(tk.END,Kategorie)

        # Erstellen der Scrollbar für Kategorien
        Scrollbar_Kategorie=tk.Scrollbar(Right_Frame_for_Label)
        Scrollbar_Kategorie.grid( row=1,column=3, sticky="nsw",pady=10)
        Scrollbar_Kategorie["command"]=Entry_Kategorie.yview
        Entry_Kategorie["yscrollcommand"]=Scrollbar_Kategorie.set

        ##########Bauteil Label und ?????#########
        Label_Bauteil=ttk.Label(Right_Frame_for_Label,text="Bauteil")
        Label_Bauteil.grid(row=2,column=0, sticky="nw")
        Listbox_Bauteile=tk.Listbox()


        Label_Kilometer=ttk.Label(Right_Frame_for_Label,text="Kilometerstand")
        Label_Kilometer.grid(row=3,column=0,sticky="nw",pady=10,ipadx=10)
        Entry_Kilometer=ttk.Entry(Right_Frame_for_Label,text="Kilometerstand eingeben",width=25)
        Entry_Kilometer.grid(row=3, column=1,columnspan=2,pady=10,padx=5,sticky="nw")

        Label_Notizen=ttk.Label(Right_Frame_for_Label,text="Anmerkungen")
        Label_Notizen.grid(row=4,column=0,sticky="nw",pady=10,ipadx=10)
        Entry_Notizen=ttk.Entry(Right_Frame_for_Label,width=25)
        Entry_Notizen.grid(row=4,column=1,columnspan=2,sticky="nw",pady=10,padx=5,rowspan=2)
        

        Button_Save=ttk.Button(Right_Frame_for_Label,text="Save")
        Button_Save.grid(row=5,column=0,sticky="nsew")

        Button_Edit=ttk.Button(Right_Frame_for_Label,text="Edit")
        Button_Edit.grid(row=5,column=1,sticky="nsew")

        Button_Delete=ttk.Button(Right_Frame_for_Label,text="Delete")
        Button_Delete.grid(row=5,column=2,sticky="nsew")
        Right_Frame_for_Label.columnconfigure(0,weight=1)
        Right_Frame_for_Label.columnconfigure(1,weight=2)
        Right_Frame_for_Label.columnconfigure(2,weight=5)
    
    def click_fill_fields(self,TreeView):
        showinfo(title="Information",message="Fields will be filled")
    
    









if __name__ == '__main__':
     ########Open Main Window ########
    root=tk.Tk()

    ########Create a Main Object for Functionality ########
    main=Main(root)

    ########Run Main Loop ########
    root.mainloop()