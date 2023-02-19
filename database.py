import pickle

class Database:
    def __init__(self) -> None:
        self.admin = []
        self.businessOwners = []
        self.users = []
        self.resellTicketList = []

    def search(self, accountList, username):
        for account in accountList:
            if account.username == username:
                return True
        return False
    
    def exist(self, accountType, username):
        result = False
        match accountType:
            case 1:
                result = self.search(self.admin, username)
            case 2:
                result = self.search(self.businessOwners, username)
            case 3:
                result = self.search(self.users, username)
        return result

    def addAccount(self, accountType, newUser):
        match accountType:
            case 1:
                self.admin.append(newUser)
            case 2:
                self.businessOwners.append(newUser)
            case 3:
                self.users.append(newUser)
        

    def checkPassword(self, accountType, username, password):
        return True

    def loadDB(self):
        try:
            db = pickle.load(open("database_file.pickle", "rb"))
        except (OSError, IOError) as e:
            db = Database()
        return db

    def saveDB(self, db):    
        with open("database_file.pickle", "wb") as dbFile: # save recent changes to db before sign out
            pickle.dump(db, dbFile)
