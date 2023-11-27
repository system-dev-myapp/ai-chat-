from flask import Flask, render_template, request
import datetime
import speech_recognition as sr
import webbrowser as wb
import os
from gtts import gTTS
from playsound import playsound
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/hello")
def hello():
    print("da lot vao day")
    return "Hello, world!"

@app.route('/process_command', methods=['POST'])
def process_command():
    playsound("static/xinchao.mp3", True)
    query = request.form['query'].lower()
    response = handle_query(query)
    return response

def speak(audio):
    print(audio)
    tts = gTTS(text=audio, lang='vi')
    tts.save("static/xinchao.mp3")
    playsound("static/xinchao.mp3", True)
    os.remove("static/xinchao.mp3")

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%p")
    speak("It is")
    speak(Time)

def welcome():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    elif 18 <= hour < 24:
        speak("Xin chào buổi tối!")
    speak("Xin chào, tôi có thể giúp gì cho bạn!")

def command():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold = 2
        audio = c.listen(source)
    try:
        query = c.recognize_google(audio, language="vi-VN")
        print("Tony Lèo: " + query)
    except sr.UnknownValueError:
        print('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Your order is: '))
    return query

def get_directions_url(start_location, end_location):
    base_url = 'https://www.google.com/maps/dir/'
    start_location_encoded = urllib.parse.quote(start_location)
    end_location_encoded = urllib.parse.quote(end_location)
    url = f'{base_url}{start_location_encoded}/{end_location_encoded}'
    return url

def handle_query(query):
    if "tìm kiếm thông tin" in query:
        speak("Bạn muốn tìm kiếm thứ gì?")
        search = command().lower()
        url = f"https://google.com/search?q={search}"
        wb.get().open(url)
        speak(f'Kết quả tìm kiếm {search} trên google')
        return f'Kết quả tìm kiếm {search} trên google'

    # Thêm xử lý cho các lệnh khác tại đây

    elif "thoát" in query:
        speak("bạn có thể gọi tôi bất cứ khi nào")
        quit()
        return 'Ứng dụng đã thoát'

if __name__ == "__main__":
    app.run(debug=True)
