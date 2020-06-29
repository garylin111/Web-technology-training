# -*- coding: utf-8 -*-
# __author__ = 'Carina'


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pyquery import PyQuery as pq
import re

# driver = webdriver.Chrome()
driver = webdriver.PhantomJS()
wait = WebDriverWait(driver, 10)


# 访问淘宝网，输入波希米亚裙
def search():
    try:
        driver.get("https://www.taobao.com")
        # 首页输入框
        input_box = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        # 搜索按钮
        submit = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#J_SearchForm > button")))
        input_box.send_keys('波希米亚裙')
        submit.click()
        total = wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total")))
        # 调用函数--商品信息
        get_products()
        return total.text
    except TimeoutError:
        return search()


# 跳转到下一页
def next_page(page_number):
    try:
        # 底部页码输入框
        input_box = wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        # 底部确定按钮
        submit = wait.until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input_box.clear()
        input_box.send_keys(page_number)
        submit.click()
        wait.until(ec.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number)))
        get_products()
    except TimeoutError:
        next_page()


# 获取淘宝商品信息
def get_products():
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist.items.item")))
    html = driver.page_source
    doc = pq(html)  # pyquery （driver.page_source）就相当于requests.get获取的内容
    items = doc("#mainsrp-itemlist.items.item").items()
    for item in items:
        product = {
            "image": item.find('.pic .img').attr('src'),
            "price": item.find('.price').text(),
            "deal": item.find('.deal-cnt').text()[:-3],
            "title": item.find('.title').text(),
            "shop": item.find('.shop').text(),
            "location": item.find('.location').text(),
        }
    print(product)


def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    # 爬取所有的数据用total+1
    for i in range(2, 4):
        next_page(i)


if __name__ == "__main__":
    main()
