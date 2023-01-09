import tkinter as tk
from tkinter import *
import customtkinter

import datetime
from datetime import date, time
from datetime import datetime, timedelta

###############################################################################################################################################

# Connect to a database to log the shifts

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="sqluser",
  password="password",
  database="mentors"
)

# print("mydb")

################################################################################################################################################

#### CREATE GUI

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("700x350")
app.title("Mentor Clock in")


# student number id entry

text_entry1 = customtkinter.CTkEntry(master=app, placeholder_text="Student Number", width = 150, justify = CENTER)
text_entry1.place(relx=0.25, rely=0.15, anchor=tk.CENTER)

# Create a dictionary to store the switch variables
switch_vars = {}

# Create a check button to choose which date you want to look at - current date or a given date
use_current_date_var = tk.BooleanVar()
use_current_date_checkbutton = customtkinter.CTkCheckBox(master=app, text="Use current date", variable=use_current_date_var)
use_current_date_checkbutton.place(relx=0.25, rely=0.375, anchor=tk.CENTER)
use_current_date_checkbutton.select()

# Create an input entry function
date_entry = customtkinter.CTkEntry(master=app, placeholder_text="Date (YYYYMMDD)", width = 150, justify = CENTER)
date_entry.place(relx=0.25, rely=0.25, anchor=tk.CENTER)




# create enter button to search for student shift
def student_ID_search():
  # query the database to search for this students shifts this week
  mycursor = mydb.cursor()

  # get the student id from the text entry
  student_ID = text_entry1.get()
  print("Student ID: ", student_ID)

  # welcome message
  name_search = """SELECT prefered_name FROM mentor_information WHERE student_number = '{}'""".format(student_ID)
  mycursor.execute(name_search)
  record1 = mycursor.fetchone()
  name = record1[0]
  print("Hello ", name, "!")

  # Condition so that if the box is not checked you can input the date value in the entry box
  if use_current_date_var.get() == TRUE:
    current_date = date.today()
    current_date = current_date.strftime("%Y%m%d")
  else:
    date_input = date_entry.get()
    current_date = date_input

    print("Date: ", current_date)

  # get the week number to find all of the shifts for the week
  week_number_search = """SELECT * from week_number WHERE Date = '{}'""".format(current_date)
  mycursor.execute(week_number_search)
  record = mycursor.fetchone()

  # selecting column value into variable
  current_week_number = record[1]
  print("Week No: ", current_week_number)

  # find the students shifts for the week
  shift_search = """SELECT * FROM given_shift_log WHERE Student_Number = '{}' AND Week_No = '{}'""".format(student_ID, current_week_number)
  mycursor.execute(shift_search)

  students_shifts_this_week = mycursor.fetchall()

  # prints the number of shifts the student has on the given week
  print("Total number of shifts this week: ", mycursor.rowcount)

  # prints information for each shift the student has in the given week
  for row in students_shifts_this_week:
        print("Student ID = ", row[0], )
        print("Week No = ", row[1])
        print("Date = ", row[2])
        print("Shift Start Time  = ", row[3])
        print("Shift End Time  = ", row[4])
        print("Actual Shift Start Time  = ", row[5])
        print("Actual Shift End Time  = ", row[6], "\n")

  #######
  #DISPLAY ALL OF THE SHIFTS SOMEHOW - ideally just print the above statement into a textbox somehow
  #######

button_search = customtkinter.CTkButton(master=app, text="Search", command=student_ID_search)
button_search.place(relx=0.25, rely=0.5, anchor=tk.CENTER)




