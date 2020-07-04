import requests
import fake_useragent
from requests import get
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from os.path import exists
from os import mkdir
import csv

rid_dict = {  # 创建字典，方便调用
    "全站": 0,
    "动画": 1,
    "国创相关": 168,
    "音乐": 3,
    "舞蹈": 129,
    "游戏": 4,
    "知识": 36,
    "数码": 188,
    "生活": 160,
    "鬼畜": 119,
    "时尚": 155,
    "娱乐": 5,
    "影视": 181}
time_dict = {
    "日排行": 1,
    "周排行": 7,
    "月排行": 30}


def dict_get(dict_, objkey):  # 从字典中取值，返回key对应的value
    if isinstance(dict_, dict):
        for key, value in dict_.items():
            if key == objkey:
                return value
            else:  # 如果value是dict类型，则进行迭代
                if isinstance(value, dict):
                    ret = dict_get(value, objkey)
                    if ret is not None:
                        return ret
                elif isinstance(value, list):  # 如果value是list类型，则依次进行迭代
                    for i in range(len(value)):
                        ret = dict_get(value[i], objkey)
                        if ret is not None:
                            return ret
        return None  # 找不到指定的key，返回None
    else:
        return None


def url_get(url, mode=None, timeout=20):  # 获取网页内容
    retry_count = 0  # 尝试的次数
    try:
        if mode is None:
            return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout)
        elif mode == "json":
            return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout).json()
        elif mode == "content":
            return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout).content
        elif mode == "text":
            return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout).text
        elif mode == "code":
            return get(url=url, headers={"User-Agent": UserAgent().random}, timeout=timeout).status_code
        else:
            raise ValueError("所给Mode错误，应是：None/json/content/text/code")
    except Exception:
        if retry_count > 3:
            raise Exception("已达最大尝试次数")
        else:
            retry_count += 1




rid_dict = {"全站": 0, "动画": 1, "国创相关": 168, "音乐": 3, "舞蹈": 129, "游戏": 4, "知识": 36, "数码": 188, "生活": 160, "鬼畜": 119, "时尚": 155, "娱乐": 5, "影视": 181}
rid1_dict = {0: "全站", 1: "动画", 2: "国创相关", 3: "音乐", 4: "舞蹈", 5: "游戏", 6: "知识", 7: "数码", 8: "生活", 9: "鬼畜", 10: "时尚", 11: "娱乐", 12: "影视" }
day_dict = {"日排行": 1, "周排行": 7, "月排行": 30}
day1_dict = {0: "日排行", 1: "周排行", 2: "月排行"}

def rank_crawler():
    # 保存目录
    save_path = "/usr/share/nginx/html/data"
    # 如果目录不存在则创建目录
    if not exists(save_path):
        mkdir(save_path)
    for x in range(13):
        for j in range(3):
            rid1 = rid1_dict[x]
            rid = rid_dict[rid1]
            day1 = day1_dict[j]
            day = day_dict[day1]
            url = "https://api.bilibili.com/x/web-interface/ranking?rid={}&day={}".format(rid, day)  # 拼接url
            res = url_get(url=url, mode="json")
            rank_list = dict_get(res, "list")

            class Video:
                def __init__(self, aid, author, coins, play, pts, title, video_review, reprint):
                    self.bvid = bvid
                    self.title = title
                    self.author = author
                    self.coins = coins
                    self.play = play
                    self.pts = pts
                    self.video_review = video_review
                    #self.pic = pic
                    self.reprint = reprint

                def to_csv(self):
                    return [self.bvid, self.author, self.coins, self.play, self.pts, self.title, self.video_review, self.reprint]

                @staticmethod
                def csv_title(self):
                    return ['视频bv号', 'up主', '投币数', '播放数', '综合得分', '视频标题', '视频弹幕数', '原创']

            videos = []

            for i in range(len(rank_list)):
                bvid = dict_get(rank_list[i], "bvid")  # 视频bv号
                author = dict_get(rank_list[i], "author")  # up主
                coins = dict_get(rank_list[i], "coins")  # 投币数
                play = dict_get(rank_list[i], "play")  # 播放数
                pts = dict_get(rank_list[i], "pts")  # 综合得分
                title = dict_get(rank_list[i], "title")  # 视频标题
                video_review = dict_get(rank_list[i], "video_review")  # 视频弹幕数
                #pic = dict_get(rank_list[i], "pic")  # 视频封面
                no_reprint = dict_get(rank_list[i], "no_reprint")
                if no_reprint == 1:  # 是否原创
                    reprint = "原创"
                else:
                    reprint = "转载"
                v = Video(bvid, author, coins, play, pts, title, video_review, reprint)
                videos.append(v)

            file_name = save_path+'/{}{}top100.csv'.format(rid1, day1)  # 保存视频信息的文件
            with open(file_name, 'w', newline='', encoding="utf-8") as f:
                pen = csv.writer(f)
                pen.writerow(Video.csv_title(v))
                for v in videos:
                    pen.writerow(v.to_csv())

if __name__ == "__main__":
    rank_crawler()