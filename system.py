import numpy as np
import math

class Account:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.messages = {}
    
    def sendMsg(self, db, accountList, destUsername, msg):
        pass

    def viewMsg(self):
        pass

class Admin(Account):
    def __init__(self, username, password) -> None:
        super().__init__(username, password)
    
    def cancelUserTicket(self):
        pass

class User(Account):
    def __init__(self, username, password, balance) -> None:
        super().__init__(username, password)
        self.balance = balance
    
    def reserve(self):
        pass

    def resellTicket(self):
        pass

    def cancelTicket(self):
        pass

    def exchangeTicket(self):
        pass

    def listAccounts(self):
        pass


class BusinessOwner(Account):
    def __init__(self, username, password) -> None:
        super().__init__(username, password)
        self.revenue = 0
        self.rooms = []
    
    def defineRoom(self, roomType, size, regularPrice):
        newRoom = Room(self.username, roomType, size, regularPrice)
        self.rooms.append(newRoom)
    
    def updateRevenue(self, price):
        self.revenue = self.revenue + price

class Room:
    def __init__(self, ownerID, roomType, size, regularPrice) -> None:
        self.ownerID = ownerID
        self.roomType = roomType 
        self.size = size
        self.regularPrice = regularPrice
        self.map = np.zeros((self.size, self.size), dtype=int)
        self.price = self.applyPrice()

    def applyPrice(self):
        price = np.full((self.size, self.size), self.regularPrice)
        middle = math.floor(self.size/2)

        # two middle columns
        price[:, middle] = price[:, 0]*1.25
        price[:, middle+1] = price[:, 1]*1.25 
        # first two rows
        price[0, :] = price[:, 0]*2 
        price[1, :] = price[:, 1]*2 
        # last two rows
        price[-2, :] = price[:, 0]*0.75 
        price[-1, :] = price[:, 1]*0.75

        return price
        
    def updateVacancy(self, rows, columns, fill):
        for i in range(len(rows)):
            self.map[rows[i], columns[i]] = fill # if fill = 1 reserve seat otherwise make it available

    def showMap(self):
        arr = self.map
        columnID = np.array([*range(0, self.size, 1)])
        arr = np.append(arr, [columnID], axis=0)
        columnID = np.append(columnID, 0)
        rowID = columnID.reshape((len(columnID), 1))
        arr = np.append(arr, rowID, axis=1)
        
        for a in arr:
            for elem in a:
                print("{}".format(elem).rjust(3), end="")
            print(end="\n")

class Ticket:
    def __init__(self, ticketID, username, roomType, seatDetail) -> None:
        self.ticketID = ticketID
        self.username = username
        self.roomType = roomType
        self.seatDetail = seatDetail
    
    def printTicket(self):
        pass

class Resale:
    def __init__(self) -> None:
        self.resaleList = []

    def addResale(self):
        pass

    def removeResale(self):
        pass
