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
                    ['1. Sign out', '2. View messages', '3. Send message', '4. Define a room', '5. View revenue of the business'], 
                    ['1. Sign out', '2. View messages', '3. Send message', '4. List all rooms', 
                    '5. List all resale tickets', '6. List all business owners', '7. List all system users', '8. Reserve', '9. Buy a resale ticket' ,
                    '10. Resell a ticket', '11. Cancel a ticket', '12. Exchange a ticket', '13. Update Balance']] 

    def welcomeMsg(self, n, m):
        for i in range(1,n,2):
            print ('-'*int((m-i*3)/2)+'.|.'*i+'-'*int((m-i*3)/2))

        print('-'*int((m-7)/2)+'WELCOME'+'-'*int((m-7)/2))

        for i in range(n-2,-1,-2):
            print ('-'*int((m-i*3)/2)+'.|.'*i+'-'*int((m-i*3)/2))
        print()

    # common features between all account types
    def signIn(self): # sign in
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
    
    def signOut(self): # 1. sign out
        seatBookingApp.db.saveDB(self.db)
        print("Thank you for choosing our platform! :)")
        exit()

    def sendMessage(self, account, accountType): # 3. send a message
        senderAccount = ""
        if accountType == 1:
            senderAccount = "Admin:"
        elif accountType == 2:
            senderAccount = "Business Owner:"
        else:
            senderAccount = "User:"

        choice = int(input("What is the account type of the user you wish to communicate with? 1. Admin 2. Business Owner 3. User \n"))
        match choice:
            case 1:
                request = int(input("What is your request? 1. Complaint 2. Support (cancel a ticket)\n"))
                if request == 1:
                    msg = input("What is your message? ")
                    src = senderAccount + account.username # source of message
                    dest = self.db.admin[0].messages # the inbox message of the destination

                    dest[src] = msg # dictionary key = source of msg, dictionary value = message

                    print(f"Message successfully was sent to Admin! :)")
                else:
                    if accountType == 1 or accountType == 2:
                        print("This feature is only for customers.")
                        return
                    # other management stuff that an admin can do
                    if len(account.tickets) == 0:
                        print("Currently you don't have any active ticket! ")
                    account.listAllTickets()
                    cancelID = int(input("Which ticket do you want to be canceled? (enter ticket #): "))
                    src = senderAccount + account.username # source of message
                    dest = self.db.admin[0].messages # the inbox message of the destination
                    msg = "cancel:"+ str(cancelID)
                    dest[src] = msg # dictionary key = source of msg, dictionary value = message
                    print("Message successfully was sent to Admin! :)")
            case 2:
                self.listBusinessOwners()
                id = int(input("Who do you want to send a message? "))
                msg = input("What is your message? ")
                
                src = senderAccount + account.username # source of message
                dest = self.db.businessOwners[id].messages # the inbox message of the destination

                dest[src] = msg # dictionary key = source of msg, dictionary value = message

                print(f"Message successfully was sent to {self.db.businessOwners[id].username}! :)")
            case 3:
                self.listSystemUsers()
                id = int(input("Who do you want to send a message? "))
                msg = input("What is your message? ")
                
                src = senderAccount + account.username # source of message
                dest = self.db.users[id].messages # the inbox message of the destination

                dest[src] = msg # dictionary key = source of msg, dictionary value = message

                print(f"Message successfully was sent to {self.db.users[id].username}! :)")

    def sendToAll(self, user): # notify all users about a new resale ticket
        msg = 'I have added a new ticket to resale list.'
        src = "User:" + user.username # source of message
        for ad in self.db.admin:
            ad.messages[src] = msg
        for business in self.db.businessOwners: # send to all business owners
            business.messages[src] = msg
        for user in self.db.users: # send to all users
            user.messages[src] = msg


    # features for admin
    def adminCancelTicket(self, account):
        account.viewMsg()
        sources = list(account.messages.keys())
        messages = list(account.messages.values())

        for i in range(len(messages)):
            if ":" in messages[i]:
                msgSplit = messages[i].split(":")
                if msgSplit[0] == "cancel":
                    srcSplit = sources[i].split(":")
                    for user in self.db.users:
                        if user.username == srcSplit[1]:
                            user.cancelTicket(int(msgSplit[1]), self.db.businessOwners)
                            del account.messages[sources[i]] # remove the cancel msg
        
        print("All cancel requests was handled! :)")                   

    # features for business owners
    def registerRoom(self, businessOwner):
        print()
        roomType = input('What business do you want this room for (Businees Type)? ')
        size = int(input('What is the desired size of the room? '))
        regularPrice = float(input('What is the regular price for seats? '))
        date = input('What date will this room be available? (example of accepted answer: 2023-02-06) ')
        timeSlot = input('What time slot will this room be available? (example of accepted answer: 12:30-14:05) ')
        businessOwner.defineRoom(roomType, size, regularPrice, date, timeSlot)

    # features for users
    def listRooms(self): # 4. list all rooms
        businessList = self.db.businessOwners
        allRoomObjects = []
        allRooms = []
        header = ["Room #", "Business Owner", "Room Type", "Regular Price", "Date", "Time Slot"]

        i = 0
        for business in businessList:
            for room in business.rooms:
                temp = []
                temp.append(i)
                temp.append(room.ownerID)
                temp.append(room.roomType)
                temp.append(room.regularPrice)
                temp.append(room.date)
                temp.append(room.timeSlot)
                allRooms.append(temp)
                allRoomObjects.append(room)
                i = i + 1
        
        print (tabulate(allRooms, headers=header))

        return allRoomObjects

    def listResaletickets(self): # 5. list all resale tickets
        allResaleTickets = self.db.resale
        if len(allResaleTickets) == 0:
            print("There is no resale offer!")
            return
        for i in range(len(allResaleTickets)):
            print(f'Resale # {i}: ')
            allResaleTickets[i].printResale()
            print()

    def listBusinessOwners(self): # 6. list all business owners
        allBusinessOwners = self.db.businessOwners
        if len(allBusinessOwners) == 0:
            print("There is no registered business owner!")
            return
        info = []
        header = ["Business Owner #", "Name", "Number of registered room"]
        for i in range(len(allBusinessOwners)):
            temp = []
            temp.append(i)
            temp.append(allBusinessOwners[i].username)
            temp.append(len(allBusinessOwners[i].rooms))
            info.append(temp)
        print (tabulate(info, headers=header))

    def listSystemUsers(self): # 7. list all system users
        allusers = self.db.users
        if len(allusers) == 0:
            print("There is no registered user!")
            return
        info = []
        header = ["User #", "Username"]
        for i in range(len(allusers)):
            temp = []
            temp.append(i)
            temp.append(allusers[i].username)
            info.append(temp)
        print (tabulate(info, headers=header))

    def checkDate(self, date1, date2): # same date returns True
        if date1 == date2:
            return True
        return False

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

    def checkTicketTimeSlot(self, newReservationDate, newReservationTime, previousReservations): # check if a new reservation has overlap with previous reservations
        overlap = False
        for pr in previousReservations:
            if self.checkDate(newReservationDate, pr.date): # same date
                if self.checkTimeOverlap(newReservationTime, pr.timeSlot):
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
        if self.checkTicketTimeSlot(desiredRoom.date ,desiredRoom.timeSlot, user.tickets):
            print("The date and time slot of new reservation has overlap with your previous reservations! Please try again.")
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
                    business.updateRevenue(totalPrice, 'deposit')
    
            user.updateBalance(totalPrice, 'withdrawal') # update user balance
        else:
            print(f"You don't have enough balance for this transaction! Please try again. (Total: {totalPrice}, Your current balance: {user.balance})")
            return
    
    def buyResaleTicket(self, user): # 9. buy a resale ticket
        self.listResaletickets()
        id = int(input('Which resale ticket do you want to buy?(enter resale #) '))
        resale = self.db.resale[id]

        # check date and time overlap
        if self.checkTicketTimeSlot(resale.ticket.date ,resale.ticket.timeSlot, user.tickets):
            print("The date and time slot of new reservation has overlap with your previous reservations! Please try again.")
            return

        # check balance
        totalPrice = resale.calculateNewPrice()
        if totalPrice <= user.balance:
            # add resale ticket to buyer ticket list
            resale.ticket.changeID(user.username)
            user.tickets.append(resale.ticket) # add to buyer tickets
            print("Reservation Completed! Your receipts: ")
            resale.ticket.printTicket()
            print(f"Price after discount: {totalPrice}")
            
            resale.seller.updateBalance(totalPrice, 'deposit') # update seller balance
            user.updateBalance(totalPrice, 'withdrawal') # update user balance
            
            self.db.resale.remove(resale) # remove from resale ticket
        else:
            print(f"You don't have enough balance for this transaction! Please try again. (Total: {resale.newPrice}, Your current balance: {user.balance})")
            return


    def userResellTicket(self, user): # 10. resell a ticket
        user.listAllTickets()
        id = int(input('Which ticket do you want to resell?(enter ticket #) '))
        ticket = user.tickets[id]                  
        discount = float(input("What do you offer as a discount ratio? "))
        resaleTicket = system.Resale(ticket, user, discount)
        self.sendToAll(user)
        self.db.resale.append(resaleTicket) # add the ticket to resale list
        user.resellTicket(ticket) # remove the ticket from user's active tickets
        print("Ticket successfully added to resale list! :)")

    def userCancelTicket(self, user): # 11. cancel a ticket
        if len(user.tickets) == 0:
            print("Currently you don't have any active ticket! ")
        user.listAllTickets()
        id = int(input('Which ticket do you want to cancel?(enter ticket #) '))
        user.cancelTicket(id, self.db.businessOwners)
        print("Ticket successfully canceled! :)")

    def exchangeTicekt(self, user): # 12. exchange a ticket
        # first user should choose among him/her tickets
        user.listAllTickets()
        id = int(input('Which ticket do you want to exchange?(enter ticket #) '))
        ticket = user.tickets[id]
        ticketRoom = None

        for business in self.db.businessOwners: # find the room correspond to the ticket
            if business.username == ticket.businessOwnerID:
                for room in business.rooms:
                    if room.roomType == ticket.roomType:
                        ticketRoom = room

        ticketRoom.showMap()

        newRows = []
        newColumns = []
        for i in range(len(ticket.rows)):
            row, column = input(f'Enter the row and column of seat # {i}: (example: 3,4)' ).split(',')
            newRows.append(int(row))
            newColumns.append(int(column))

        # check vacancy
        for i in range(len(newRows)):
            if newRows[i] == ticket.rows[i] and newColumns[i] == ticket.columns[i]: # if the user wants one of its previous seats don't show this error
                continue
            elif ticketRoom.map[newRows[i], newColumns[i]] == 1:
                print("You can't change your ticket with these seats. The selected seats have already been reserved! Please try again.")
                return
        
            
        newTicket = user.reserve(ticketRoom, newRows, newColumns)
        # check price difference and balance
        previousPrice = ticket.calculateTotal()
        newPrice = newTicket.calculateTotal()

        if newPrice == previousPrice:
            print("The ticket changed successfully! Your new receipts: ")
            newTicket.printTicket()
            del user.tickets[id] # replace the new ticket with previous one
        elif newPrice > previousPrice:
            if newPrice-previousPrice <= user.balance:
                print(f"The ticket changed successfully! {newPrice-previousPrice} was withdrawn from your balance. Your receipts: ")
                newTicket.printTicket()
                del user.tickets[id] # replace the new ticket with previous one
                # update business owner revenue
                for business in self.db.businessOwners:
                    if business.username == ticketRoom.ownerID:
                        business.updateRevenue(newPrice-previousPrice, 'deposit')
        
                user.updateBalance(newPrice-previousPrice, 'withdrawal') # update user balance
            else:
                print(f"You don't have enough balance for this transaction! Please try again. (Total: {newPrice-previousPrice}, Your current balance: {user.balance})")
                user.tickets.pop() # new tickets was added, so we need to remove it
                return
        elif newPrice < previousPrice:
            # update business owner revenue
            for business in self.db.businessOwners:
                if business.username == ticketRoom.ownerID:
                    business.updateRevenue(previousPrice-newPrice, 'withdrawal') 
            user.updateBalance(previousPrice-newPrice, 'deposit') # update user balance
            print(f"The ticket changed successfully! {previousPrice-newPrice} was deposited to your balance. Your new receipts: ")
            newTicket.printTicket()
            del user.tickets[id] # replace the new ticket with previous one
        
        ticketRoom.updateVacancy(ticket.rows, ticket.columns, 0) # empty the seats in previous ticket
        ticketRoom.updateVacancy(newRows, newColumns, 1) # fill the seats in room map

    def userUpdateBalance(self, user): # 13. update balance
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
    # tickets = seatBookingApp.db.users[1].tickets
    # print(tickets[0].seatPrice)
    # print(tickets[0].calculateTotal())
    # exit()
    seatBookingApp.welcomeMsg(n=5, m=25) #  welcome pattern 
    
    accountType, account = seatBookingApp.signIn() # sign in 

    # each user based on the accountType have different elligibilities    
    while(True):
        print()
        choice = 0
        if accountType == 1: # admin domain
            print(f'Admin pannel: {account.username}')
            print()
            print('What do you wish to do?')
            choice = int(input('\n'.join(seatBookingApp.eligibility[0])))
            print()
            match choice:
                case 1: # sign out
                    seatBookingApp.signOut()
                case 2: # view messages
                    account.viewMsg()
                case 3: # send message
                    seatBookingApp.sendMessage(account, accountType)
                case 4: # cancel user ticket
                    seatBookingApp.adminCancelTicket(account)
        elif accountType == 2: # business owner domain
            print(f"{account.username}'s profile :)")
            print(f"Revenue: {account.revenue}")
            print()
            print('What do you wish to do?')
            choice = int(input('\n'.join(seatBookingApp.eligibility[1])))
            print()
            match choice:
                case 1: # sign out
                    seatBookingApp.signOut()
                case 2: # view messages
                    account.viewMsg()
                case 3: # send message
                    seatBookingApp.sendMessage(account, accountType)
                case 4: # define a new room
                    seatBookingApp.registerRoom(account)
                case 5: # view the revenue
                    account.viewRevenue()
        else: # user domain
            print(f"{account.username}'s profile :)")
            print(f"balance: {account.balance}")
            print()
            print('What do you wish to do?')
            choice = int(input('\n'.join(seatBookingApp.eligibility[2])))
            print()
            match choice:
                case 1: # sign out
                    seatBookingApp.signOut()
                case 2: # view messages
                    account.viewMsg()
                case 3: # send message
                    seatBookingApp.sendMessage(account, accountType)
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
                case 9: # buy a resale ticket
                    seatBookingApp.buyResaleTicket(account)
                case 10: # resell a ticket
                    seatBookingApp.userResellTicket(account)
                case 11: # cancel a ticket
                    seatBookingApp.userCancelTicket(account) 
                case 12: # exchange a ticket
                    seatBookingApp.exchangeTicekt(account)
                case 13: # update balance
                    seatBookingApp.userUpdateBalance(account)







    

