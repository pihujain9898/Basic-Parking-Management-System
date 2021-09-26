# First of all we import the necesaary modules
# Then that we connet our program to MYSQL
# After it we create the sub-functions which will be called by the main function 
# After that we create the main function thorugh which our program runs
# In last after the welcome line we calls our main function 

#importing statements
import mysql.connector as msc
import pandas as pd
import numpy as np
import time
from datetime import datetime
from fpdf import FPDF
import os
import matplotlib.pyplot as plt
import calendar

# Here we used try-except conditional statements
try:
    # We ask user his/her mysql password for making connection of program to mysql
    mysql_paswrd = input("Enter password of your MySQL: ")

    # Here we tried to connect in existing parking database in this try loop if it was created previously
    mysql_obj = msc.connect(host = "localhost",
                            user = "root",
                            passwd = mysql_paswrd,
                            database = "Parking_Management",
                            charset = 'utf8')
    mysql_crsr = mysql_obj.cursor()
    mysql_crsr.execute("use Parking_Management;")
except:
    # If database would not found then we create a new database in this except loop    
    mysql_obj = msc.connect(host = "localhost",
                            user = "root",
                            passwd = mysql_paswrd,
                            database = "mysql",
                            charset = 'utf8')
    mysql_crsr = mysql_obj.cursor()
    mysql_crsr.execute("create database Parking_Management;")
    mysql_crsr.execute("use Parking_Management;")

    # Here we create parking-management table
    mysql_crsr.execute("create table Parking_Table(Parking_ID int Primary Key, Vechile_No varchar(16),Vechile_Type varchar(20), Vechile_Entery_Time datetime, Vechile_Checkout_Time datetime, Net_Amount int, Paid_Amount int ,Rest_Amount int, Status varchar(12));")
    # We add some dumy data here
    mysql_crsr.execute("insert into Parking_Table values(1, 'RJ14 DN 0031', 'Scooty', '2021-01-06 10:20:20', '2021-01-06 18:40:50', 20, 20, 0, 'Gone');")
    mysql_crsr.execute("insert into Parking_Table values(2, 'RJ14 CN 7816', 'Car', '2021-01-07 10:37:23', '2021-01-07 17:21:28', 40, 40, 0, 'Gone');")
    mysql_crsr.execute("insert into Parking_Table values(3, 'RJ14 PQ 5674', 'Bike', '2021-01-08 13:27:53', '2021-01-08 19:47:49', 20, 20, 0, 'Gone');")
    mysql_crsr.execute("insert into Parking_Table values(4, 'RJ14 TY 2211', 'Bike', '2021-01-09 17:14:34', '2021-01-09 20:33:28', 20, 20, 0, 'Gone');")
    mysql_crsr.execute("insert into Parking_Table values(5, 'RJ14 LH 8853', 'Car', '2021-01-09 22:02:05', '2021-01-09 23:39:02', 40, 40, 0, 'Gone');")
    mysql_crsr.execute("insert into Parking_Table values(6, 'RJ14 ZX 9423', 'Auto', '2021-01-10 08:44:57', '2021-01-10 13:21:31', 30, 30, 0, 'Gone');")
    mysql_crsr.execute("insert into Parking_Table values(7, 'RJ14 OI 2153', 'Car', '2021-01-10 13:32:08', '0000-00-00 00:00:00', 40, 40, 0, 'Parked');")
    mysql_crsr.execute("insert into Parking_Table values(8, 'RJ14 BV 8977', 'Scooty', '2021-01-10 17:53:31', '2021-01-10 18:55:36', 20, 20, 0, 'Gone');")
    mysql_crsr.execute("insert into Parking_Table values(9, 'RJ14 QW 8079', 'Scooty', '2021-01-11 18:21:12', '0000-00-00 00:00:00', 20, 20, 0, 'Parked');")
    mysql_crsr.execute("insert into Parking_Table values(10, 'RJ14 SA 4355', 'Bike', '2021-01-12 21:20:23', '0000-00-00 00:00:00', 20, 20, 0, 'Parked');")

    # Here we create vechile-categories table
    mysql_crsr.execute("create table Vechile_Categories(Vechile_ID int Primary Key, Vechile_Name varchar(20),Vechile_Spacing varchar(14), Vechile_Charge int);")
    # Inserting data in vechile-category table
    mysql_crsr.execute("insert into Vechile_Categories values(1, 'Puck', '2-Wheeler', 20),(2, 'Scooty', '2-Wheeler', 20),(3, 'Scooter', '2-Wheeler', 20),(4, 'Bike', '2-Wheeler', 20),(5, 'Hand-Cart', '3-Wheeler', 30),(6, 'E-Rickshawa', '3-Wheeler', 30),(7, 'Auto', '3-Wheeler', 30),(8, 'Car', '4-Wheeler', 40),(9, 'Mini_Truck', '4-Wheeler', 40);")
    #For saving all the above creation/changes in MySQL permanently
    mysql_obj.commit()

