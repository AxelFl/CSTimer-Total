import glob
import json
import math

total_solves = 0
total_time_ms = 0

# This is where the stats of individual sessions will go
session_stats = []

# Finds all .txt files and if only 1 is present save that file name, else exit the program
file_names = glob.glob("*.txt")
if len(file_names) != 1:
	print("Please have 1 .txt file in this directory")
	exit()
else:
	file_name = file_names[0]

# Loads the found file
with open(file_name, "r") as file:
	text = file.read()

# Make read string into a JSON file, if it is an invalid file, ask the user for a good file and exit the program
try:
	json_file = json.loads(text)
except json.JSONDecodeError:
	print("Please supply a valid CSTimer file")
	exit()

# Go through all the sessions in the file,
# Range should be + 1 to reach the last one, because it is not inclusive
# But since we have an extra object with session no modification is required
for session_nr in range(1, len(json_file)):
	session = json_file["session%s" % session_nr]

	# Don't know why this works or why it's needed
	session = json.loads(session)

	# First index is time and second is number of solves
	# Third is the name of the session which will be filled in later
	session_stats.append([0, 0, None])

	for solve in session:
		total_solves += 1
		session_stats[session_nr - 1][1] += 1

		# Get the time in milliseconds
		time_ms = solve[0][1]

		total_time_ms += time_ms

		# Add the time to that sessions stats
		session_stats[session_nr - 1][0] += time_ms

# Load into the part where the session names are
properties = json.loads(json_file["properties"])
session_data = json.loads(properties["sessionData"])
# For all the session add the sessions name to session_stats
for session_nr in range(1, len(session_data) + 1):
	current_session = session_data[str(session_nr)]
	session_name = current_session["name"]
	session_stats[session_nr - 1][2] = session_name


# Calculate the time in hours, minutes and seconds
# Function because it is used multiple times
# Returns a tuple with the times
def get_time(ms):
	# Everything gets floored because it gets covered by the lower unit
	# Seconds are so small and just gets rounded anyways
	# First and second is obvious
	seconds = ms / 1000
	hours = math.floor(seconds / 3600)
	# Gives me total minutes mod 60 because the rest are taken by hours
	minutes = math.floor((seconds / 60) % 60)
	# Takes the number of seconds mod 60 because of the minutes
	seconds = round(seconds % 60)
	return hours, minutes, seconds


# Find the most used session in time
highest_time = 0
for session in session_stats:
	if session[0] > highest_time:
		most_used_time = session
		highest_time = session[0]

# Find the most used session in number of solves
highest_solves = 0
for session in session_stats:
	if session[1] > highest_solves:
		most_used_solves = session
		highest_solves = session[1]

# Print out all the special statistics at the end
print("You have spent a total of %s hours, %s minutes and %s seconds of solving in CSTimer" % get_time(total_time_ms))
print("With a total of %s solves" % total_solves)

# if the number of hours is 0, 0 evaluates to False in python, print the time without hours
if not get_time((total_time_ms/total_solves))[0]:
	# [1:] Gets the tuple without the hour
	print("Average time: %s minutes and %s seconds" % get_time((total_time_ms/total_solves))[1:])
else:
	print("Average time: %s hours, %s minutes and %s seconds" % get_time((total_time_ms/total_solves)))


print("")
print("The session you have spent the most time solving with is %s" % most_used_time[2])
print("In that session you spent a total of %s hours, %s minutes and %s seconds" % get_time(most_used_time[0]))
print("With a total of %s solves" % most_used_time[1])

# if the number of hours is 0, 0 evaluates to False in python, print the time without hours
if not get_time(most_used_time[0]/most_used_time[1])[0]:
	# [1:] Gets the tuple without the hour
	print("Average time: %s minutes and %s seconds" % get_time((most_used_time[0]/most_used_time[1]))[1:])
else:
	print("Average time: %s hours, %s minutes and %s seconds" % get_time((most_used_time[0]/most_used_time[1])))


print("")
print("The session you have the most solves with is %s" % most_used_solves[2])
print("In that session you spent a total of %s hours, %s minutes and %s seconds" % get_time(most_used_solves[0]))
print("With a total of %s solves" % most_used_solves[1])

# if the number of hours is 0, 0 evaluates to False in python, print the time without hours
if not get_time(most_used_solves[0]/most_used_solves[1])[0]:
	# [1:] Gets the tuple without the hour
	print("Average time: %s minutes and %s seconds" % get_time(most_used_solves[0]/most_used_solves[1])[1:])
else:
	print("Average time: %s hours, %s minutes and %s seconds" % get_time((most_used_solves[0]/most_used_solves[1])))


# Prints out all of the stats at the end
for session in session_stats:
	print("")
	print(session[2])
	print("%s hours, %s minutes and %s seconds" % get_time(session[0]))
	print("%s solves" % session[1])
	# If there are no solves, there is no average
	if not session[1]:
		continue
	if not get_time(session[0]/session[1])[0]:
		print("Average time: %s minutes and %s seconds" % get_time(session[0]/session[1])[1:])
	else:
		print("Average time: %s hours, %s minutes and %s seconds" % get_time(session[0]/session[1]))

input()
