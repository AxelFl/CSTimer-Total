import glob
import json

# Finds all .txt files and if only 1 is present save that file name, else exit the program
file_names = glob.glob("*.txt")
if len(file_names) != 1:
	print("Please have 1 .txt file in this directory")
	quit()
else:
	file_name = file_names[0]

# Opens the found file, if not a valid JSON file, ask the user to supply a valid file
try:
	with open(file_names, "r") as file:
		text = file.read()
except TypeError:
	print("Please put a CSTimer .txt file in the directory")
	quit()

# Make read string into a JSON file
json_file = json.loads(text)

