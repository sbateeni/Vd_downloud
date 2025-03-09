from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
import yt_dlp
import os

class DownloaderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # إنشاء المجلد عند بدء التطبيق
        self.base_path = os.path.join(os.getenv('EXTERNAL_STORAGE', '/storage/emulated/0'), 'YTDownloader')
        self.download_path = os.path.join(self.base_path, 'Downloads')
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.download_path, exist_ok=True)

    def build(self):
        # إنشاء التخطيط الرئيسي
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # إضافة عنوان التطبيق
        title_label = Label(
            text='تحميل الفيديو',
            size_hint_y=None,
            height=50,
            font_size='20sp',
            bold=True
        )
        layout.add_widget(title_label)

        # إنشاء حقل URL
        self.url_input = TextInput(
            hint_text='أدخل رابط الفيديو',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.url_input)

        # إنشاء قائمة اختيار النوع
        self.format_spinner = Spinner(
            text='فيديو',
            values=('فيديو', 'صوت فقط'),
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.format_spinner)

        # زر التحميل
        download_button = Button(
            text='تحميل',
            size_hint_y=None,
            height=50,
            background_color=(1, 0, 0, 1)  # لون أحمر
        )
        download_button.bind(on_press=self.download_media)
        layout.add_widget(download_button)

        # نص الحالة
        self.status_label = Label(
            text=f'مسار التحميل:\n{self.download_path}',
            size_hint_y=None,
            height=70,
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        layout.add_widget(self.status_label)

        return layout

    def download_media(self, instance):
        url = self.url_input.text
        if not url:
            self.status_label.text = 'الرجاء إدخال رابط'
            return

        try:
            # إعدادات التحميل
            ydl_opts = {
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'progress': True
            }

            # إذا تم اختيار تحميل الصوت فقط
            if self.format_spinner.text == 'صوت فقط':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'best'
                })

            self.status_label.text = 'جاري التحميل...'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.status_label.text = f'تم التحميل بنجاح!\nتم الحفظ في: {self.download_path}'
            self.url_input.text = ''  # مسح الرابط بعد التحميل

        except Exception as e:
            self.status_label.text = f'خطأ: {str(e)}'

if __name__ == '__main__':
    DownloaderApp().run() 