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
    
    def reserve(self, room, rows, columns):
        seatPrice = []
        for i in range(len(rows)):
            seatPrice.append(room.price[rows[i], columns[i]])

        ticket = Ticket(self.username, room.ownerID, room.roomType, rows, columns, seatPrice, room.timeSlot)
        self.tickets.append(ticket)
        return ticket

    def listAllTickets(self):
        for i in range(len(self.tickets)):
            print(f"Ticket # {i}:")
            self.tickets[i].printTicket()
            print("**************************************************************************************************************")

    def resellTicket(self, ticket):
        self.tickets.remove(ticket)

    def cancelTicket(self, i, businessOwners):
        ticket = self.tickets[i]
        for business in businessOwners:
            if ticket.businessOwnerID == business.username:
                for room in business.rooms:
                    if ticket.roomType == room.roomType:
                        room.updateVacancy(ticket.rows, ticket.columns, 0)
        del self.tickets[i]

    def exchangeTicket(self):
        pass

    def listAccounts(self):
        pass

    def updateBalance(self, amount, flag):
        if flag == 'deposit':
            self.balance = self.balance + amount
        elif flag == 'withdrawal':
            self.balance = self.balance - amount




class BusinessOwner(Account):
    def __init__(self, username, password) -> None:
        super().__init__(username, password)
        self.revenue = 0
        self.rooms = []
    
    def defineRoom(self, roomType, size, regularPrice, timeSlot):
        newRoom = Room(self.username, roomType, size, regularPrice, timeSlot)
        self.rooms.append(newRoom)
    
    def updateRevenue(self, price):
        self.revenue = self.revenue + price

class Room:
    def __init__(self, ownerID, roomType, size, regularPrice, timeSlot) -> None:
        self.ownerID = ownerID
        self.roomType = roomType 
        self.size = size
        self.regularPrice = regularPrice
        self.map = np.zeros((self.size, self.size), dtype=int)
        self.price = self.applyPrice()
        self.timeSlot = timeSlot

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
        return f"Map of the {self.roomType} - {self.ownerID}"

class Ticket:
    def __init__(self, ticketID, businessOwnerID, roomType, rows, columns, seatPrice, timeSLot) -> None:
        self.ticketID = ticketID # ticket owner
        self.businessOwnerID = businessOwnerID # business owner
        self.roomType = roomType
        self.rows = rows
        self.columns = columns
        self.seatPrice = seatPrice
        self.timeSlot = timeSLot

    def ticketInfo(self):
        info = []
        header = ["Seat #", "Username", "Business Owner", "Room Type", "Row", "Column", "Time Slot", "Price"]
        total = 0
        for i in range(len(self.rows)):
            temp = []
            temp.append(i) 
            temp.append(self.ticketID) 
            temp.append(self.businessOwnerID) 
            temp.append(self.roomType) 
            temp.append(self.rows[i]) 
            temp.append(self.columns[i]) 
            temp.append(self.timeSlot) 
            temp.append(self.seatPrice[i])
            total = total + self.seatPrice[i]
            
            info.append(temp)
        
        return info, header, total

    def printTicket(self):
        info, header, total = self.ticketInfo()
        print (tabulate(info, headers=header))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'Total Price: {total} CAD') 
        return total
    

class Resale:
    def __init__(self, ticket, businessOwner, room, seller, discount) -> None:
        self.ticket = ticket
        self.businessOwner = businessOwner
        self.room = room
        self.seller = seller
        self.discount = discount

    def printResale(self):
        total = self.ticket.printTicket()
        afterDiscount = total*(1-self.discount)
        print(f'Discount Ratio: {self.discount}') 
        print(f'Price After discount: {afterDiscount} CAD') 
        return "Seat Booking Platform"
        
