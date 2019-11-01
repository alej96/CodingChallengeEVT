# Load packages
from pygeocoder import Geocoder
import pandas as pd
import numpy as np

class Geocoder(object):


    
    def geoCodeFromLatLng(self, lat , lng):
        
        geo_results = Geocoder.reverse_geocode(lat, lng)

        city = geo_results.city
        zip_code = geo_results.zip_code
        return  city
