import pickle
import getpass

import database
import system
        

if __name__ == "__main__":
    # load database ---------------------------------------
    try:
        db = pickle.load(open("database_file.pickle", "rb"))
    except (OSError, IOError) as e:
        db = database.Database()
    # load database ---------------------------------------

    #  welcome pattern ---------------------------------------
    n, m = 5, 25
    for i in range(1,n,2):
      print ('-'*int((m-i*3)/2)+'.|.'*i+'-'*int((m-i*3)/2))

    print('-'*int((m-7)/2)+'WELCOME'+'-'*int((m-7)/2))

    for i in range(n-2,-1,-2):
      print ('-'*int((m-i*3)/2)+'.|.'*i+'-'*int((m-i*3)/2))
    #  welcome pattern ---------------------------------------
    
    # log in ---------------------------------------
    print()
    
    accountType = int(input('Which one of these options best describe you? 1.Admin 2.Business Owner 3.User\n'))
    username = input('Please enter your username:\n')
    password = getpass.getpass()

    newAccount = db.exist(accountType, username) # check if the user already exists or no
    if newAccount == True:
        if accountType == 1:
            newUser = system.Admin(username, password)
            db.addAccount(accountType, newUser)
        elif accountType == 2:
            newUser = system.BusinessOwner(username, password)
            db.addAccount(accountType, newUser)
        elif accountType == 3:
            balance = input("What is your initial balance?\n")
            newUser = system.User(username, password, balance)
            db.addAccount(accountType, newUser)
    else:
        authentication = db.checkPassword(accountType, username, password)
        if authentication == False:
            print('your username and password do not match! Please try again.')
            exit()
    # log in ---------------------------------------

    

