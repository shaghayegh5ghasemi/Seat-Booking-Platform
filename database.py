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
