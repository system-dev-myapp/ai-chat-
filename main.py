import datetime, time
import speech_recognition as sr
import webbrowser as wb
import os
import playsound
from gtts import gTTS
from playsound import playsound
import urllib.parse
import os
import openai
import re
import wikipedia
import json
import smtplib
from youtube_search import YoutubeSearch

wikipedia.set_lang('vi')
language = 'vi'

def speak(audio):
    tts = gTTS(text =audio,lang='vi')
    tts.save("audio.mp3")
    file_path = os.path.join(".", "audio.mp3")
    playsound(file_path, True)
    os.remove(file_path)

def get_audio(): 
    c=sr.Recognizer()
    
    while True:
        with sr.Microphone() as microphone:
            c.pause_threshold = 1
            audio = c.listen(microphone)
        try:
            query = c.recognize_google(audio, language="vi-VN")
            return query.lower();
        except sr.UnknownValueError:
            speak("Xin lỗi tôi không thể nghe rõ bạn nói gì, bạn hãy nói lại giúp tôi!")
    

def get_directions(start_location, end_location, type = "map", key_word_search = ""):
    if(type == "map"):
        base_url = "https://www.google.com/maps/dir"
        url_start_end_code = urllib.parse.quote(start_location) 
        url_end_location = urllib.parse.quote(end_location)
        url = f"{base_url}/{url_start_end_code}/{url_end_location}"
        wb.get().open(url);
        speak(f"Đây là quãng đường ngắn nhất từ {start_location} đến {end_location}")
    if(type == "search"):
        base_url = "https://www.google.com/maps/search/"
        query_search_end_code =  urllib.parse.quote(key_word_search)
        wb.get().open(f"{base_url}{query_search_end_code}")
    
def the_end (): 
    speak("Hẹn gặp lại bạn lần sau nhé!")
    
def welcome():
        hour=datetime.datetime.now().hour
        if hour >= 6 and hour<12:
            speak("Xin chào buổi sáng, tôi có thể gọi bạn là gì nhỉ?")
        elif hour>=12 and hour<18:
            speak("Xin chào buổi chiều, tôi có thể gọi bạn là gì nhỉ?")
        elif hour>=18 and hour<24:
            speak("Xin chào buổi tối, tôi có thể gọi bạn là gì nhỉ?")
        name_user = get_audio().split("là") 
        print(name_user)
        speak(f"Xin chào {name_user[0] if len(name_user) == 1 else name_user[1]}, tôi có thể giúp gì cho bạn!") 
        
def google_search(keyword):
    base_url = "https://www.google.com/search?q="
    speak("Okay!")
    wb.get().open(f"{base_url}{keyword}")
    speak(f"Kết quả tìm kiếm cho từ khóa {keyword} trên google!")

def chat_gpt_run_time(prompt):
    openai.api_key="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"
    response = openai.Completion.create(
        engine="text-davinci-002",  # Đặt loại model bạn muốn sử dụng
        prompt=prompt,
        max_tokens =1000  # Số từ tối đa trong câu trả lời
    )
    return response.choices[0].text.strip()

def clean_text(raw_text):
    # Loại bỏ Markdown và HTML
    cleaned_text = re.sub(r'[*_`~]', '', raw_text)
    cleaned_text = re.sub(r'\[.*?\]', '', cleaned_text)
    cleaned_text = re.sub(r'<.*?>', '', cleaned_text)
    return cleaned_text

def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" %
              (now.day, now.month, now.year))
    else:
        speak("Tôi chưa nghe được bạn nói gì? hãy thử nói lại")

def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì?")
        query = get_audio()
        contents = wikipedia.summary(query).split("\n")
        print(contents)
        speak(contents[0])
        if(len(contents) > 1):
            time.sleep(3)
            speak("Bạn muốn nghe thêm không")
            load_more = get_audio()
            if("có" in load_more or "nghe thêm" in load_more):
                for content in contents[1:]:
                    speak(content)
                    time.sleep(5)
        speak('Cảm ơn bạn đã lắng nghe!!!')
    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")

def visits_website(domain):
    wb.get().open(f"https://{domain}")
    speak("Trang web bạn yêu cầu đã được mở!")
    
