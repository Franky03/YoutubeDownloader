from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_bootstrap import Bootstrap
import pytube
from io import BytesIO

app= Flask(__name__)
Bootstrap(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method== 'POST':
        link= request.form['link']
        if request.form.get("mp3", False):
            try:
                buffer= BytesIO()
                url= pytube.YouTube(link)
                video= url.streams.get_audio_only()
                video.stream_to_buffer(buffer)
                buffer.seek(0)
                
                return send_file(buffer, as_attachment=True, download_name='music.mp3', mimetype='audio/mp3')
            except:
                raise Exception("Unfortunately the music was not downloaded, please try again.")

        elif request.form.get("mp4", False):
            try:
                buffer= BytesIO()
                url= pytube.YouTube(link)
                video= url.streams.get_highest_resolution()
                video.stream_to_buffer(buffer)
                buffer.seek(0)
                return send_file(buffer, as_attachment=True, download_name='video.mp4', mimetype='video')
            except:
                raise Exception("Unfortunately the video was not downloaded, please try again.")

    return render_template('index.html')
    
if __name__== "__main__":
    app.run(debug=True)