# This is sub-function of main_function() that do task 1 of main function i.e. showing records
def display_records():
    print("\nParking Records....\n")
    # Here we call data from mysql server
    mysql_crsr.execute("select * from Parking_Table;")
    parking_table_data = mysql_crsr.fetchall()

    # converting the data into tabluar form to represent
    parking_table = pd.DataFrame(parking_table_data, columns=['Parking_ID', 'Vechile_No', 'Vechile_Type', 'Vechile_Entery_Time', 'Vechile_Checkout_Time', 'Net_Amount', 'Paid_Amount', 'Rest_Amount', 'Status'])
    print(parking_table)

    # This code will do next function after stoping for 1 second
    time.sleep(1)
    print("\n")

    # After completion of this function we call the main function in it so that it will run unbreakably
    main_function()

# This is sub-function of main_function() that do task 2 of main function i.e. adding new vechile in parking area
def vechile_entery():
    print("\nVechile Entery....\n")
    # Here first we genrate the new entery data values like parking id, current date-time, etc

    # This data helps us to genrate the next Parking_ID for the upcoming vechile
    mysql_crsr.execute("select * from Parking_Table;")
    parking_table_data = mysql_crsr.fetchall()
    Parking_ID = parking_table_data[-1][0] + 1
    
    # This genrates curent date and time
    Vechile_Entery_Time = datetime.now()

    # We can't decide checkout time now so we inserted not a time value in it
    Vechile_Checkout_Time = '0000-00-00 00:00:00'

    # As the vechile came for parking so we put its status as parked
    Status = 'Parked'

    # Here we ask necessary details from user like which type of vechile his\her customer wants to park
    # We extract the data from vechile_categories table
    mysql_crsr.execute("select * from Vechile_Categories;")
    vechile_categories_data = mysql_crsr.fetchall()
    vechile_categories = pd.DataFrame(vechile_categories_data, columns=['Vechile_ID', 'Vechile_Name', 'Vechile_Spacing', 'Vechile_Charge'])
    print(vechile_categories)
    vechile_id = input('\nEnter vechile ID type from above table or press 0 to exit : ')

    # Here we used conditional statements by which if user insert wrong number than he/she will get notify about it
    if vechile_id == '0':
        # This is case when user wants to exit 
        print('\nExit successfully\n')
        main_function()
    elif vechile_id in np.array(np.arange(1, len(vechile_categories)+1), dtype='U'):
        # Here we extract the vechile type and minimum parking charge for user's customer by his choice
        Net_Amount =  vechile_categories_data[int(vechile_id)-1][3]
        Vechile_Type = vechile_categories_data[int(vechile_id)-1][1]
    else:
        # This is case when user puts wrong value
        print('\nPlease enter valid number\n')
        time.sleep(1)
        # By calling this function, we restared this function itself again 
        vechile_entery()
    
    # Here we ask user to insert the vechile number(vechile no. plate number)
    Vechile_No = input('Enter Vechile Number : ')

    # We notify the user that his/her customer should pay this much amount
    print('Customer should pay the minimum charge i.e. valid for 24hr of {} is {}rs'.format(Vechile_Type,Net_Amount))

    # As we took minimum charge here so paid amount is also equal to the minimum charge
    Paid_Amount = Net_Amount

    # There will be no dues this time as we assumed that customer would take checkout in minimum charge time
    Rest_Amount =  0

    # Here we inserted the data in MySQL server 
    inserting_str = "insert into Parking_Table values({}, '{}', '{}', '{}', '{}', {}, {}, {}, '{}');".format(Parking_ID,Vechile_No,Vechile_Type,Vechile_Entery_Time,Vechile_Checkout_Time, Net_Amount, Paid_Amount, Rest_Amount, Status)
    mysql_crsr.execute(inserting_str)
    mysql_obj.commit()  

    #Parking Recipt Genration in PDF Format
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial" ,size=20)

    # This cell method will create the line in pdf page
    pdf.cell(0,25,"PARKING MANAGEMENT SYSTEM", ln=1, align="C")
    pdf.cell(0,4,"Parking Recipt", ln=1, align="C")
    pdf.set_font("Arial","B" ,size=18)
    pdf.cell(0,40,f"PARKING ID : {Parking_ID}",ln=1,align="L")

    # This code changes the font aspects from here that will we written in PDF
    pdf.set_font("Arial", size=16)
    pdf.cell(0,0,f"Vechile Type : {Vechile_Type}",ln=0,align="L") 
    pdf.cell(0,0,f"Date : {datetime.strftime(Vechile_Entery_Time,'%d-%m-%y')}",ln=1,align="R")
    pdf.cell(0,20,f"Vechile Number : {Vechile_No}",ln=0,align="L") 
    pdf.cell(0,20,f"Time : {datetime.strftime(Vechile_Entery_Time,'%H:%M:%S')}",ln=1,align="R")
    pdf.cell(0,20,f"Minimum Charge : Rs {Net_Amount}",ln=0,align="L")

    # This code make a pdf in the same loaction of program 
    pdf.output(f"Parking_Recipt{Parking_ID}.pdf")

    # This code access the pdf file in computer location that we made above and open it
    os.startfile(f"Parking_Recipt{Parking_ID}.pdf")
    
    print("\n")
    main_function()

