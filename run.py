from flask import Flask, redirect, url_for, render_template, request,send_file,send_from_directory, safe_join, abort,flash,make_response
import os
import youtube_dl
from urllib.request import urlopen
import re,json,requests,sys,codecs,unicodedata,os
from urllib import parse

app = Flask(__name__)

picFolder = os.path.join('static', 'images')



app.config['UPLOAD_FOLDER'] = picFolder



def getTitle(url):
    url_parsed = parse.urlparse(url)
    qsl = parse.parse_qs(url_parsed.query)
    id=qsl["v"][0]
    title=json.loads(requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={id}&part=snippet,statistics,recordingDetails&key=AIzaSyBmQcXmAHD2h5ZurlNKHvHRwMVHbBQqbvc").content)
    items=title["items"]
    return unicodedata.normalize('NFKD', items[0]["snippet"]["title"]).encode('ascii', 'ignore').decode()
    
def Download(url,_type):
    filename=getTitle(url)
    if _type=="video":
        ydl_opts = {
         'nocheckcertificate': True,
         'outtmpl': f'env/{filename}.%(ext)s',
         'format': 'mp4',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return filename
    elif _type=="audio":
        ydl_opts = {
        'nocheckcertificate': True,
        'format': 'bestaudio/best',
        'outtmpl': f'env/{filename}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filename

@app.route("/")
def home():
    step1 = os.path.join(app.config['UPLOAD_FOLDER'], 'step1.png')
    step2 = os.path.join(app.config['UPLOAD_FOLDER'], 'step2.png')
    step3 = os.path.join(app.config['UPLOAD_FOLDER'], 'step3.png')
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'Logo2.jpg')
    stepimg=os.path.join(app.config['UPLOAD_FOLDER'],'step1img.png')
    stepimg2=os.path.join(app.config['UPLOAD_FOLDER'],'stepimg2.png')
    stepimg3=os.path.join(app.config['UPLOAD_FOLDER'],'stepimg3.png')
    phoneimg=os.path.join(app.config['UPLOAD_FOLDER'],'phoneimgimp.png')
    phoneimg2=os.path.join(app.config['UPLOAD_FOLDER'],'phonestep2.jpeg')
    return render_template("index.html", pic1=step1, pic2=step2, pic3=step3, pic4=logo,pic5=stepimg,pic6=stepimg2,pic7=stepimg3,pic8=phoneimg,pic9=phoneimg2)

@app.route("/index.html")
def arrive():
    step1 = os.path.join(app.config['UPLOAD_FOLDER'], 'step1.png')
    step2 = os.path.join(app.config['UPLOAD_FOLDER'], 'step2.png')
    step3 = os.path.join(app.config['UPLOAD_FOLDER'], 'step3.png')
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'Logo2.jpg')
    stepimg=os.path.join(app.config['UPLOAD_FOLDER'],'step1img.png')
    stepimg2=os.path.join(app.config['UPLOAD_FOLDER'],'stepimg2.png')
    stepimg3=os.path.join(app.config['UPLOAD_FOLDER'],'stepimg3.png')
    phoneimg=os.path.join(app.config['UPLOAD_FOLDER'],'phoneimgimp.png')
    phoneimg2=os.path.join(app.config['UPLOAD_FOLDER'],'phonestep2.jpeg')
    return render_template("index.html", pic1=step1, pic2=step2, pic3=step3, pic4=logo,pic5=stepimg,pic6=stepimg2,pic7=stepimg3,pic8=phoneimg,pic9=phoneimg2)

@app.route("/contact.html",methods=["GET"])
def contact():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'Logo2.jpg')
    return render_template("contact.html",pic4=logo)
    
@app.route("/video",methods=["POST"])
def video():
    dataGet = request.get_json()
    filename=Download(dataGet["url"],_type="video")
    return send_file(filename+".mp4",as_attachment=True)

@app.route("/audio",methods=["POST"])
def audio():
    dataGet = request.get_json()
    filename=Download(dataGet["url"],_type="audio")
    return send_file(filename+".mp3",as_attachment=True)
    
@app.route("/services.html",methods=["GET"])
def services():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'Logo2.jpg')
    return render_template("service.html",pic4=logo)

if __name__ == "__main__":
    app.run(debug=True)
