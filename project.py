import presenter.imageToJson as imageToJson
import os, sys
sys.path.append("model")
import model.imageDecoder as imageDecoder
import model.geoCoder as geoCoder
from flask import Flask, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

from pygeocoder import Geocoder
import pandas as pd
import numpy as np
import geocoder as googleGeocode




app = Flask(__name__)
dropzone = Dropzone(app)

#dont forget about bootstrap in layout.html
Bootstrap(app)
# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'
app.config['SECRET_KEY'] = '1234'

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


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

    path1 = 'testData/data0.jpg'
    path2 = 'testData/data2.jpg'
    #image_path_list.append(path1)
   # image_path_list.append(path2)
    #posts = imageToJson.convertImage(image_path_list = image_path_list)


    return render_template('index.html')

@app.route('/map')
def about():
    return render_template('map.html')

@app.route('/results')
def results():
     # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)


    posts= []
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
    
    return render_template('results.html', file_urls=file_urls, posts = posts)

# @app.route("/upload", methods=["POST"])
# def upload():
#     uploaded_files = app.request.files.getlist("file[]")
#     print (uploaded_files)
#     return ""

if __name__ == 'main':
    
    app.debug = True
    app.run(host= '0.0.0.0', port= 5000)