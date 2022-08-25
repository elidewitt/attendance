from rpi_lcd import LCD
lcd = LCD() # Create LCD

lcd.text("Booting...", 1)
print("Booting...")

import RPi.GPIO as GPIO # GPIO
GPIO.setmode(GPIO.BOARD)
from time import sleep, gmtime, strftime # Time
from datetime import datetime

import gspread # Google Spreadsheets
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/home/pi/Attendance/creds.json", scope)
client = gspread.authorize(creds)

# try to define spreadsheets until no error is occuring
spreadsheet = None
while spreadsheet is None:
	try:
		spreadsheet = client.open("Attendance") # Open the spreadsheet
	except:
		pass

members = spreadsheet.worksheet("Members") # Setup member sheet
clock = spreadsheet.worksheet("Clock")  # Setup clock sheet
history = spreadsheet.worksheet("History") # Setup history sheet

MATRIX = [ ["1", "2", "3"],
           ["4", "5", "6"],
           ["7", "8", "9"],
           ["*", "0", "#"] ]

MESSAGE = ""

# correlate GPIO.BOARD pins to the rows and cols of keypad
ROW = [31, 40, 38, 35]
COL = [33, 29, 37]

# setup rows and cols
for j in range(len(COL)):
	GPIO.setup(COL[j], GPIO.OUT)
	GPIO.output(COL[j], 1)
for i in range(len(ROW)):
	GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

def punch(id):
	# test to find if the id punched is valid
	try:
		userCell = members.find(id)
		user = members.cell(userCell.row, 2).value
		print(user)
	except:
		return False

	# look on live clock to see if user is already punched in
	try:
		cell = clock.find(user)
		history.append_row([user, clock.cell(cell.row, 2).value, strftime("%m/%d/%Y %H:%M:%S", gmtime())])
		clock.delete_rows(cell.row)
		lcd.clear()
		lcd.text(user, 1)
		lcd.text("Clocked Out!", 2)
		print("Clocked Out!")
		sleep(3)
	except:
		clock.append_row([user, strftime("%m/%d/%Y %H:%M:%S", gmtime())])
		lcd.clear()
		lcd.text(user, 1)
		lcd.text("Clocked In!", 2)
		print("Clocked In!")
		sleep(3)
	return True

# show time on lcd screen function
currentTime, currentDate = None, None
def showTime():
	global currentTime, currentDate

	if currentTime != datetime.now().strftime("%H:%M:%S"):
		currentTime = datetime.now().strftime("%H:%M:%S")
		lcd.text(currentTime, 2)
		print(currentTime)
	if currentDate != datetime.now().strftime("%b %d, %Y"):
		currentDate = datetime.now().strftime("%b %d, %Y")
		lcd.text(currentDate, 1)

# run until keyboard interrupt

lcd.text("Boot Successful", 1)
print("Boot Successful")

sleep(2)
lcd.clear()

active = False
try:
	while (True):

		if (not active):
			showTime()

			# check for input to switch mode
			for j in range(len(COL)):
				GPIO.output(COL[j], 0)

				for i in range(len(ROW)):
					if GPIO.input(ROW[i]) == 0:
						active = True
		else:
			lcd.clear()
			lcd.text(MESSAGE, 1)

			# loop though all colums turning them off and check the row output
			for j in range(len(COL)):
				GPIO.output(COL[j], 0)

				for i in range(len(ROW)):
					if GPIO.input(ROW[i]) == 0:

						if MATRIX[i][j].isnumeric():
							MESSAGE += MATRIX[i][j]
							print(MESSAGE)
						elif MATRIX[i][j] == "*":
							MESSAGE = MESSAGE[:-1]
						elif MATRIX[i][j] == "#":
							if (not punch(MESSAGE)):
								lcd.text("Invalid ID", 2)
								sleep(3)

							MESSAGE = ""
							lcd.clear()
							currentTime, currentDate = None, None
							active = False
						else:
							print(MATRIX[i][j], " doesn't have a function")
						while (GPIO.input(ROW[i]) == 0):
							pass
				GPIO.output(COL[j], 1)

		sleep(0.15)

except KeyboardInterrupt:
	lcd.clear()
	GPIO.cleanup()
finally:
	lcd.clear()
	GPIO.cleanup()
