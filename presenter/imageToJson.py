import os, sys
import model.imageDecoder as imageDecoder


class imageToJson(object):

    def __init__(self):
        super(self)


    jsonFile = list()

    def convertImage(self, image_path_list):
        
        for image_path in image_path_list:
            meta_data =  imageDecoder.ImageMetaData(image_path)
            latlng =meta_data.get_lat_lng()
            jsonFile.append(
            {
                'image' : image_path,
                'latitude' : latlng[1],
                'longitude': latlng[2],
                'zip_code' : '72703',
                'date' : '04/30/2019',
                'time' : '11:45'
                
            })

        return jsonFile