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
    
    def defineRoom(self, BusinessType, size, regularPrice):
        pass

class Room:
    def __init__(self, roomType, size, regularPrice) -> None:
        self.roomType = roomType 
        self.size = size
        self.regularPrice = regularPrice
        self. map = []
    
    def createRoomMap(self):
        pass 

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
