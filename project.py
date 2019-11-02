import os, sys
sys.path.append("model")
import presenter.imageToJson as imageToJson
sys.path.append("model")
import model.imageDecoder as imageDecoder
sys.path.append("model")
import model.geoCoder as geoCoder
from flask import Flask, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

from pygeocoder import Geocoder
import pandas as pd
import numpy as np
import geocoder as googleGeocode
from flask_googlemaps import GoogleMaps as GoogleMaps
from flask_googlemaps import Map, icons



app = Flask(__name__)
dropzone = Dropzone(app)



# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'
app.config['SECRET_KEY'] = '1234'
# set key as configin the app
app.config['GOOGLEMAPS_KEY'] = 'AIzaSyDbqMl372WFLuNl3P-OzksyAWqw5njSHSU'

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

Bootstrap(app)
GoogleMaps(app)

@app.route('/',  methods=['GET', 'POST'])
@app.route('/index',  methods=['GET', 'POST'])
def index():
    
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']


    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            print (file.filename)

            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename    
            )
            # append image urls
            file_urls.append(photos.url(filename))

            print("file URL")
            print(file_urls)
        session['file_urls'] = file_urls
        return "uploading..."


    #posts = imageToJson.convertImage(image_path_list = image_path_list)


    return render_template('index.html')

@app.route('/results',methods = ['POST', 'GET'])
def results():
     # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)

  # set session for image data
    if "imgData" not in session:
        session['imgData'] = []
    # list to hold the data object
    posts = session['imgData']
   # posts= []
    image_path_list = []
    #Extract data from images
    if request.method == 'GET':

        for image_path in file_urls:
            meta_data = imageDecoder.ImageMetaData(image_path)
            latlng =meta_data.get_lat_lng()
            
            print("===============latlong======================")
            print(latlng)
            lat = latlng[0]
            lng = latlng[1]
            print(lat)
            print (lng)
          

            # googleGeo = googleGeocode.google([lat, lng], method = 'reverse')
            # city2 = googleGeo.city
            #print(city2)
            #check if it have latlng data
            if lat is not None or lng is not None:
               
              #revecse geocode lat,long
                geocoder = Geocoder(api_key='AIzaSyDbqMl372WFLuNl3P-OzksyAWqw5njSHSU')
                geo_results = geocoder.reverse_geocode(lat, lng)
            #   zip_code = imageDecoder.geoCodeFromLatLng(48.8566, 2.3522)
            #  zip_code = latlng[2]
                zip_code = geo_results.postal_code
                city = geo_results.city
                country = geo_results.country
                print(geo_results)
               
                posts.append(
                {
                    'image' : image_path,
                    'latitude' : lat,
                    'longitude': lng,
                    'zip_code' : zip_code,
                    'city' : city,
                    'country' : country
                    
                })
            else:
                posts.append(
                {
                    'image' : image_path,
                    'latitude' : 'Unknown',
                    'longitude': 'Unknown',
                    'zip_code' : 'Unknown',
                    'city' : 'Unknown',
                    'country' : 'Unknown'
                    
                })
            #save data into sesion
            session['imgData'] = posts

    #redirect to maps page
    if request.method == 'POST':
        return redirect(url_for('map', posts))
    
    return render_template('results.html', file_urls=file_urls, posts = posts)

@app.route('/map',methods = ['POST', 'GET'])
def map():


    # redirect to results if no images to display
    if "imgData" not in session or session['imgData'] == []:
        return redirect(url_for('results'))
        
    # set the file_urls and remove the session variable
    imgDataList = session['imgData']
    session.pop('imgData', None)

    print(imgDataList)

#    googleMap = googleMapReator()

    if request.method == 'POST':
       # result = request.form
       print("post method!!!!!!!!!!!!!!!!!")

    mapData = []
    latitude = 0
    longitude = 0
    image_path = ''
    for imgData in imgDataList:
        latitude = imgData['latitude']
        longitude = imgData['longitude']
        image_path = imgData['image']
        city = imgData['city']
        zip_code = imgData['zip_code']
        country = imgData['country']
        
        mapData.append({
                'icon': icons.dots.blue,
                'lat': latitude,
                'lng': longitude,
                'infobox': (
                    "<p>Image taken at<b style='color:#c2c5cc double;'> " +
                         city + ", " + country + " </b>!</p>"                   
                    "<img style='height: 50px' src= " + image_path + ">"     
                )
            } ) 
        
    # creating a map in the view
    trdmap = Map(
        identifier="trdmap",
        varname="trdmap",
        lat= latitude,
        lng= longitude,
        markers=mapData       
        
    )
    return render_template('map.html',trdmap=trdmap)


if __name__ == 'main':
    
    app.debug = True
    app.run(host= '0.0.0.0', port= 5000)