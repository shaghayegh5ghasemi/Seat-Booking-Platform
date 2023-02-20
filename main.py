import numpy as np
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
                    ['1. Sign out', '2. View messages', '3. Send message', '4. List all rooms', 
                    '5. List all resale tickets', '6. List all business owners', '7. List all system users', '8. Reserve', '9. Resell a ticket',
                     '10. Cancel a ticket', '11. Exchange a ticket', '12. Update Balance']] 

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
                balance = float(input("What is your initial balance?\n"))
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
        roomType = input('What business do you want this room for (Businees Type)? ')
        size = int(input('What is the desired size of the room? '))
        regularPrice = float(input('What is the regular price for seats? '))
        timeSlot = input('What time slot will this room be available? (example of accepted answer: 2:30-4:05) ')
        businessOwner.defineRoom(roomType, size, regularPrice, timeSlot)

    # features for users
    def listRooms(self): # 4. list all rooms
        businessList = self.db.businessOwners
        allRoomObjects = []
        allRooms = []
        header = ["Room #", "Business Owner", "Room Type", "Regular Price", "Time Slot"]

        i = 0
        for business in businessList:
            for room in business.rooms:
                temp = []
                temp.append(i)
                temp.append(room.ownerID)
                temp.append(room.roomType)
                temp.append(room.regularPrice)
                temp.append(room.timeSlot)
                allRooms.append(temp)
                allRoomObjects.append(room)
                i = i + 1
        
        print (tabulate(allRooms, headers=header))

        return allRoomObjects

    def listResaletickets(self): # 5. list all resale tickets
        allResaleTickets = self.db.resale
        for resale in allResaleTickets:
            resale.printResale()

    def listBusinessOwners(self): # 6. list all business owners
        info = []
        header = ["Business Owner #", "Name", "Number of registered room"]
        allBusinessOwners = self.db.businessOwners
        for i in range(len(allBusinessOwners)):
            temp = []
            temp.append(i)
            temp.append(allBusinessOwners[i].username)
            temp.append(len(allBusinessOwners[i].rooms))
            info.append(temp)
        print (tabulate(info, headers=header))

    def listSystemUsers(self): # 7. list all system users
        info = []
        header = ["User #", "Username"]
        allusers = self.db.users
        for i in range(len(allusers)):
            temp = []
            temp.append(i)
            temp.append(allusers[i].username)
            info.append(temp)
        print (tabulate(info, headers=header))

    def toMin(self, timeSlot): # convert hh:mm input format to an integer that show which min from midnight!
        s, e = timeSlot.split('-')
        sHour, sMin = s.split(':')
        eHour, eMin = e.split(':')
        strat = int(sHour)*60 + int(sMin)
        end = int(eHour)*60 + int(eMin)
        return strat, end

    def checkTimeOverlap(self, timeSlot1, timeSlot2): # check overlap between two time slots based on their converted format
        # source of algorithm: https://stackoverflow.com/questions/3269434/whats-the-most-efficient-way-to-test-if-two-ranges-overlap
        overlap = False
        
        start1, end1 = self.toMin(timeSlot1) 
        width1 = end1 - start1

        start2, end2 = self.toMin(timeSlot2)
        width2 = end2 - start2 

        minRange = min(start1, start2)
        maxRange = max(end1, end2)

        if width1 + width2 > maxRange - minRange:
            overlap = True
        
        return overlap     

    def checkTicketTimeSlot(self, newReservation, previousReservations): # check if a new reservation has overlap with previous reservations
        overlap = False
        for t in previousReservations:
            if self.checkTimeOverlap(newReservation, t.timeSlot):
                overlap = True
                break
        
        return overlap

    def reserveSeat(self, user): # 8. reserve a seat
        allRoomObjects = self.listRooms()
        print()
        roomNumber = int(input("You want to reserve from which Room # ? "))
        desiredRoom = allRoomObjects[roomNumber]
        desiredRoom.showMap()

        # ask for the detail (row and column)
        seatNumbers = int(input('How many seats do you want to reserve? '))
        rows = []
        columns = []
        for i in range(seatNumbers):
            row, column = input(f'Enter the row and column of seat # {i}: (example: 3,4)' ).split(',')
            rows.append(int(row))
            columns.append(int(column))

        # check vacancy
        for i in range(len(rows)):
            if desiredRoom.map[rows[i], columns[i]] == 1:
                print("The selected seats have already been reserved! Please try again.")
                return 
        
        # check time slot
        if self.checkTicketTimeSlot(desiredRoom.timeSlot, user.tickets):
            print("The time slot of new reservation has overlap with your precious reservations! Please try again.")
            return
    
        # check balance
        totalPrice = 0
        for i in range(len(rows)):
            totalPrice = totalPrice + desiredRoom.price[rows[i], columns[i]]

        if totalPrice <= user.balance:
            # create a ticket
            ticket = user.reserve(desiredRoom, rows, columns)
            print("Reservation Completed! Your receipts: ")
            ticket.printTicket()
            
            desiredRoom.updateVacancy(rows, columns, 1) # fill the seats in room map
            
            # update business owner revenue
            for business in self.db.businessOwners:
                if business.username == desiredRoom.ownerID:
                    business.updateRevenue(totalPrice)
    
            user.updateBalance(totalPrice, 'withdrawal') # update user balance
        else:
            print(f"You don't have enough balance for this transaction! Please try again. (Total: {totalPrice}, Your current balance: {user.balance})")
            return
    
    def userResellTicket(self, user): # 9. resell a ticket
        user.listAllTickets()
        id = int(input('Which ticket do you want to resell?(enter ticket #) '))
        ticket = user.tickets[id]
        businessOwner = None
        room = None

        for business in self.db.businessOwners:
            if ticket.businessOwnerID == business.username:
                businessOwner = business
                for r in business.rooms:
                    if ticket.roomType == r.roomType:
                        room = r
                        
        discount = float(input("What do you offer as a discount ratio? "))
        resaleTicket = system.Resale(ticket, businessOwner, room, user, discount)
        self.db.resale.append(resaleTicket) # add the ticket to resale list
        user.resellTicket(ticket) # remove the ticket from user's available tickets
        print("Ticket successfully added to resale list! :)")

    def userCancelTicket(self, user): # 10. cancel a ticket
        user.listAllTickets()
        id = int(input('Which ticket do you want to cancel?(enter ticket #) '))
        user.cancelTicket(id, self.db.businessOwners)
        print("Ticket successfully canceled! :)")

    def userUpdateBalance(self, user): # 11. update balance
        print(f"Your current balance is: {user.balance}")
        choice = int(input("What do you want to do with your balance? 1. Deposit 2. Withdrawal \n"))
        match choice:
            case 1:
                amount = float(input("How much do you want to deposit? "))
                user.updateBalance(amount, 'deposit')
            case 2:
                amount = float(input("How much do you want to withdrawal? "))
                user.updateBalance(amount, 'withdrawal')
        print(f"Successful! Your new balance is: {user.balance}")

