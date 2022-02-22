from skimage import io
from matplotlib import pyplot as plt
import numpy as np
from crop_manual import *
import datetime
from PIL import Image, ImageDraw, ImageFont
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
directory = set_param.working_dir + '\\'
font = ImageFont.truetype('arial.ttf', 20)

# Part for data acquisition with Mono and Cam
# If there is already photos to process, we dont acquire data
if not set_param.crop.isChecked():
    # TODO: Mettre le code pour la caméra et le monochromateur ici
    print("_________ACQUISITION_EN_COURS_________")
    directory = directory + 'ZonesNano/'

# If we have more than 1 zones to crop
if set_param.multiple.isChecked():
    nbZones = int(set_param.data[9])
else:
    nbZones = 1

for j in range(nbZones):
    # Variables
    j = j+1
    avg = []
    wavelength = []

    # Directories
    input_loc = directory+str(firstW)+'.tiff'
    try:
        os.mkdir(directory + 'cropped')
    except FileExistsError:
        pass
    output_loc = directory+'cropped\\'+'crop_'+str(firstW)+'nm.png'

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

    # Multiple zones identification on separate image
    if set_param.multiple.isChecked():
        # Naming according to zones
        experience_name_zone = experience_name+' Zone '+str(chr(j+64))
        graph = 'graph(zone_'+str(chr(j+64))+').png'
        if j == 1:
            zones = Image.open(input_loc)
            zones = zones.convert("RGB")
            Z1 = ImageDraw.Draw(zones)
            Z1.text((left, upper), chr(64+j), font=font, fill='red')
            zones.save(directory+'ZonesIdentification.png')
        else:
            zones = Image.open(directory+'ZonesIdentification.png')
            Z1 = ImageDraw.Draw(zones)
            Z1.text((left, upper), chr(64+j), font=font, fill='red')
            zones.save(directory + 'ZonesIdentification.png')
    else:
        # Default name
        graph = 'graph_'+str(datetime.date.today())+'.png'
        experience_name_zone = experience_name

    # For loop that will do the same cropping for each photos
    for i in set_param.wavelengths:
        input_loc = directory + str(i) + '.tiff'
        output_loc = directory + 'cropped\\' + 'crop_' + str(i) + 'nm.png'

        im = Image.open(input_loc)
        im = im.crop((left, upper, right, lower))
        im.save(output_loc)

        image = io.imread(output_loc)
        avg.append(np.average(image))
        wavelength.append(i)

    # Create the graphic
    plt.plot(wavelength, avg, marker='o', label=experience_name_zone)
    plt.title(experience_name+" ("+str(datetime.date.today())+")")
    plt.grid()
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.legend(loc='upper right')

# Save and show the graph
plt.savefig(directory+graph)
plt.show()
