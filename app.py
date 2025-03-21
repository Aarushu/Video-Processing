import os
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST', 'GET'])
def upload_video():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('static/', filename))
    # Code for Project 265 Grayscale start here
    source = cv2.VideoCapture('static/' + filename)
    frame_width = int(source.get(3))
    frame_height = int(source.get(4))
    size = (frame_width, frame_height)
    result = cv2.VideoWriter('static/' + 'blackandwhite.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, size, 0)
    try:
        while True:
            status, frame_image = source.read()
            gray = cv2.cvtColor(frame_image, cv2.COLOR_RGB2GRAY)
            result.write(gray)
            video_file = 'blackandwhite.mp4'
    except:
        print('Completed reading all the Frames from the Video')
    # Code for Project 265 end here

    return render_template('upload.html', filename=video_file)


# Code for Project 265 download function starts here
@app.route('/download', methods=['GET', 'POST'])
def download_file():
    converted_video_path = "static/blackandwhite.mp4"
    return send_file(converted_video_path, as_attachment=True)


# Code for Project 265 download function ends here


@app.route('/display/<filename>', methods=['GET', 'POST'])
def display_video(filename):
    return redirect(url_for('static', filename=filename))


if __name__ == "__main__":
    app.run(debug=True)