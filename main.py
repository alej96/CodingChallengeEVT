import os, sys
sys.path.append("model")
import imageDecoder
from flask import Flask

class main:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



#app= Flask(__name__)



path_name = 'testData/data2.jpg'
meta_data =  imageDecoder.ImageMetaData(path_name)
latlng =meta_data.get_lat_lng()
print("lat long:  ")
print( latlng)

print("==========================================")
exif_data = meta_data.get_exif_data()
print(exif_data)