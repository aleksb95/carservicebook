#!/usr/bin/python3


import pickle

class AKlasse:
    def __init__(self, end=3):
        self.lis = list(range(1, end))
    def __str__(self):
        return "A["+str(self.lis)+"]"
    __repr__ = __str__


tup = (1, 1.0, 1+1j, (1,), "1", {1:2})
lis = [1,2,3]
lis.append(lis)
alis = [AKlasse(i) for i in range(1, 6)]
pickle.dump((tup, lis),
open("tuplis.pickle", "wb"))        #creates pickle file with data stream. The Stream includes
pickle.dump(alis,                   #the data structure (tup,lis) in file "tuplis.pickle"
open("alis.pickle", "wb"))          #Data Stream includes the Information of alis in file "alis.pickle"
pass

########## NOW WANT TO READ ##########

########## OPEN PICKLE FILE ##########
of = open("tuplis.pickle", "rb")

########## TRY TO READ TUP ONLY ##########
tup,lis=pickle.load(of)         #
print (tup)     
print (lis)
of = open("tuplis.pickle", "rb")
alis = pickle.load(open("alis.pickle", "rb"))
print (alis)
