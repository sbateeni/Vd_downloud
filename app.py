from flask import Flask, render_template, request, send_file, jsonify
import os
import yt_dlp
import browser_cookie3
import tkinter as tk
from tkinter import filedialog

app = Flask(__name__)

# مجلد الحفظ الافتراضي
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_save_path():
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    folder_path = filedialog.askdirectory()
    return folder_path

def download_media(url, format_type, save_path):
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'quiet': False
    }

    if format_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif format_type == 'video':
        ydl_opts.update({'format': 'best'})

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        format_type = request.form['format']
        save_path = request.form.get('save_path', DOWNLOAD_FOLDER)

        try:
            download_media(url, format_type, save_path)
            return f"✅ التحميل تم بنجاح! الملفات محفوظة في: {save_path}"
        except Exception as e:
            return f"❌ خطأ أثناء التحميل: {str(e)}"

    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL مطلوب'}), 400

        # الحصول على ملفات تعريف الارتباط من المتصفح
        cookies = browser_cookie3.load('youtube.com')
        cookie_dict = {cookie.name: cookie.value for cookie in cookies}

        # السماح للمستخدم باختيار مسار الحفظ
        save_path = get_save_path()
        if not save_path:
            return jsonify({'error': 'لم يتم اختيار مسار الحفظ'}), 400

        ydl_opts = {
            'format': 'best',
            'cookiesfrombrowser': ('chrome',),  # يمكنك تغيير المتصفح حسب الحاجة
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({'message': 'تم التحميل بنجاح', 'save_path': save_path})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
