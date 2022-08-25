# attendance

Hello! 

I only had a few requirements for the attendance system: A) It should be stationed at the front door so students will see it as they enter or exit the building, B) should require minimal effort from the students, and C) it needs to be easy to manipulate the data collected.

The solution I came up with involved a raspberry pi (a credit card-sized computer), an LCD screen, a phone keypad, and a few wires.
I chose to utilize a raspberry pi because it allowed most of the requirements to be filled. It would be portable and could be stationed at an entrance/exit, and I could wire a keypad to the computer. It would be easy to use for the student because all they need to do is enter their ID.

I utilized a python library called gspread to read and write data to google spreadsheets. I chose to use gspread because it allowed me to dump data into a worksheet, and create useful calculations and other graphs within the same interface.

The LCD screen will display the date and time until interrupted by the keypad. This is where the student will enter their ID number and press the hashtag button to submit. The system will then look through a spreadsheet of members and their IDs. If it isn't in the list, the screen will notify the user of the invalid input and return to displaying the time and date. If they punch in an ID that is included on the members sheet, the program will then look at the spreadsheet to see if they are already clocked in, and will clock them out if they are clocked in. Otherwise, it will clock the user in. When the user is clocked out, it will add the relevant data to another worksheet to track the history of all shifts clocked. This data can then be used to create useful graphs and visualizations all from within google sheets!

Something else I thought was fun: The HDMI output does not work on this raspberry pi. So all package installations, and code written, EVERYTHING was done via SSH in a command line. It made the development process a little more difficult, but I learned a whole lot more about using a terminal in Linux!
