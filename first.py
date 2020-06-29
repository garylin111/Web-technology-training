import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.bilibili.com/ranking/all/1/0/1'

response = requests.get(url)
html_text = response.text
soup = BeautifulSoup(html_text, 'html.parser')

class Video:
    def __init__(self, rank, title, visit, comments, score):
        self.rank = rank
        self.title = title
        self.visit = visit
        self.comments = comments
        self.score = score

    def to_csv(self):
        return [self.rank, self.title, self.visit, self.comments, self.score]

    @staticmethod
    def csv_title(self):
        return ['排名', '标题', '播放量', '讨论数', '得分']


items = soup.findAll('li', {'class': 'rank-item'})
videos = []

for item in items:
    rank = item.find('div', {'class': 'num'}).text
    title = item.find('a', {'class': 'title'}).text
    visit = item.find('span', {'class': 'data-box'}).text
    comments = item.find_all('span', {'class': 'data-box'})[1].text
    score = item.find('div', {'class': 'pts'}).find('div').text
    print(f'{rank}.{title} {visit} {comments} {score}')
    v = Video(rank, title, visit, comments, score)
    videos.append(v)

file_name = 'first.csv'
with open(file_name, 'w', newline='', encoding="utf-8") as f:
    pen = csv.writer(f)
    pen.writerow(Video.csv_title(v))
    for v in videos:
        pen.writerow(v.to_csv())