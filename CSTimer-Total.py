import glob
import json

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

