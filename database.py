import pickle
class Database:
    def __init__(self) -> None:
        self.admin = []
        self.businessOwners = []
        self.users = []
        self.resellTicketList = []

    def exist(self, accountType, username):
        return True

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
