import pickle

class Database:
    def __init__(self) -> None:
        self.businessOwners = []
        self.users = []
        self.admin = []
        self.resellTicketList = []

    def addAccount():
        pass

    def checkPassword():
        pass

class Account:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.messages = {}
    
    def sendMsg():
        pass

    def viewMsg():
        pass

class Admin(Account):
    def __init__(self, username, password) -> None:
        super().__init__(username, password)
    
    def cancelUserTicket():
        pass

class User(Account):
    def __init__(self, username, password, balance) -> None:
        super().__init__(username, password)
        self.balance = balance
    
    def resellTicket():
        pass

class BusinessOwner(Account):
    def __init__(self, username, password) -> None:
        super().__init__(username, password)
        self.revenue = 0
        self.rooms = []
    
    def defineRoom(BusinessType, size, regularPrice):
        pass
        

if __name__ == "__main__":
    # load database ---------------------------------------
    try:
        database = pickle.load(open("database_file.pickle", "rb"))
    except (OSError, IOError) as e:
        database = Database()
    # load database ---------------------------------------

    #  welcome pattern ---------------------------------------
    n, m = 15, 45
    for i in range(1,n,2):
      print ('-'*int((m-i*3)/2)+'.|.'*i+'-'*int((m-i*3)/2))

    print('-'*int((m-7)/2)+'WELCOME'+'-'*int((m-7)/2))

    for i in range(n-2,-1,-2):
      print ('-'*int((m-i*3)/2)+'.|.'*i+'-'*int((m-i*3)/2))
    #  welcome pattern ---------------------------------------
    print()
    accountType = input('Which one of these options best describe you? 1.Admin 2.Business Owner 3.User\n')
    if accountType == 1:
        pass
    elif accountType == 2:
        pass
    elif accountType == 3:
        pass
    else:
        print("Wrong input! (Please enter 1 or 2 or 3)")

