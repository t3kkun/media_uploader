from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import time
import socket
import qrcode
from werkzeug.utils import secure_filename
from yt_dlp import YoutubeDL
import threading
import subprocess

app = Flask(__name__)

# ダウンロード関数（スレッド用）
def run_download(url):
    options = {
        'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }
    try:
        with YoutubeDL(options) as ydl:
            print(f"[INFO] Downloading: {url}")
            ydl.download([url])
            print("[INFO] Download complete.")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")

def generate_qr(ip,port):
    url = f"http://{ip}:{port}"
    qr = qrcode.make(url)
    qr_path = os.path.join(BASE_DIR, "static", "qr.png")
    qr.save(qr_path)

# アップロードフォルダの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

texts = []

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
        print("[ERROR] 'file' field not found in request.")
        return redirect(url_for('index'))

    files = request.files.getlist('file')

    if not files or files[0].filename == '':
        print("[INFO] No file selected.")
        return redirect(url_for('index'))

    print(f"[INFO] Received {len(files)} file(s).")

    for file in files:
        if file and file.filename:
            filename = get_unique_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            start_time = time.perf_counter()
            file.save(path)
            end_time = time.perf_counter()

            transfer_time = end_time - start_time
            file_size_mb = os.path.getsize(path) / (1024 * 1024)

            print(f"[UPLOAD] {filename}")
            print(f"[INFO] Size: {file_size_mb:.2f} MB")
            print(f"[INFO] Time: {transfer_time:.4f} sec")

    return redirect(url_for('index'))

@app.route('/download_video', methods=['POST'])
def download_video_endpoint():
    url = request.form.get('video_url')
    if not url:
        print("[ERROR] No URL provided")
        return redirect(url_for('index'))

    thread = threading.Thread(target=run_download, args=(url,))
    thread.start()

    print(f"[INFO] Download started in background: {url}")
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))  # Google DNSへダミー接続
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

def list_media_files():
    return os.listdir(app.config['UPLOAD_FOLDER'])

def save_text(text):
    texts.append(text)
    if len(texts) > 5:
        texts.pop(0)

def get_unique_filename(original_filename):
    base, ext = os.path.splitext(secure_filename(original_filename))
    counter = 1
    new_filename = f"{base}{ext}"
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    ip = get_ip_address()
    generate_qr(ip, 8000)
    app.run(debug=False, host='0.0.0.0', port=8000)
