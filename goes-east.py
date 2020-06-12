import requests
import os
from bs4 import BeautifulSoup
import cv2
from skimage import io
import ctypes

# To do:
# - Librarify.
# - Install script

# INSTRUCTIONS
#
# Use this at your own risk, I'm not responsible for any damages on your end.
# I also don't intend to actively develop this, but might help in some situations.
#
# SCRIPT SETUP
# Set destination location for image file below
# Select desired image below
# Select desired image resolution below
#
# AUTOMATIC WALLPAPER UPDATES
# Open Task Scheduler (Windows search)
# Create Task...
# General Tab
# 	Give name and description (not important, be creative)
# 	Change User or Group -> Advanced
#		Find Now
#		Find and select your user account, then click OK (formatted as "Username (email)" sometimes)
# 	Run only when user is logged on
# Triggers
#	Begin the task: At log on
#	Specific user: Yourself
#	Repeat task every: 10 minutes for a duration of: Indefinitely
# Actions
#	Action: Start a program
#	Program/script: python.exe (or pythonw.exe to run in background)
#		To find exe folder, open Python, import sys, print(sys.executable)
#	Add arguments: 'C:/Users/<user>/<wherever you want>/goes-east.py'

# Destination for image. File is overwritten each time to save disk space.
file = 'C:/Users/<user>/<wherever you want>/earth.jpg'

# Select an image by uncommenting it. Preview them here: https://www.star.nesdis.noaa.gov/GOES/GOES16_FullDisk.php
targetImage = 'GEOCOLOR'			# True color daytime, multispectral IR at night
#targetImage = 'EXTENT'				# Geostationary Lightning Mapper
#targetImage = 'AirMass'			# RGB composite based on the data from IR and WV
#targetImage = 'Sandwich'			# Multi-spectral blend combines IR band 13 with visual band 3
#targetImage = 'DMW'				# Derived Motion Winds
#targetImage = 'DayCloudPhase'		# RGB used to evaluate the phase of cooling cloud tops
#targetImage = 'NightMicrophysics'	# RGB used to distinguish clouds from fog
#targetImage = '01'					# 0.47um Blue - Visible
#targetImage = '02'					# 0.64um Red - Visible
#targetImage = '03'					# 0.86um Veggie - Near IR
#targetImage = '04'					# 1.37um Cirrus - Near IR
#targetImage = '05'					# 1.6um Snow-Ice - Near IR
#targetImage = '06'					# 2.2um Cloud Particle - Near IR
#targetImage = '07'					# 3.9um Shortwave Window - IR
#targetImage = '08'					# 6.2um Upper-Level Water Vapor - IR
#targetImage = '09'					# 6.9um Mid-Level Water Vapor - IR
#targetImage = '10'					# 7.3um Lower-Level- Water Vapor - IR
#targetImage = '11'					# 8.4um Cloud Top - IR
#targetImage = '12'					# 9.6um Ozone - IR
#targetImage = '13'					# 10.3um Clean Longwave Window - IR
#targetImage = '14'					# 11.2um Longwave Window - IR
#targetImage = '15'					# 12.3um Dirty Longwave Window - IR
#targetImage = '16'					# 13.3um CO2 Longwave - IR

# Select a resolution for your monitor. Recommend to pick one higher than your monitor's vertical resolution
#targetResolution = '339x339.jpg'
#targetResolution = '678x678.jpg'
targetResolution = '1808x1808.jpg'
#targetResolution = '5424x5424.jpg'
#targetResolution = '10848x10848.jpg'

def get_image_link():
    page = requests.get('https://www.star.nesdis.noaa.gov/GOES/GOES16_FullDisk.php')
    raw_html = page.content
    html = BeautifulSoup(raw_html, "html5lib")

    # all the image links have one of these classes
    links = html.select('a.FB,a.FBNZ')
    image_link = None

    for l in links:
        link_target = l.get_attribute_list('href')[0]
        if targetImage in link_target:
            # print(link_target)
            if (link_target.endswith(targetResolution)):
                image_link = link_target
    return image_link

# taken from "https://stackoverflow.com/questions/16694907/"
# "how-to-download-large-file-in-python-with-requests-py"

def download_file(url, file):
    # print("Downloading image from {}".format(url))
    r = requests.get(url, stream=True)
    with open(file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush() # commented by recommendation from J.F.Sebastian
    return file

def is_valid_image(file):
    try:
        img = io.imread(file)
    except:
        return False
    return True

def setWallpaper():
	# Sets desktop wallpaper for Windows
	SPI_SET_WALLPAPER = 20
	ctypes.windll.user32.SystemParametersInfoW(SPI_SET_WALLPAPER, 0, file, 0)

def fetch_and_set():
	# Get latest image
	os.remove(file)
	link = get_image_link()
	download_file(link, file)
	
	# Add border to image - not really a fan since it makes the image smaller
	'''img = cv2.imread(file)
	assert is_valid_image(file)
	height = img.shape[0]
	img = cv2.copyMakeBorder(img, int(0.03 * height), 0, 0, 0, cv2.BORDER_CONSTANT)
	cv2.imwrite(file, img)'''
	
	# Set as desktop wallpaper
	setWallpaper()

fetch_and_set()