from flask import Flask, render_template, request, send_file
import os
import yt_dlp

app = Flask(__name__)

# مجلد الحفظ الافتراضي
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

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

if __name__ == '__main__':
    app.run(debug=True)
