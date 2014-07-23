#

#


def polyPointCollides(poly, point):
	#print(poly, point)
	testX, testY = point
	last = -1
	answer = False
	for now in range(0, len(poly)):
		nowX, nowY = poly[now]
		lastX, lastY = poly[last]
		if (nowY > testY) != (lastY > testY) and (testX < (lastX - nowX) * (testY - nowY)/(lastY - nowY) + nowX):
			answer = not answer
		last += 1
	return answer
