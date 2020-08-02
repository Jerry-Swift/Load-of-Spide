'''
*------------------------------------------------------------------*
*
*                          第四个爬虫代码
*                     采用线程池方式并发爬取图片
*                           实现逻辑为：
*                        对所有页面进行遍历
*                     获取每个页面中存在的对象链接
*                    将每个链接依次加入到列表urls中
*                  以上步骤由函数get_page_urls()完成
*                   再依次遍历urls中的每一个对象链接
*                  爬取对象链接中存在的所有页面中的图片
*                       由函数download()完成
*                          将图片保存到本地
*                      由函数download_Pic()完成
*       线程池采用 concurrent.futures 模块的 ThreadPoolExecutor 实现
*
*-------------------------------------------------------------------*

'''
# encoding = utf-8
import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
from headers import fake_headers
import requests
from bs4 import BeautifulSoup


def header(referer):

    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }

    return headers


def request_page(url):
    try:
        headers = fake_headers()
        response = requests.get(url, headers=headers)   #必须带headers才能请求到网页
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print('请求失败')
        return None


def get_page_urls():        #遍历所有页面，将页面中的链接依次加入到urls内

    for i in range(1, 5):   #指定要爬取的页面
        baseurl = 'https://www.mzitu.com/page/{}'.format(i)
        print('******* ' + baseurl + ' ********')
        html = request_page(baseurl)
        soup = BeautifulSoup(html, 'lxml')

        list = soup.find(class_='postlist').find_all('li')
        urls = []
        for item in list:
            url = item.find('span').find('a').get('href')
            print('页面链接：%s' % url)
            urls.append(url)


    return urls     #要爬取的页面内的所有URL对象


def download_Pic(title, image_list):
    # 新建文件夹
    os.mkdir(title)
    j = 1
    # 下载图片
    for item in image_list:
        filename = '%s/%s.jpg' % (title, str(j))
        print('downloading....%s : NO.%s' % (title, str(j)))
        with open(filename, 'wb') as f:
            img = requests.get(item, headers=header(item)).content
            f.write(img)
        j += 1

def download(url):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    total = soup.find(class_='pagenavi').find_all('a')[-2].find('span').string  #单个对象内的所有图片
    title = soup.find('h2').string
    image_list = []

    for i in range(int(total)):
    #for i in range(5):
        html = request_page(url + '/%s' % (i + 1))  #每个对象内的URL组织形式
        soup = BeautifulSoup(html, 'lxml')
        img_url = soup.find('img').get('src')
        image_list.append(img_url)                  #获取到单个对象内的所有图片

    download_Pic(title, image_list)                 #调用文件写入命令，访问所有图片链接，保存至本地


def download_all_images(list_page_urls):
    # 获取每一个详情妹纸
    # works = len(list_page_urls)
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as exector:
        for url in list_page_urls:
            exector.submit(download, url)


if __name__ == '__main__':
    # 获取每一页的链接和名称
    list_page_urls = get_page_urls()
    download_all_images(list_page_urls)