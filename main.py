import sys
import os
from skimage import io
from matplotlib import pyplot as plt
import numpy as np
from crop_manual import *
import datetime
from PIL import Image
from QtUi import *

# Ui for the parameters
app = QtWidgets.QApplication(sys.argv)
set_param = MainWindow()
app.exec_()
if not set_param.data:
    sys.exit()
lambda_low = int(set_param.data[1])
lambda_step = int(set_param.data[2])
lambda_high = int(set_param.data[3])
experience_name = set_param.data[0]
exposure = int(set_param.data[4])
gain = int(set_param.data[5])
slit_ent = int(set_param.data[6])
slit_exi = int(set_param.data[7])
firstW = int(set_param.data[8])

# Setting up the directory for the photos
directory = set_param.working_dir +'/'

# Part for data acquisition with Mono and Cam
# If there is already photos to process, we dont acquire data
if not set_param.crop.checkState():
    # TODO: Mettre le code pour la caméra et le monochromateur ici
    print("_________ACQUISITION_EN_COURS_________")
    directory = directory + 'ZonesNano/'


# Variables
avg = []
wavelength = []
input_loc = directory+str(firstW)+'.tiff'
output_loc = directory+'cropped/'+'crop_'+str(firstW)+'nm.png'

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

# For loop that will do the same cropping for each photos
for i in set_param.wavelengths:
    input_loc = directory + str(i) + '.tiff'
    output_loc = directory + 'cropped/' + 'crop_' + str(i) + 'nm.png'

    im = Image.open(input_loc)
    im = im.crop((left, upper, right, lower))
    im.save(output_loc)

    image = io.imread(output_loc)
    avg.append(np.average(image))
    wavelength.append(i)

# Create the graphic et show it
plt.scatter(wavelength, avg, marker='o')
plt.title(experience_name+" ("+str(datetime.date.today())+")")
plt.grid()
plt.xlabel("Wavelength (nm)")
plt.ylabel("Intensity")
plt.savefig(directory+'graph.png')
plt.show()


