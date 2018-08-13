import glob
import json
import math

total_solves = 0
total_time_ms = 0

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
# len() - 1 because the last object is a properties object
for session_nr in range(1, len(json_file) - 1):
	session = json_file["session%s" % session_nr]

	# Don't know why this works or why it's needed
	session = json.loads(session)

	for solve in session:
		total_solves += 1

		# Get the time in milliseconds
		time_ms = solve[0][1]

		total_time_ms += time_ms

# Calculate the time in hours, minutes and seconds
seconds = total_time_ms / 1000
hours = math.floor(seconds / 3600)
minutes = math.floor((seconds / 60) % 60)
seconds = round(seconds % 60)

print(total_solves)
print(hours, minutes, seconds)
