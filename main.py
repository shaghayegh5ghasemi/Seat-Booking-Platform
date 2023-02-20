import pickle
import getpass
import os
from time import sleep
from tabulate import tabulate

import database
import system

class Application:
    def __init__(self) -> None:
        self.db = database.Database().loadDB() # load database 
        # index 0 for admin (accountType = 1), index 1 for business owner (accountType = 2), index 2 for user (accountType = 3)
        self.eligibility = [['1. Sign out', '2. View messages', '3. Send message', '4. Cancel User Ticket'], 
                    ['1. Sign out', '2. View messages', '3. Send message', '4. Define a room'], 
                    ['1. Sign out', '2. View messages', '3. Send message', '4. List all rooms', '5. Reserve', '6. Resell a ticket', '7. Cancel a ticket', '8. Exchange a ticket', '9. List all business types', '10. List all available users']] 

    def welcomeMsg(self, n, m):
        for i in range(1,n,2):
            print ('-'*int((m-i*3)/2)+'.|.'*i+'-'*int((m-i*3)/2))

        print('-'*int((m-7)/2)+'WELCOME'+'-'*int((m-7)/2))

        for i in range(n-2,-1,-2):
            print ('-'*int((m-i*3)/2)+'.|.'*i+'-'*int((m-i*3)/2))
        print()

    # common features between all account types
    def signIn(self):
        accountType = int(input('Which one of these options best describe you? 1.Admin 2.Business Owner 3.User\n'))
        username = input('Please enter your username:\n')
        password = getpass.getpass()
        account = None

        newAccount = self.db.exist(accountType, username) # check if the user already exists or no
        if newAccount == False:
            if accountType == 1:
                newUser = system.Admin(username, password)
                account = newUser
                self.db.addAccount(accountType, newUser)
            elif accountType == 2:
                newUser = system.BusinessOwner(username, password)
                account = newUser
                self.db.addAccount(accountType, newUser)
            elif accountType == 3:
                balance = input("What is your initial balance?\n")
                newUser = system.User(username, password, balance)
                account = newUser
                self.db.addAccount(accountType, newUser)
        else:
            authentication, acc = self.db.checkPassword(accountType, username, password)
            if authentication == False:
                print('your username and password do not match! Please try again.')
                exit()
            account = acc
        sleep(1)
        os.system('cls')
        print("Successfully logged in! :)")
        return accountType, account
    
    def signOut(self):
        seatBookingApp.db.saveDB(self.db)
        print("Thank you for choosing our platform! :)")
        exit()
    
    def sendMessage(self):
        pass

    def sendToAll(self):
        pass

    def viewMessage(self):
        pass


    # features for business owners
    def registerRoom(self, businessOwner):
        print()
        roomType = input('What business do you want this room for (Businees Type)?    ')
        size = int(input('What is the desired size of the room?    '))
        regularPrice = float(input('What is the regular price for seats?    '))
        timeSlot = input('What time slot will this room be available? (example of accepted answer: 2:30-4:05)    ')
        businessOwner.defineRoom(roomType, size, regularPrice, timeSlot)

    # features for users
    def listRooms(self):
        businessList = self.db.businessOwners
        allRooms = []
        header = ["Room #", "Business Owner", "Room Type", "Regular Price", "Time Slot"]

        for business in businessList:
            for i in range(len(business.rooms)):
                room = business.rooms[i]
                temp = []
                temp.append(i)
                temp.append(room.ownerID)
                temp.append(room.roomType)
                temp.append(room.regularPrice)
                temp.append(room.timeSlot)
                allRooms.append(temp)
        
        print (tabulate(allRooms, headers=header))


    def reserveSeat(self):
        pass


if __name__ == "__main__":
    seatBookingApp = Application()
    seatBookingApp.welcomeMsg(n=5, m=25) #  welcome pattern 
    
    accountType, account = seatBookingApp.signIn() # sign in 

    # each user based on the accountType have different elligibilities    
    while(True):
        print()
        print('What do you wish to do?')
        choice = 0
        if accountType == 1: # admin domain
            choice = int(input(seatBookingApp.eligibility[0]))
            match choice:
                case 1: # sign out
                    seatBookingApp.signOut()
                case 2: # view messages
                    pass
                case 3: # send message
                    pass
                case 4: # cancel user ticket
                    pass
        elif accountType == 2: # business owner domain
            choice = int(input(seatBookingApp.eligibility[1]))
            match choice:
                case 1: # sign out
                    seatBookingApp.signOut()
                case 2: # view messages
                    pass
                case 3: # send message
                    pass
                case 4: # define a new room
                    seatBookingApp.registerRoom(account)
        else: # user domain
            choice = int(input(seatBookingApp.eligibility[2]))
            match choice:
                case 1: # sign out
                    seatBookingApp.signOut()
                case 2: # view messages
                    pass
                case 3: # send message
                    pass
                case 4: # list all rooms
                    seatBookingApp.listRooms()
                case 5: # reserve a seat
                    pass







    

