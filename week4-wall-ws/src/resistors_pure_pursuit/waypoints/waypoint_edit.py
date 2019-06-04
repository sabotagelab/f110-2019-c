file = open('kelley.csv', 'r')
newFile = open('test2.csv', 'a')

x = 0
for line in file:
	coord = line.split(",")
#	if (coord[0] >= 10 and coord[0] < 20):
	#if(x > 999 and x <= 1180):
	#	coord[0] = float(coord[0])
	#	coord[0] -= 0.3
	#if(x > 1044 and x <= 1135):
	#	coord[0] = float(coord[0])	
	#	coord[0] -= 0.1
	newLine = str(coord[0]) + "," + str(coord[1]) + "," + str(coord[2]) + "\n"
	newFile.write(newLine)	
	x += 1


file.close()
newFiles.close()
