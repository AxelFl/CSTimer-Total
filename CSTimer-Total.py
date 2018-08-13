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

		session_stats[session_nr - 1][0] += time_ms

properties = json.loads(json_file["properties"])
session_data = json.loads(properties["sessionData"])
for session_nr in range(1, len(session_data) + 1):
	current_session = session_data[str(session_nr)]
	session_name = current_session["name"]
	session_stats[session_nr - 1][2] = session_name

# Calculate the time in hours, minutes and seconds
seconds = total_time_ms / 1000
hours = math.floor(seconds / 3600)
minutes = math.floor((seconds / 60) % 60)
seconds = round(seconds % 60)

print(session_stats)
print(total_solves)
print(hours, minutes, seconds)
