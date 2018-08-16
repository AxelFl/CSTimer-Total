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
	solve_str = file.read()
solves = solve_str.split("\n")

solves.remove(solves[0])
solves.remove(solves[len(solves) - 1])
session_stats = {}

for solve in solves:
	solve = solve.split(";")
	solve[0] = solve[0].replace('"', '')
	solve[1] = solve[1].replace('"', '')
	solve[2] = solve[2].replace('"', '')

	if solve[0] + " " + solve[1] not in session_stats:
		session_stats[solve[0] + " " + solve[1]] = [0, 0, solve[0] + " " + solve[1]]
	session_stats[solve[0] + " " + solve[1]][1] += 1
	session_stats[solve[0] + " " + solve[1]][0] += int(solve[2])

	total_solves += 1
	total_time_ms += int(solve[2])


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
for key, session in session_stats.items():
	if session[0] > highest_time:
		most_used_time = session
		highest_time = session[0]

# Find the most used session in number of solves
highest_solves = 0
for key, session in session_stats.items():
	if session[1] > highest_solves:
		most_used_solves = session
		highest_solves = session[1]

# Print out all the special statistics at the end
print("You have spent a total of %s hours, %s minutes and %s seconds of solving in Twisty Timer" % get_time(total_time_ms))
print("With a total of %s solves" % total_solves)

# if the number of hours is 0, 0 evaluates to False in python, print the time without hours
if not get_time((total_time_ms / total_solves))[0]:
	# [1:] Gets the tuple without the hour
	print("Average time: %s minutes and %s seconds" % get_time((total_time_ms / total_solves))[1:])
else:
	print("Average time: %s hours, %s minutes and %s seconds" % get_time((total_time_ms / total_solves)))

print("")
print("The session you have spent the most time solving with is %s" % most_used_time[2])
print("In that session you spent a total of %s hours, %s minutes and %s seconds" % get_time(most_used_time[0]))
print("With a total of %s solves" % most_used_time[1])

# if the number of hours is 0, 0 evaluates to False in python, print the time without hours
if not get_time(most_used_time[0] / most_used_time[1])[0]:
	# [1:] Gets the tuple without the hour
	print("Average time: %s minutes and %s seconds" % get_time((most_used_time[0] / most_used_time[1]))[1:])
else:
	print("Average time: %s hours, %s minutes and %s seconds" % get_time((most_used_time[0] / most_used_time[1])))

print("")
print("The session you have the most solves with is %s" % most_used_solves[2])
print("In that session you spent a total of %s hours, %s minutes and %s seconds" % get_time(most_used_solves[0]))
print("With a total of %s solves" % most_used_solves[1])

# if the number of hours is 0, 0 evaluates to False in python, print the time without hours
if not get_time(most_used_solves[0] / most_used_solves[1])[0]:
	# [1:] Gets the tuple without the hour
	print("Average time: %s minutes and %s seconds" % get_time(most_used_solves[0] / most_used_solves[1])[1:])
else:
	print("Average time: %s hours, %s minutes and %s seconds" % get_time((most_used_solves[0] / most_used_solves[1])))

# Prints out all of the stats at the end
for key, session in session_stats.items():
	print("")
	print(session[2])
	print("%s hours, %s minutes and %s seconds" % get_time(session[0]))
	print("%s solves" % session[1])
	# If there are no solves, there is no average
	if not session[1]:
		continue
	if not get_time(session[0] / session[1])[0]:
		print("Average time: %s minutes and %s seconds" % get_time(session[0] / session[1])[1:])
	else:
		print("Average time: %s hours, %s minutes and %s seconds" % get_time(session[0] / session[1]))

input()
