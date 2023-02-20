import pickle

class Database:
    def __init__(self) -> None:
        self.admin = []
        self.businessOwners = []
        self.users = []
        self.resale = []

    def search(self, accountList, username):
        account = None
        for acc in accountList:
            if acc.username == username:
                account = acc
                return True, account
        return False, account
    
    def exist(self, accountType, username):
        result = False
        match accountType:
            case 1:
                result, account = self.search(self.admin, username)
            case 2:
                result, account = self.search(self.businessOwners, username)
            case 3:
                result, account = self.search(self.users, username)
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
        passwordMatch = False
        match accountType:
            case 1:
                result, account = self.search(self.admin, username)
                if account.password == password:
                    passwordMatch = True
            case 2:
                result, account = self.search(self.businessOwners, username)
                if account.password == password:
                    passwordMatch = True
            case 3:
                result, account = self.search(self.users, username)
                if account.password == password:
                    passwordMatch = True
        return passwordMatch, account

    def loadDB(self):
        try:
            db = pickle.load(open("database_file.pickle", "rb"))
        except (OSError, IOError) as e:
            db = Database()
        return db

    def saveDB(self, db):    
        with open("database_file.pickle", "wb") as dbFile: # save recent changes to db before sign out
            pickle.dump(db, dbFile)
    
    def addResale(self):
        pass

    def removeResela(self):
        pass
