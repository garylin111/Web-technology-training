import requests
from bs4 import BeautifulSoup
import csv
rid_dict = {"全站": 0, "动画": 1, "国创相关": 168, "音乐": 3, "舞蹈": 129, "游戏": 4, "知识": 36, "数码": 188, "生活": 160, "鬼畜": 119, "时尚": 155, "娱乐": 5, "影视": 181}
rid1_dict = {0: "全站", 1: "动画", 2: "国创相关", 3: "音乐", 4: "舞蹈", 5: "游戏", 6: "知识", 7: "数码", 8: "生活", 9: "鬼畜", 10: "时尚", 11: "娱乐", 12: "影视" }
time_dict = {"日排行": 1, "周排行": 7, "月排行": 30}
time1_dict = {0: "日排行", 1: "周排行", 2: "月排行"}
for i in range(13):
    for j in range(3):
        rid1 = rid1_dict[i]
        rid = rid_dict[rid1]
        time1 = time1_dict[j]
        time = time_dict[time1]
        url = "https://www.bilibili.com/ranking/all/{}/0/{}".format(rid, time)

        response = requests.get(url)
        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')


        class Video:
            def __init__(self, rank, title, visit, comments, score, up_id, av):
                self.rank = rank
                self.title = title
                self.visit = visit
                self.comments = comments
                self.score = score
                self.up_id = up_id
                self.av = av

            def to_csv(self):
                return [self.rank, self.title, self.visit, self.comments, self.score, self.up_id, self.av]

            @staticmethod
            def csv_title(self):
                return ['排名', '标题', '播放量', '讨论数', '得分', 'UP的ID', '视频av号']

        items = soup.findAll('li', {'class': 'rank-item'})
        videos = []  # 保存提取出来的Video列表

        for item in items:
            rank = item.find('div', {'class': 'num'}).text  # 视频排名
            title = item.find('a', {'class': 'title'}).text  # 视频标题
            visit = item.find('span', {'class': 'data-box'}).text  # 视频播放量
            comments = item.find_all('span', {'class': 'data-box'})[1].text  # 视频讨论数
            score = item.find('div', {'class': 'pts'}).find('div').text  # 视频综合得分
            space = item.find_all('a')[2].get('href')
            up_id = space[len('//space.bilibili.com/'):]
            http = item.find_all('a')[1].get('href')
            av = http[len('https//www.bilibili.com/video//'):]
            v = Video(rank, title, visit, comments, score, up_id, av)
            videos.append(v)

        file_name = '{}{}top100.csv'.format(rid1, time1)  # 保存视频信息的文件
        with open(file_name, 'w', newline='', encoding="utf-8") as f:
            pen = csv.writer(f)
            pen.writerow(Video.csv_title(v))
            for v in videos:
                pen.writerow(v.to_csv())