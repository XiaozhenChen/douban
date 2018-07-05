# coding = UTF8

import requests
from pyquery import PyQuery as pq
import csv
import time

id = 1467557
i = 0

URL_FORMAT = "https://movie.douban.com/subject/20495023/comments?start={}&limit=20&sort=new_score&status=P"

headers = {'user-agent': 'my-app/0.0.1'}
cookies = {
    'bid':'VJkeetqYdq8',
    '__utma':'30149280.573664895.1530809687.1530809687.1530809687.1',
    '__utmb':'30149280.1.10.1530809687',
    '__utmc':'30149280',
    '__utmz':'30149280.1530809687.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmt':'1',
    'ap':'1',
    'ps':'y',
    'll':'"119093"',
    'dbcl2':'"48342704:7Cg+xTaJX6U"',
    'ck':'lORc',
    'push_noty_num':'0',
    'push_doumail_num':'0',
    '_pk_id.100001.4cf6':'a971128f683843e5.1530809687.1.1530809982.1530809687.',
    '_pk_ses.100001.4cf6':'*',
    '__utma':'223695111.57711524.1530809847.1530809847.1530809847.1',
    '__utmb':'223695111.0.10.1530809847',
    '__utmc':'223695111',
    '__utmz':'223695111.1530809847.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login'
}

def main():
    ending = False
    index = 0
    while True:
        if ending:
            break
        time.sleep(2)
        r = requests.get(URL_FORMAT.format(index), cookies=cookies, verify=False)
        doc = pq(r.text)
        # doc = pq(URL_FORMAT.format(index))
        div_comments = doc("#comments")
        comment_items = div_comments(".comment-item")
        if len(comment_items) < 20:
            ending = True
        if len(comment_items) == 0:
            break
        save_to_file(comment_items)
        index += 20

def save_to_file(comment_items):
    # datas = pq.map(comment_items, parse(item))
    datas = []
    for item in comment_items:
        datas.append(parse(item))
            
    with open("comments.csv", 'a+', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerows(datas)

def parse(item):
    global i
    item = pq(item)
    vote = item(".votes").html()
    info = item(".comment-info a").html().encode("gbk","ignore").decode("gbk")
    rating = item(".comment-info").children(".rating").attr("title")
    comment_time = item(".comment-info").children(".comment-time").attr("title")
    comments = item("p").html().encode("gbk","ignore").decode("gbk")
    print(i, vote, info, rating, comment_time)
    i += 1
    return [vote, info, rating, comment_time, comments]

if __name__ == "__main__":
    main()
