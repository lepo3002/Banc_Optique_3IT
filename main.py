import sys
from skimage import io
from matplotlib import pyplot as plt
import numpy as np
from crop_manual import *
import datetime
from PIL import Image
from QtUi import *

# Variables
avg = []
wavelength = []

# Ui for the parameters
app = QtWidgets.QApplication(sys.argv)
set_param = MainWindow()
app.exec_()
lambda_low = int(set_param.data[1])
lambda_step = int(set_param.data[2])
lambda_high = int(set_param.data[3])
experience_name = set_param.data[0]
exposure = int(set_param.data[4])
gain = int(set_param.data[5])
slit_ent = int(set_param.data[6])
slit_exi = int(set_param.data[7])

# Part for data acquisition with Mono and Cam
# If there is already photos to process, we dont acquire data
if not set_param.crop.checkState():
    # TODO: Mettre le code pour la caméra et le monochromateur ici
    print("_________ACQUISITION_EN_COURS_________")

# Setting up the directory for the photos
directory = 'ZonesNano/'
input_loc = directory+'Camera_'+str(lambda_low)+'nm.tiff'
output_loc = directory+'cropped/'+'crop_'+str(lambda_low)+'nm.png'

# Setup and opening of the selection window
screen, px = setup(input_loc)
left, upper, right, lower = SelectionWindow(screen, px)

# Readjust the coordinates if they are reversed
if right < left:
    left, right = right, left
if lower < upper:
    lower, upper = upper, lower

# Doing the cropping
im = Image.open(input_loc)
im = im.crop((left, upper, right, lower))

# Exit the selection window
pygame.display.quit()

# Save the image in the output location
im.save(output_loc)

# Calculate the average of the pixels values and save it
image = io.imread(output_loc)
avg.append(np.average(image))
wavelength.append(lambda_low)

# For loop that will do the same cropping for each photos
for i in range(((lambda_high-lambda_low)//lambda_step)):
    input_loc = directory+'Camera_'+str(lambda_low+(lambda_step*i))+'nm.tiff'
    output_loc = directory+'cropped/'+'crop_'+str(lambda_low+(lambda_step*i))+'nm.tiff'

    im = Image.open(input_loc)
    im = im.crop((left, upper, right, lower))
    im.save(output_loc)

    image = io.imread(output_loc)
    avg.append(np.average(image))
    wavelength.append(lambda_low+lambda_step*i)

# Create the graphic et show it
plt.scatter(wavelength, avg, marker='o')
plt.title(experience_name+" ("+str(datetime.date.today())+")")
plt.grid()
plt.xlabel("Wavelength (nm)")
plt.ylabel("Intensity")
plt.show()
# plt.savefig(path+'Graphique.png')


