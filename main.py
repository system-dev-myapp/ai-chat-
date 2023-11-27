import datetime 
import speech_recognition as sr
import webbrowser as wb
import os
import playsound
from gtts import gTTS
from playsound import playsound
import urllib.parse

def speak(audio):
    print(audio)
    tts = gTTS(text =audio,lang='vi')
    tts.save("xinchao.mp3")
    playsound("D:\\worksapce\\python\\aibot\\xinchao.mp3", True)
    os.remove("D:\\worksapce\\python\\aibot\\xinchao.mp3")
   
def time():
    Time=datetime.datetime.now().strftime("%I:%M:%p") 
    speak("It is")
    speak(Time)

def welcome():
        #Chao hoi
        hour=datetime.datetime.now().hour
        if hour >= 6 and hour<12:
            speak("Good Morning Sir!")
        elif hour>=12 and hour<18:
            speak("Good Afternoon Sir!")
        elif hour>=18 and hour<24:
            speak("Xin chào buổi tối!")
        speak("Xin chào, tôi có thể giúp gì cho bạn!") 


def command():
    c=sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold=2
        audio=c.listen(source)
    try:
        query = c.recognize_google(audio, language="vi-VN")
        print("Tony Lèo: "+query)
    except sr.UnknownValueError:
        print('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Your order is: '))
    return query

def get_directions_url(start_location, end_location):
    base_url = 'https://www.google.com/maps/dir/'
    # Chuyển đổi tọa độ đầu điểm và điểm đến thành dạng thích hợp cho URL
    start_location_encoded = urllib.parse.quote(start_location)
    end_location_encoded = urllib.parse.quote(end_location)

    # Tạo URL chỉ đường
    url = f'{base_url}{start_location_encoded}/{end_location_encoded}'

    return url

if __name__  =="__main__":
    welcome()

    while True:
        query=command().lower()
        if "tìm kiếm thông tin" in query:
            speak("Bạn muốn tìm kiếm thứ gì?")
            search=command().lower()
            url = f"https://google.com/search?q={search}"
            wb.get().open(url)
            speak(f'Kết quả tìm kiếm {search} trên google')
        
        elif "youtube" in query or  "video" in query:
            speak("Bạn muốn xem thứ gì?")
            search=command().lower()
            url = f"https://youtube.com/search?q={search}"
            wb.get().open(url)
            speak(f'Đây là kết quả {search} trên youtube')
        elif "chỉ đường" in query:
            speak("Vị trí bắt đầu của bạn ở đâu?")
            start_location=command().lower()
            speak("Điểm kết thúc của bạn ở đâu?")
            end_location=command().lower()
            url = get_directions_url(start_location, end_location)
            wb.get().open(url)
            speak(f'Đây là kết quả {search} trên google map')
        elif "thoát" in query:
            speak("bạn có thể gọi tôi bất cứ khi nào")
            quit()
        elif "open video" in query:
            wb.get().open('https://www.youtube.com/watch?v=xD8Xchuxq8gs')
        elif 'time' in query:
            time()
            