# This is sub-function of main_function() that do task 2 of main function i.e. adding new vechile in parking area
def vechile_checkout():
    print("\nVechile Checkout....\n")

    # Here we calls the parked vechils data from mysql
    mysql_crsr.execute("select * from Parking_Table;")
    parking_table_data = mysql_crsr.fetchall()

    # Here customer have to show his recipt of and tell his parking id to user through which user procced the checkout
    parking_no = input("Enter a parking ID of vechile or press 0 to exit: ")

    # This loop verfies that the inserted number is integer or not
    try:
        parking_no = int(parking_no)
    except:
        print("\nPlease enter valid parking ID\n")
        time.sleep(1)
        vechile_checkout()

    if parking_no == 0:
        # This is case when user wants to exit 
        print('\nExit successfully\n')
        main_function()
    elif parking_no in list(range(1,len(parking_table_data)+1)):
        # This loop verify the parking_id in our data
        mysql_crsr.execute("select * from Parking_Table where Parking_ID = {};".format(parking_no))
        parking_table_data = mysql_crsr.fetchall()
        vechile_Status = parking_table_data[0][-1]

        # In these loops we verfiy the inserted data
        if vechile_Status == 'Gone':
            # This is condition when anyone inserts that parking id whose status is of gone
            print("\nThis vechile took checkout already\n")
        elif vechile_Status == 'Parked' :
            # Here we extract no. of days from given time that how much time vechile is parked
            entery_time = parking_table_data[0][3]
            exit_time = datetime.now()
            staying_time = exit_time - entery_time
            staying_time = staying_time.days

            #We create this for those vechiles that checkout same day as they parked
            if staying_time == 0:
                staying_time = staying_time + 1
            else:
                pass

            # Here we genrate the charges
            minimum_charge = parking_table_data[0][5]
            Paid_Amount = parking_table_data[0][6]
            vechile_no = parking_table_data[0][1]
            total_amount = minimum_charge*staying_time
            left_Amount = total_amount - Paid_Amount
            
            # Here we show user that how much he/she should charge his/her customer
            print("\nAmount to be paid is ", left_Amount, "rs by the owner of vechile",vechile_no,"\n")
            print("1. Amount paid successfully\n2. Cancel the operation")

            # Though this loop we get that customer payed charge or not
            procced = input("\nYour choice: ")
            if procced == '1':
                # Chechout process is done here
                print("\nCheckout successfully\n")
                
                # Here we genrate left amount as 0 and update the data in our mysql server
                left_Amount = 0
                mysql_crsr.execute(f"update parking_table set Vechile_Checkout_Time = '{exit_time}' where Parking_ID = {parking_no};")
                mysql_crsr.execute(f"update parking_table set Rest_Amount = {left_Amount} where Parking_ID = {parking_no};")
                mysql_crsr.execute(f"update parking_table set Net_Amount = {total_amount} where Parking_ID = {parking_no};")
                mysql_crsr.execute(f"update parking_table set Paid_Amount = {total_amount} where Parking_ID = {parking_no};")
                mysql_crsr.execute(f"update parking_table set Status = 'Gone' where Parking_ID = {parking_no};")
                mysql_obj.commit()
            elif procced == '2':
                # Condition when user wants to cancel the operation
                print("\nOperation Cancelled Successfully\n")
                time.sleep(1)
                main_function()
            else:
                # Condition when user type something different from options
                print("\nSomething went wrong so operation cancelled\n")
                time.sleep(1)
                main_function()
        else:
            pass
    else:
        # Condition when user entered that parking ID which is not existed in our data
        print("\nPlease enter valid parking ID\n")
        time.sleep(1)
        vechile_checkout()
    main_function()

