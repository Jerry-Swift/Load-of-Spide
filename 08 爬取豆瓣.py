'''

*----------------------------------------------------------------*
*                                                                *
*                     尝试编写第二个爬虫代码                       *
*               爬取目标为豆瓣网评分前二百五十部电影                *
*                        爬取内容为:                              *
*            电影名|分数|导演|排名|电影|封面|简介                   *
*                      部分内容待注释                             *
*----------------------------------------------------------------*

'''


import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent    #模仿浏览器请求
import xlwt     #写excel表格模块，excel表格读模块为xlrd



def main(page):

    url = 'https://movie.douban.com/top250?start='+ str(page*25)+'&filter='
    html = request_douban(url)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)

book = xlwt.Workbook(encoding='utf-8', style_compression=0)     #创建一个excel表格
sheet=book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)    #创建一个子表sheet
sheet.write(0,0,'名称')       #写入（行，列，内容）
sheet.write(0,1,'图片')
sheet.write(0,2,'排名')
sheet.write(0,3,'评分')
sheet.write(0,4,'导演')
sheet.write(0,5,'简介')

n=1

def request_douban(url):
    user_Agent = UserAgent()
    agent = user_Agent.random
    headers = {
        "User-Agent": agent
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:     #捕捉异常请求
        return None




def save_to_excel(soup):
    list = soup.find(class_='grid_view').find_all('li')     #find(key=value) 找到并返回第一个指定的’key=value‘
                                                            #find_all('attribute') 找到所有attribute，并以列表形式返回

    for item in list:
        item_name = item.find(class_='title').string        #class_ 结尾带下划线用于避免和保留字冲突，在实际调用中不会带下划线
        item_img = item.find('a').find('img').get('src')    #get('attribute') 直接获取标签attribute对应的链接内容
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string  #从html标签格式中提取出字符串 eg：从<em class="">50</em>中提取出50
        item_director = item.find('p').text.split('主演')[0].lstrip().lstrip('导演: ')  #只留下电影导演

        if(item.find(class_='inq')!=None):
            item_intr = item.find(class_='inq').string

        # print('爬取电影：' + item_index + ' | ' + item_name +' | ' + item_img +' | ' + item_score +' | ' + item_author +' | ' + item_intr )
        print('爬取电影：' + item_index + ' | ' + item_name  +' | ' + item_score  +' | ' + item_intr )

        global n

        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_director)
        sheet.write(n, 5, item_intr)

        n = n + 1





if __name__ == '__main__':

    for i in range(0, 10):
        main(i)

book.save(u'豆瓣最受欢迎的250部电影.xlsx')    #保存表格文件并命名