if __name__ == "__main__":
    seatBookingApp = Application()
    # resale = seatBookingApp.db.resale
    # print(resale[0].printResale())
    # exit()
    seatBookingApp.welcomeMsg(n=5, m=25) #  welcome pattern 
    
    accountType, account = seatBookingApp.signIn() # sign in 

    # each user based on the accountType have different elligibilities    
    while(True):
        print()
        print('What do you wish to do?')
        choice = 0
        if accountType == 1: # admin domain
            choice = int(input('\n'.join(seatBookingApp.eligibility[0])))
            print()
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
            choice = int(input('\n'.join(seatBookingApp.eligibility[1])))
            print()
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
            choice = int(input('\n'.join(seatBookingApp.eligibility[2])))
            print()
            match choice:
                case 1: # sign out
                    seatBookingApp.signOut()
                case 2: # view messages
                    pass
                case 3: # send message
                    pass
                case 4: # list all rooms
                    seatBookingApp.listRooms()
                case 5: # list all resale tickets
                    seatBookingApp.listResaletickets()
                case 6: # list all business owners
                    seatBookingApp.listBusinessOwners()
                case 7: # list alll system users
                    seatBookingApp.listSystemUsers()
                case 8: # reserve a seat
                    seatBookingApp.reserveSeat(account)
                case 9: # resell a ticket
                    seatBookingApp.userResellTicket(account)
                case 10: # cancel a ticket
                    seatBookingApp.userCancelTicket(account) 
                case 11: # exchange a ticket
                    pass
                case 12: # update balance
                    seatBookingApp.userUpdateBalance(account)







    

