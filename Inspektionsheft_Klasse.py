#!/usr/bin/python3




from asyncio.events import BaseDefaultEventLoopPolicy
from tkinter.ttk import Progressbar
from urllib.request import proxy_bypass
import pickle


class Inspectionbook():
    Inspektionsliste=[]
    def __init__(self):
        
        self.Inspektionshefts=[]
        

    def append(self,Objekt):
        for element in Objekt:
            self.Inspektionshefts.append(element)
        pass
        
# #Generator für getter Funktion um Listenobjekte zurückzugeben
#     @property
    def get_Inspectionbook(self):
        for DataSet in self.Inspektionshefts:
            yield DataSet.Kategorie
            yield DataSet.Bauteil
            yield DataSet.Kilometerstand
            yield DataSet.Notizen


class Inspectiondata(Inspectionbook):
    
    def __init__(self,Kategories="", Bauteil="", Kilometerstand=0, Notizen=""):
        Inspectionbook.__init__(self)
        self.Kategorie=Kategories
        self.Bauteil=Bauteil
        self.Kilometerstand=Kilometerstand
        self.Notizen=Notizen

    def AddDatainInspectionbook(self,Liste):
        Liste.append(self)

    
        
    # @property
    # def Kategorie(self):
    #     return self.Kategorie
    # @property
    # def Bauteil(self):
    #     return self.Bauteil

    # @property
    # def Kilometer(self):
    #     return self.Kilometerstand
    # @property
    # def Notizen(self):
    #     return self.Notizen

# Inspectionsdatei1=Inspectiondata("Motor","Luftfilter",230500)
# Inspectionsdatei2=Inspectiondata("Beleuchtung","Glühbirne","230500","Scheinwerfer vorne links")
# Collected_Datas=Inspectionbook()
# Inspectionsdatei1.AddDatainInspectionbook(Collected_Datas)
# Inspectionsdatei2.AddDatainInspectionbook(Collected_Datas)

# pickle.dump(Collected_Datas.Inspektionsliste,open ("Reset_Contact", "wb"))
# file=open ("Reset_Contact", "rb")
# Collected_Datas=pickle.load(file)
# #Ausgabe über getter Funktion mit dem neugeladenen file
# print(Collected_Datas[1].Bauteil)
# print(Collected_Datas[1].Kilometerstand)
# print(Collected_Datas[1].Notizen)