def open_application(text):
    if "google" in text:
        speak("Mở Google Chrome")
        os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk")
    elif "word" in text:
        speak("Mở Microsoft Word")
        os.startfile(
            'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk')
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        os.startfile(
            'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk')
    else:
        speak("Ứng dụng chưa được cài đặt. bạn có muốn tìm kiếm trên cửa hàng không?")
        user_should_use = get_audio()
        if("có" in user_should_use):
            base_url = "https://apps.microsoft.com/search?query="
            filter_query = "mở"
            if("ứng dụng" in text):
                filter_query = "ứng dụng"
            app_search = text.split(filter_query)[1]
            wb.get().open(f"{base_url}{app_search}")
        else:
            speak("Cảm ơn bạn đã sử dụng tôi!")
            
def send_mail_user(name):
    file_path = os.path.join(".", "acquaintance.json")
    with open(file_path, 'r', encoding='utf-8') as user_file:
        try:
            with open(file_path, 'r', encoding='utf-8') as user_file:
                data = json.load(user_file)
                users = data.get('user',[]) # nếu user không tồn tại thì giá trị của users là []
                user_match = [user for user in users if user.get("name").lower() == name]
                if(len(user_match) == 0): {
                    speak("Tên người dùng của bạn nói chưa có trong danh sách thân thiết!")
                }
                else:
                    email_user = [user.get('email') for user in user_match]
                    speak('Nội dung bạn muốn gửi là gì')
                    content = get_audio()
                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login('truongsonpt.80@gmail.com', 'ybjmuwqxsohznaow')
                    mail.sendmail('truongsonpt.80@gmail.com',
                                email_user[0], content.encode('utf-8'))
                    mail.close()
                    speak('Email của bạn vùa được gửi. Bạn check lại email nhé')
        except Exception as e:
            print("Có lỗi xảy ra:"+ str(e))

def play_music(mysong):
    while True:
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    print(result[0])
    print(url)
    wb.get().open(url)
    speak("Bài hát bạn yêu cầu đã được mở.")

# main
def __main__():
    welcome()
    i = 0
    while True:
        if(i > 0):
            speak("Bạn có muốn tôi làm gì nữa không?")
        query = get_audio()
        if("mở" in query):
            if("bật google" in query or "tìm kiếm" in query or "search" in query):
                filter_query = query.split("tìm kiếm")[1]
                if(filter_query != ""):
                    google_search(filter_query)
                else:
                    speak("Bạn muốn tìm gì?")
                    query_search = get_audio()
                    google_search(query_search)
            elif ("bài hát" in query):
                filter_query = "là"
                if("hát" in query):
                    filter_query = "hát"
                mysong = query.split(filter_query)
                if(len(mysong) > 0): {
                    play_music(mysong[1])
                }
                else:
                    speak("Bạn hãy nói tên bài hát muốn nghe!")
                    mysong = get_audio()
                    play_music(mysong)
            else:
                open_application(query)
        elif ("nói chuyện với ai" in query):
            speak("Bạn hãy nói thông tin câu hỏi?")
            question = get_audio()
            result = chat_gpt_run_time(question)
            print(result)
            speak(f"Kết quả của câu hỏi {question} là: {clean_text(result)}")
        elif ("chỉ đường" in query):
            if("từ" in query and "đến" in query or "tới" in query or "đi" in query):
                keyword_filter = "đến"
                if("tới" in query):
                    keyword_filter = "tới"
                elif ("đi" in query):
                    keyword_filter = "đi"
                array_locations = query.split("từ")[1].split(keyword_filter)
                get_directions(array_locations[0],array_locations[1])
            elif ("đến" in query or "tới" in query):
                keyword_filter = "đến"
                if("tới" in query):
                    keyword_filter = "tới"
                keyword_search = query.split(keyword_filter)[1]
                get_directions("","","search",keyword_search)
            else:
                speak("Bạn hãy nói điểm bắt đầu của bạn!")
                start_location =  get_audio()
                speak("Điểm kết thúc của bạn ở đâu?")
                end_location = get_audio()
                get_directions(start_location, end_location)
        elif ("bây giờ là mấy giờ" in query or "hôm nay ngày bao nhiêu" in query):
            get_time(query)
        elif ("gửi thư" in query):
            speak("Hãy nói tên bạn muốn gửi")
            name_user = get_audio()
            send_mail_user(name_user)
        elif("lý thuyết" in query):
            tell_me_about()
        elif ("hẹn gặp lại" in query):
            the_end()
            quit()
        time.sleep(3)
        i += 1
    
__main__()