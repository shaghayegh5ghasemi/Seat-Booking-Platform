import numpy as np
import math
from tabulate import tabulate
import pprint

class Account:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.messages = {}

    def viewMsg(self):
        messages = self.messages
        if len(messages) == 0:
            print("Your inbox is empty!")
        else:
            pprint.pprint(messages)

class User(Account):
    def __init__(self, username, password, balance) -> None:
        super().__init__(username, password)
        self.balance = balance
        self.tickets = []
    
    def reserve(self, room, rows, columns):
        seatPrice = [] # contain price of each seat reserved by user
        for i in range(len(rows)):
            seatPrice.append(room.price[rows[i], columns[i]]) 

        ticket = Ticket(self.username, room.ownerID, room.roomType, rows, columns, seatPrice, room.date, room.timeSlot)
        self.tickets.append(ticket)
        return ticket

    def listAllTickets(self):
        for i in range(len(self.tickets)):
            print(f"Ticket # {i}:")
            self.tickets[i].printTicket()
            print("**************************************************************************************************************")

    def resellTicket(self, ticket):
        self.tickets.remove(ticket) # the ticket won't be active for the user anymore, still won't be any refund

    def cancelTicket(self, i, businessOwners):
        ticket = self.tickets[i]
        for business in businessOwners: # update the vacancy of the room after a cancelation
            if ticket.businessOwnerID == business.username:
                for room in business.rooms:
                    if ticket.roomType == room.roomType and ticket.date == room.date and ticket.timeSlot == room.timeSlot:
                        room.updateVacancy(ticket.rows, ticket.columns, 0)
        del self.tickets[i]

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
    
    def defineRoom(self, roomType, size, regularPrice, date, timeSlot):
        newRoom = Room(self.username, roomType, size, regularPrice, date, timeSlot)
        self.rooms.append(newRoom)
    
    def updateRevenue(self, price, flag):
        if flag == 'deposit':
            self.revenue = self.revenue + price
        elif flag == 'withdrawal':
            self.revenue = self.revenue - price

    def printRooms(self):
        header = ["Room #", "Business Owner", "Room Type", "Regular Price", "Date", "Time Slot"]
        i = 0
        allRooms = []
        for room in self.rooms:
            temp = []
            temp.append(i)
            temp.append(room.ownerID)
            temp.append(room.roomType)
            temp.append(room.regularPrice)
            temp.append(room.date)
            temp.append(room.timeSlot)
            allRooms.append(temp)
            i = i + 1
        
        print (tabulate(allRooms, headers=header))


class Room:
    def __init__(self, ownerID, roomType, size, regularPrice, date, timeSlot) -> None:
        self.ownerID = ownerID
        self.roomType = roomType 
        self.size = size
        self.regularPrice = regularPrice
        self.map = np.zeros((self.size, self.size), dtype=int)
        self.price = self.applyPrice()
        self.date = date
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
    def __init__(self, ticketID, businessOwnerID, roomType, rows, columns, seatPrice, date, timeSLot) -> None:
        self.ticketID = ticketID # ticket owner
        self.businessOwnerID = businessOwnerID # business owner
        self.roomType = roomType
        self.rows = rows
        self.columns = columns
        self.seatPrice = seatPrice
        self.date = date
        self.timeSlot = timeSLot
        self.discount = 0 # for resale ticket

    def ticketInfo(self):
        info = []
        header = ["Seat #", "Username", "Business Owner", "Room Type", "Row", "Column", "Date", "Time Slot", "Price", "Discount"]
        for i in range(len(self.rows)):
            temp = []
            temp.append(i) 
            temp.append(self.ticketID) 
            temp.append(self.businessOwnerID) 
            temp.append(self.roomType) 
            temp.append(self.rows[i]) 
            temp.append(self.columns[i])
            temp.append(self.date) 
            temp.append(self.timeSlot) 
            temp.append(self.seatPrice[i])
            temp.append(self.discount)
            
            info.append(temp)
        
        return info, header

    def calculateTotal(self):
        return sum(self.seatPrice)

    def printTicket(self):
        total = self.calculateTotal()
        info, header = self.ticketInfo()
        print (tabulate(info, headers=header))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'Total Price: {total} CAD') 
        if self.discount > 0:
            price = self.calculateNewPrice()
            print(f'Discount Ratio: {self.discount}') 
            print(f'Price After discount: {price} CAD') 

    
    def changeID(self, newTicketID):
        self.ticketID = newTicketID

    # for resale ticket
    def calculateNewPrice(self):
        before = self.calculateTotal()
        new = (1-self.discount)
        new = before*new
        return float(new)