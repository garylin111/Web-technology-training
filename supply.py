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


def rank_crawler():
    # 保存目录
    save_path = "rank"
    # 如果目录不存在则创建目录
    if not exists(save_path):
        mkdir(save_path)
    for k, v in rid_dict.items():  # 遍历排行时间字典
        rid = v
        for k2, v2 in time_dict.items():
            day = v2
            url = "https://api.bilibili.com/x/web-interface/ranking?rid={}&day={}".format(rid, day)  # 拼接url
            res = url_get(url=url, mode="json")
            rank_list = dict_get(res, "list")
            for i in range(len(rank_list)):
                aid = dict_get(rank_list[i], "aid")  # 视频id
                author = dict_get(rank_list[i], "author")  # up主
                coins = dict_get(rank_list[i], "coins")  # 投币数
                play = dict_get(rank_list[i], "play")  # 播放数
                pts = dict_get(rank_list[i], "pts")  # 综合得分
                title = dict_get(rank_list[i], "title")  # 视频标题
                video_review = dict_get(rank_list[i], "video_review")  # 视频弹幕数
                pic = dict_get(rank_list[i], "pic")  # 视频封面
                no_reprint = dict_get(rank_list[i], "no_reprint")
                if no_reprint == 1:  # 是否原创
                    reprint = "原创"
                else:
                    reprint = "转载"

                with open("rank/Bilibili-{}-{}.csv".format(save_path, k, k2), "a+", encoding="utf-8") as data_file:
                    data_file.write("排名:{}".format(i + 1))
                    data_file.write("视频id:{}".format(aid))
                    data_file.write("up主:{}".format(author))
                    data_file.write("投币数:{}".format(coins))
                    data_file.write("播放数:{}".format(play))
                    data_file.write("综合得分:{}".format(pts))
                    data_file.write("视频标题:{}".format(title))
                    data_file.write("视频弹幕数:{}".format(video_review))
                    data_file.write("是否原创:{}".format(reprint))
                    data_file.write("视频封面:{}/n".format(pic))
                    data_file.close()

                print("时间：{}".format(day))
                print("排名: {}".format(i + 1))
                print("视频id: {}".format(aid))
                print("up主: {}".format(author))
                print("投币数: {}".format(coins))
                print("播放数: {}".format(play))
                print("综合得分: {}".format(pts))
                print("视频标题: {}".format(title))
                print("视频封面：{}".format(pic))
                print("视频弹幕数: {}".format(video_review))
                print("是否原创: {}".format(reprint))
                print("-" * 60)
if __name__ == "__main__":
    rank_crawler()