#clock in button
def clock_in():
  mycursor = mydb.cursor()

  # get the student id from the text entry
  student_ID = text_entry1.get()

  # get the current date
  current_date = date.today()
  current_date = current_date.strftime("%Y%m%d")

  # Get the current time
  current_time = datetime.now()
  print(current_time)
  
  # clock in can only happen within 15 mineuts of the start time, cant be earlier than 15 mins, and cant be later than 15 mins 
  # hence if I am notified I can edit it manually - otherwise it is taken as absent
  current_time_lower = current_time - timedelta(minutes=15)
  current_time_upper = current_time + timedelta(minutes=15) 

  current_time = current_time.strftime("%H%M%S")
  current_time_lower = current_time_lower.strftime("%H%M%S")
  current_time_upper = current_time_upper.strftime("%H%M%S") 

  # first check to see if they are clocked in or not and then update the database accordingly
  clock_in_check = """SELECT * FROM given_shift_log WHERE Student_Number = '{}' AND Date = '{}' AND Shift_Start BETWEEN '{}' AND '{}'""".format(student_ID, current_date, current_time_lower, current_time_upper)
  mycursor.execute(clock_in_check)
  record2 = mycursor.fetchone()
  clock_in_time = record2[5]
  clock_in_time = datetime.strptime(str(clock_in_time), "%H:%M:%S").time()
  current_time_lower = datetime.strptime(current_time_lower, "%H%M%S").time()
  current_time_upper = datetime.strptime(current_time_upper, "%H%M%S").time()

  # Update the database to import the current time in the shift log table
  # make sure here that if there is already a value entered in the collumn, within the range +- 15min range, it does nothing
  
  def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

  if time_in_range(current_time_lower, current_time_upper, clock_in_time) == TRUE:
    print("Don't worry, you are already clocked in!")
  else:
    clock_in_command = """UPDATE given_shift_log SET Actual_Shift_Start = '{}' WHERE Student_Number = '{}' AND Date = '{}' AND Shift_Start BETWEEN '{}' AND '{}'""".format(current_time, student_ID, current_date, current_time_lower, current_time_upper)
    mycursor.execute(clock_in_command)
    mydb.commit()

    print("You are now clocked in!")

# Use CTkButton instead of tkinter Button
# define the shape and layout of the button
button_c_in = customtkinter.CTkButton(master=app, text="Clock In", command=clock_in)
button_c_in.place(relx=0.25, rely=0.75, anchor=tk.CENTER)




#clock out button
def clock_out():
  mycursor = mydb.cursor()

  # get the student id from the text entry
  student_ID = text_entry1.get()

  # get the current date
  current_date = date.today()
  current_date = current_date.strftime("%Y%m%d")

  # Get the current time
  current_time = datetime.now()

  # Update the database to import the current time in the shift log table
  # clock out can happen anytime within the shift time period (+ 10 mins over) - anytime over the end time will clock out the shift end time not the current time
  # if there is already a valid value in the cell it will overwrite the value up till the cuttoff

  # just realised you can clock out even if you havet clocked in????

  # again first check if there is a value in the cell and what it is
  clock_out_check = """SELECT * FROM given_shift_log WHERE Student_Number = '{}' AND Date = '{}' AND shift_start <= '{}' AND shift_end >= '{}'""".format(student_ID, current_date, current_time, current_time)
  mycursor.execute(clock_out_check)
  record3 = mycursor.fetchone()  
  shift_start_time = record3[3]
  shift_start_time = datetime.strptime(str(shift_start_time), "%H:%M:%S").time()
  shift_end_time = record3[4]
  shift_end_time = datetime.strptime(str(shift_end_time), "%H:%M:%S").time()
  current_time = current_time.time()
  current_time = current_time.strftime("%H%M%S")
  current_time = datetime.strptime(str(current_time), "%H%M%S").time()


  if current_time <= shift_end_time:
    shift_start_time = shift_start_time.strftime("%H%M%S")
    shift_end_time = shift_end_time.strftime("%H%M%S")
    
    clock_out_command1 = """UPDATE given_shift_log SET Actual_Shift_End = '{}' WHERE Student_Number = '{}' AND Date = '{}' AND shift_start <= '{}' AND shift_end >= '{}'""".format(current_time, student_ID, current_date, shift_start_time, shift_start_time)
    mycursor = mydb.cursor()
    mycursor.execute(clock_out_command1)
    mydb.commit()

    print("You are now clocked out, thank you!")
  else:
    shift_start_time = shift_start_time.strftime("%H%M%S")
    shift_end_time = shift_end_time.strftime("%H%M%S")

    clock_out_command2 = """UPDATE given_shift_log SET Actual_Shift_End = '{}' WHERE Student_Number = '{}' AND Date = '{}' AND shift_start <= '{}' AND shift_end >= '{}'""".format(shift_end_time, student_ID, current_date, shift_start_time, shift_start_time)
    mycursor = mydb.cursor()
    mycursor.execute(clock_out_command2)
    mydb.commit()

    print("You are now clocked out, thank you!")

# Use CTkButton instead of tkinter Button
# define the shape and layout of the button
button_c_out = customtkinter.CTkButton(master=app, text="Clock Out", command=clock_out)
button_c_out.place(relx=0.75, rely=0.75, anchor=tk.CENTER)



# run the GUI
app.mainloop()