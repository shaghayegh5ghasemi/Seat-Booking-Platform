import pickle
class Database:
    def __init__(self) -> None:
        self.businessOwners = []
        self.users = []
        self.admin = []
        self.resellTicketList = []

    def exist(self, accountType, username):
        return True

    def addAccount(self, accountType, newUser):
        return True

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
