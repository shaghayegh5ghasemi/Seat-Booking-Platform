import numpy as np
import math
from tabulate import tabulate

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
        self.tickets = []
    
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
        middle = math.floor(self.size/2) - 1

        # two middle columns
        price[1:-1, middle:middle+2] = price[1:-1, middle:middle+2]*1.25
        # first row
        price[0, :] = price[0, :]*2 
        # last row
        price[-1, :] = price[-1, :]*0.75

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
    def __init__(self, ownerID, ticketID, roomType, rows, columns, seatPrice) -> None:
        self.ownerID = ownerID # ticket owner
        self.ticketID = ticketID # business owner
        self.roomType = roomType
        self.rows = rows
        self.columns = columns
        self.seatPrice = seatPrice

    def ticketInfo(self):
        info = []
        header = ["Seat #", "Username", "Business Owner", "Room Type", "Row", "Column", "Price"]
        for i in range(len(self.rows)):
            temp = []
            temp.append(i, self.ownerID, self.ticketID, self.roomType, self.rows[i], self.columns[i], self.seatPrice[i])
        
        return info, header

    def printTicket(self):
        info, header = self.ticketInfo()
        temp = np.array(info)
        total = np.sum(temp[:, -1])
        print (tabulate(info, headers=header))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'Total Price: {total}')

class Resale:
    def __init__(self) -> None:
        self.resaleList = []

    def addResale(self):
        pass

    def removeResale(self):
        pass
