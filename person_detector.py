import grovepi

def isPersonPresent(device_pin, threshold):
    try:
	value = grovepi.ultrasonicRead(device_pin)
	print "Value from sensor is ", value
	if (value < threshold):
		return True
	else:
		return False
    except TypeError:
        print "Error reading ranger sensor..."
	return False
    except IOError:
        print "Error reading ranger sensor..."
	return False
