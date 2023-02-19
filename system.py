class Account:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.messages = {}
    
    def sendMsg(self):
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
    x = 1

class Ticket:
    a = 2

class Resell:
    b = 3
