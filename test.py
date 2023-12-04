import requests
from bs4 import BeautifulSoup

def get_khoa_info():
    url = "https://khoacntt.uneti.edu.vn/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tìm kiếm và in thông tin giới thiệu về khoa
        intro = soup.find('div', class_='content').get_text()
        print("Thông tin giới thiệu về khoa:")
        print(intro.strip())

        # Tìm kiếm và in danh sách đề tài NCKH
        research_projects = soup.find('div', class_='research-projects').find_all('li')
        print("\nDanh sách đề tài NCKH:")
        for project in research_projects:
            print(project.get_text().strip())

    else:
        print(f"Không thể truy cập trang web, mã trạng thái: {response.status_code}")

# Gọi hàm để lấy thông tin từ trang web
get_khoa_info()
