'''

*-----------------------------------------------------------------*
*                                                                 *
*                      尝试编写第一个爬虫代码                       *
*              爬取目标为当当网的前500本五星好评书籍                 *
*                           爬取内容为:                            *
*      书名、五星评分次数、价格、推荐指数、排名、作者、图片地址        *
*                                                                 *
*-----------------------------------------------------------------*

'''

import requests
import json
import re

def main(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    html = request_dandan(url)
    items = parse_result(html)


    for item in items:
#        print(item)
        write_item_to_file(item)

def request_dandan(url):          #请求网页的文本内容
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def parse_result(html):            #使用正则处理网页文本内容，过滤出想要爬取的内容
    pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'range': item[0],
            'image': item[1],
            'title': item[2],
            'recommand': item[3],
            'author': item[4],
            'times': item[5],
            'price': item[6]
        }

def write_item_to_file(item):      #将过滤出的内容写成json文本保存到bbook.txt
    print('Start writing data ===>' + str(item))
    with open('book.txt', 'a', encoding='UTF-8') as file:
        file.write(json.dumps(item, ensure_ascii=False) + '\n')
        file.close()




if __name__ == '__main__':
    for i in range(1,26):
        main(i)
