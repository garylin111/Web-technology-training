#导入所需的库
import requests
from bs4 import BeautifulSoup
import csv

#爬取的网页的网址
url = 'https://www.bilibili.com/ranking/all/1/0/1'

#发起网络请求
response = requests.get(url)
html_text = response.text
soup = BeautifulSoup(html_text, 'html.parser')

#用来保存视频信息的对象
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

#提取列表
items = soup.findAll('li', {'class': 'rank-item'})
videos = []#保存提取出来的Video列表

for item in items:
    rank = item.find('div', {'class': 'num'}).text#视频排名
    title = item.find('a', {'class': 'title'}).text#视频标题
    visit = item.find('span', {'class': 'data-box'}).text#视频播放量
    comments = item.find_all('span', {'class': 'data-box'})[1].text#视频讨论数
    score = item.find('div', {'class': 'pts'}).find('div').text#视频综合得分
    v = Video(rank, title, visit, comments, score)
    videos.append(v)

print(Video.csv_title(v))
for v in videos:
    print(v.to_csv())

file_name = 'top100.csv'#保存视频信息的文件
with open(file_name, 'w', newline='', encoding="utf-8") as f:
    pen = csv.writer(f)
    pen.writerow(Video.csv_title(v))
    for v in videos:
        pen.writerow(v.to_csv())