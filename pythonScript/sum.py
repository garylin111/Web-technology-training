import csv
rid_dict = {1: "动画", 2: "国创相关", 3: "音乐", 4: "舞蹈", 5: "游戏", 6: "知识", 7: "数码", 8: "生活", 9: "鬼畜", 10: "时尚", 11: "娱乐", 12: "影视" }
time_dict = {0: "日排行", 1: "周排行", 2: "月排行"}

class Video:
    def __init__(self, sum_title, sum_play, sum_coins):
        self.sum_play = sum_play
        self.sum_title = sum_title
        self.sum_coins = sum_coins

    def to_csv(self):
        return [self.sum_title, self.sum_play, self.sum_coins]

    @staticmethod
    def csv_title(self):
        return ['分区', '播放量总量', '硬币总量']
sumList=[]
for x in range(3):
    for j in range(1,13):
        rid = rid_dict[j]
        time = time_dict[x]
        file_name = '/usr/share/nginx/html/data/{}{}top100.csv'.format(rid, time)
        csvfile = open(file_name, encoding="utf-8")
        reader = csv.reader(csvfile)
        data = []

        sum_coins = 0
        sum_play = 0
        sum_title = '{}'.format(rid)
        for line in reader:
            data.append(line)
        for i in range(1, 101):
            sum_coins += int(data[i][2])
            sum_play += int(data[i][3])
        v = Video(sum_title, sum_play, sum_coins)
        sumList.append(v)
        file_name = '/usr/share/nginx/html/data/sum/{}总和.csv'.format(time)
        with open(file_name, 'w', newline='', encoding="utf-8") as f:
            pen = csv.writer(f)
            pen.writerow(Video.csv_title(v))
            for v in sumList:
                pen.writerow(v.to_csv())
