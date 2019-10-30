from flask import Flask, render_template
from flask_bootstrap import Bootstrap

create_app()

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

posts = [
    {
        'image' : 'image_path',
        'latitude' : '000.001',
        'longitude': '000.2',
        'zip_code' : '72703',
        'date' : '04/30/2019',
        'time' : '11:45'
        
    },
    {
        'image' : 'image_path2',
        'latitude' : '000.003',
        'longitude': '000.4',
        'zip_code' : '72701',
        'date' : '05/10/2019',
        'time' : '04:12'
        
    }
]
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/map')
def about():
    return render_template('map.html')

# @app.route("/upload", methods=["POST"])
# def upload():
#     uploaded_files = app.request.files.getlist("file[]")
#     print (uploaded_files)
#     return ""

if __name__ == 'main':
    app.debug = True
    app.run(host= '0.0.0.0', port= 5000)