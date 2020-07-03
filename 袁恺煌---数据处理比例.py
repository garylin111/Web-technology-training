import csv
rid_dict = {0: "全站", 1: "动画", 2: "国创相关", 3: "音乐", 4: "舞蹈", 5: "游戏", 6: "知识", 7: "数码", 8: "生活", 9: "鬼畜", 10: "时尚", 11: "娱乐", 12: "影视" }
time_dict = {0: "日排行", 1: "周排行", 2: "月排行"}
for x in range(13):
    for j in range(3):
        rid = rid_dict[x]
        time = time_dict[j]
        file_name = '{}{}top100.csv'.format(rid, time)
        csvfile = open(file_name, encoding="utf-8")
        reader = csv.reader(csvfile)
        data = []
        sum_coins = 0
        sum_play = 0
        for line in reader:
            data.append(line)
        for i in range(1, 101):
            sum_coins += int(data[i][2])
            sum_play += int(data[i][3])


        class Video:
            def __init__(self, rata_title, rata_play, rata_coins):
                self.rata_play = rata_play
                self.rata_title = rata_title
                self.rata_coins = rata_coins

            def to_csv(self):
                return [self.rata_title, self.rata_play, self.rata_coins]

            @staticmethod
            def csv_title(self):
                return ['标题', '播放量比例', '硬币比例']


        rata = []

        for i in range(1, 101):
            rata_title = data[i][5]
            rata_coins = int(data[i][2]) / int(sum_coins)
            rata_play = int(data[i][3]) / int(sum_play)
            v = Video(rata_title, rata_play, rata_coins)
            rata.append(v)

        file_name = 'top{}{}100播放量,投币占总比例.csv'.format(rid, time)  # 保存视频信息的文件
        with open(file_name, 'w', newline='', encoding="utf-8") as f:
            pen = csv.writer(f)
            pen.writerow(Video.csv_title(v))
            for v in rata:
                pen.writerow(v.to_csv())