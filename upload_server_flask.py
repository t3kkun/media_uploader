from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import time
import os
import socket

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@app.route('/')
def index():
    media_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mov', '.avi', '.mkv'))]
    return render_template('index.html', media_files=media_files, ip_address=get_local_ip(), port=8000)

@app.route('/upload', methods=['POST'])
def upload_file():
    start_time = time.time()

    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename != '':
        file_path=os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        end_time = time.time()
        transfer_time = end_time - start_time
         # ファイルサイズを取得し、転送速度を計算
        file_size = os.path.getsize(file_path)  # バイト単位
        transfer_speed = (file_size / transfer_time) / 1024  # KB/s

        # 表示: ファイルサイズ(MB)と転送速度(MB/sまたはKB/s)
        file_size_mb = file_size / (1024 * 1024)  # MB単位
        if transfer_speed >= 1024:
            transfer_speed /= 1024  # MB/s に変換
            print(f"File uploaded in {transfer_time:.2f} sec, Size: {file_size_mb:.2f} MB, Speed: {transfer_speed:.2f} MB/s")
        else:
            print(f"File uploaded in {transfer_time:.2f} sec, Size: {file_size_mb:.2f} MB, Speed: {transfer_speed:.2f} KB/s")


    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
