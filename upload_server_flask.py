from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import time
import socket

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

texts = []
media_files = []

print('-----------------------------------------------------')
print('ファイルと文字列受け入れ開始中 停止するには【CTRL + C】\nStarting server.. To interrupt, press 【CTRL + C】\n\n公衆無線LANは使わずインタネット共有を活用してください\nDo not use free Wifi, use Mobile Hotspot instead.')
print('-----------------------------------------------------')

@app.route('/')
def index():
    ip_address = get_ip_address()
    media_files = list_media_files()
    return render_template('index.html', texts=texts, media_files=media_files, ip_address=ip_address, port=8000)

@app.route('/post_text', methods=['POST'])
def post_text():
    text = request.form['text']
    save_text(text)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename != '':
        start_time = time.time()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        end_time = time.time()
        transfer_time = end_time - start_time
        file_size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)) / (1024 * 1024)  # MB
        calculate_transfer_speed(file_size, transfer_time)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def get_ip_address():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def list_media_files():
    return os.listdir(UPLOAD_FOLDER)

def save_text(text):
    texts.append(text)
    if len(texts) > 5:
        texts.pop(0)

def calculate_transfer_speed(file_size, transfer_time):
    speed = file_size / transfer_time
    print(f"Transfer speed: {speed:.2f} MBps ({speed * 8:.2f} Mbps)")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=False, host='0.0.0.0')
