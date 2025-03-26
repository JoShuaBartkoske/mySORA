'''
Creating a SORA script to run and save all of the occultation predictions for a dark run
Author: Joshua T Bartkoske
DoC: March 25, 2025
'''

## SORA package
from sora import Occultation, Body, Star, LightCurve, Observer
from sora.prediction import prediction

## Other main packages
from astropy.time import Time
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.table import Table
from astropy.io import ascii

## Usual packages
import numpy as np
import matplotlib.pylab as pl
import os
import time

# define your Dark Run
DR = 6

# set up a log file
import logging
path = "/home/joshuabartkoske/mySORA/"

# Check whether the specified path exists or not
isExist = os.path.exists(path+"log")
if isExist == False:
    os.mkdir(path+"log")

logfilename = path + f"log/dr{DR}_predictions.log"
isFile = os.path.isfile(logfilename)
if isFile == True:
    print("Found log file already exists. Deleting log file...")
    os.remove(logfilename)
    print("Log file deleted")
logging.basicConfig(filename=logfilename, level=logging.INFO)

time_begun = time.ctime(time.time())
logging.info(f"Time begun: {time_begun}")

# Now to have a list of bodies to search for an occultation:
## we will use every named body
MPC_bodies = np.arange(4,7) # use numbers instead of names. 773917 is the max as of right now
print(MPC_bodies[-1])
logging.info(f"Final numbered body is: {MPC_bodies[-1]}")

# define our "observers", one for each telescope in VERITAS
T1 = Observer(name='Telescope 1', lat='31 40 29.5572', lon='-110 57 3.456', height =1268)
T2 = Observer(name='Telescope 2', lat='31 40 28.2756', lon='-110 57 6.8976', height =1260)
T3 = Observer(name='Telescope 3', lat='31 40 31.8936', lon='-110 57 7.4844', height =1267)
T4 = Observer(name='Telescope 4', lat='31 40 30.2556', lon='-110 57 9.9756', height =1265)

# then for every MPC body, we run the entire predictive software
# But first we set up a Boolean for when we get a first succesful prediction
occultation_found = False

for n in MPC_bodies:
    asteroid = Body(name=f'{n}')
    print(f"MPC Body {asteroid.shortname}")
    print(f"Occultation Found Boolean is: {occultation_found}")
    if occultation_found:
        new_pred = prediction(body=asteroid, time_beg='2025-01-18',time_end='2025-02-07',mag_lim={'B': 13.5}, reference_center=T1)
        new_pred.add_column([int(n)], name="MPC Number")
        for i in range(len(new_pred)):
            pred.add_row([new_pred[i][col] for col in new_pred.colnames])
            new_pred_epoch = Time(new_pred["Epoch"][i])
            pred['ICRS Star Coord at Epoch'] = SkyCoord(new_pred['ICRS Star Coord at Epoch'][i], unit=(u.hourangle, u.deg))
            pred['Geocentric Object Position'] = SkyCoord(new_pred['Geocentric Object Position'][i], unit=(u.hourangle, u.deg))
            pred["Epoch"][-1] = new_pred_epoch

    else:
        pred = prediction(body=asteroid, time_beg='2025-01-18',time_end='2025-02-07',mag_lim={'B': 13.5}, reference_center=T1)

        if pred["Epoch"] != None:
            occultation_found = True
            pred.add_column([int(n)], name="MPC Number")
        else:
            print(f"No occultation found for {n}")
            logging.info(f"No occultation found for {n}")



# save the file as a .dat file
ascii.write(pred, f'{path}/predictions/DR{DR}_predictions.dat', overwrite=True) 

# save when the full prediction finished
time_finished = time.ctime(time.time())
logging.info(f"Time finished: {time_finished}")