# This is sub-function of main_function() that do task 4 of main function i.e. representing data through graph
def graphical_analysis():
    print('\nDay-wise earning analysis : \n')

    # Here we extract data from mysql which will be shown graphically
    mysql_crsr.execute("select sum(Paid_Amount),date(vechile_entery_time) from parking_table group by date(vechile_entery_time);")
    graph_data = mysql_crsr.fetchall()

    # Here we put this data into list form so that we can make graph from them
    x_items = []
    y_items = []
    day_numbers = []
    for i in range(len(graph_data)):
        x_items.append(int(graph_data[i][0]))
        y_items.append(calendar.day_name[datetime.weekday(graph_data[i][1])])
        day_numbers.append(datetime.weekday(graph_data[i][1]))
    
    # Here we arranged the data in proper way
    statstics_table = pd.DataFrame({'Day_Number':day_numbers,'Day':y_items, 'Earning':x_items,})
    statstics_table = statstics_table.sort_values('Day_Number')
    
    # Here we show analysis in tabular form
    print(statstics_table.iloc[0:,1:])

    # here we plot the graph
    plt.bar(statstics_table['Day'],statstics_table['Earning'])
    plt.xlabel("Days")
    plt.ylabel("Earning(Rs)")
    plt.title("Day Wise Earning")

    #Here we show analysis in graphical form 
    plt.show()

    print("\n")
    main_function()

#This is main function that runs the whole program expect connectivity code
# In this we simply used a conditional loop that runs our program as per user choice
# In this conditional loop we recalls the sub functions as per user's choice
def main_function():
    print("1. View parking records\n2. Vechile Entery\n3. Vechile Checkout\n4. Day-Wise Analysis\n0. Quit")
    choice = input("\nEnter your choice : ")
    if choice == '0':
        print('Shuting Down...')
        time.sleep(1)
    elif choice == '1':
        display_records()
    elif choice == '2':
        vechile_entery()
    elif choice == '3':
        vechile_checkout()
    elif choice == '4':
        graphical_analysis()
    else:
        print("\nPlease enter valid number\n")
        main_function()

#For displaying welcome line for 1s
print("\nWelcome to Parking Management System\n\n")
time.sleep(1)

# This function call runs our program as we diffined it above 
main_function()