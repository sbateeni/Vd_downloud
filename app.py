from flask import Flask, render_template, request, send_file, jsonify
import os
import yt_dlp
import browser_cookie3

app = Flask(__name__)

# مجلد الحفظ الافتراضي
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_media(url, format_type, save_path):
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'cookiesfrombrowser': ('chrome',),  # يمكنك تغيير المتصفح حسب الحاجة
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
        save_path = DOWNLOAD_FOLDER

        try:
            # الحصول على ملفات تعريف الارتباط من المتصفح
            cookies = browser_cookie3.load('youtube.com')
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
        
        ydl_opts = {
            'format': 'best',
            'cookiesfrombrowser': ('chrome',),
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({'message': 'تم التحميل بنجاح', 'save_path': DOWNLOAD_FOLDER})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
