import numpy as np

processing_time = np.genfromtxt('Development/Processing_time.csv')

meanProcess = np.mean(processing_time)

print("Mean Processing Time: ",meanProcess)

print("Mean FPS: ", 1/meanProcess)