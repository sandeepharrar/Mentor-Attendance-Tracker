import tkinter as tk
from tkinter import *
import customtkinter
import pandas as pd

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

# import xlxs file from teams to get the this weeks shifts to update the database
# download the file from teams and store it in the same place each week/day - depending on how often you update the shifts

df = pd.read_excel(r'C:\Users\sande\Documents\_Uni Job\Mentors\Attendance Code\excel sheets\Timetable.xlsx', sheet_name='Week begining 9th Jan TEST')
print(df)



def Monday():
    # dasflkaj;f

def Tuesday():
    # jfdlfs

def Wednesday():
    # fjdsjfdld

def Thursday():
    # kfdkalf

def Friday():
    # fjsafjl