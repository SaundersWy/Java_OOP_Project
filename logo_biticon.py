# Curtis Saunders, Final Project, CIS 345, 10:30 AM
import cv2
from PIL import Image

filename = 'knives.png'

'''
im = Image.open(filename)

# sharp = im.filter(ImageFilter.SHARPEN)
# sharp.show()
small = im.resize((16, 16))
small.save('bit_icon.ico')

'''

im = Image.open(filename)

# sharp = im.filter(ImageFilter.SHARPEN)
# sharp.show()
logo = im.resize((128, 128))
logo.save('logo.png')
