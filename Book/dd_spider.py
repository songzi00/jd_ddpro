import requests
from bs4 import BeautifulSoup
from sql_setting.config import cursor,connect
import time,random

# 构建useragnet列表
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


def get_type():
    url = 'http://category.dangdang.com/?ref=www-0-C'
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers, timeout=10)
    file = response.content.decode('gbk')
    soup = BeautifulSoup(file, 'lxml')
    type_url_list = [] #存储每个种类的分页
    original_link = [] #存储原始url链接

    # 获取每个种类的图书url
    computer = soup.select('#floor_1 > div:nth-child(39) > div > a')[0]['href']  # 计算机分类url
    kp_book = soup.select('#floor_1 > div:nth-child(38) > div > a')[0]['href']  # 科普读物分类url
    gj_book = soup.select('#floor_1 > div:nth-child(37) > div > a')[0]['href']  # 工具书分类url
    jc_book = soup.select('#floor_1 > div:nth-child(36) > div > a')[0]['href']  # 教材分类url
    ks_book = soup.select('#floor_1 > div:nth-child(35) > div > a')[0]['href']  #考试分类url

    original_link.extend([computer,kp_book,gj_book,jc_book,ks_book])

    # 构建多页URL
    for url in original_link:
        url = url.replace('http://category.dangdang.com/','')
        # 构建多页url
        for url_num in range(1,9):
            type_url = 'http://category.dangdang.com/pg{}-'.format(url_num) + url
            type_url_list.append(type_url)

    print('--------------图书种类链接获取成功--------------')
    return type_url_list



def get_detail_url(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers, timeout=10)
    file = response.content.decode('gbk')
    soup = BeautifulSoup(file, 'lxml')
    detail_list = []
    #获取所有的详情页url列表
    url_list = soup.select('#component_59 > li > a')
    # 遍历以后存入列表
    for url in url_list:
        detail_list.append(url['href'])
    print('--------------获取详情页链接成功--------------')
    return detail_list

def get_book_date(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers, timeout=10)
    file = response.content.decode('gbk')

    soup = BeautifulSoup(file, 'lxml')
    name = soup.select('#product_info > div.name_info > h1')[0].get_text().strip()  #书名
    author = soup.select('#author > a')[0].get_text()   #作者
    press = soup.select('#product_info > div.messbox_info > span:nth-child(2) > a')[0].get_text()  #出版社

    date = soup.select('#product_info > div.messbox_info > span:nth-child(3)')[0].get_text()    #出版时间
    date = date.replace('出版时间:','')

    price = soup.select('#dd-price')[0].get_text().strip()
    price = price.replace('¥','')

    size = soup.select('#detail_describe > ul > li:nth-child(1)')[0].get_text()
    size = size.replace('开 本：','')

    number = soup.select('#detail_describe > ul > li:nth-child(5)')[0].get_text()   #书号
    number = number.replace('国际标准书号ISBN：','')

    type = soup.select('#detail-category-path > span > a:nth-child(2)')[0].get_text()



    img = soup.select('#largePic')[0]['src'] #图片
    com_num = ''
    url = url
    origin = '当当网'

    print(name, author, press, date, price, com_num, size, number, type, img, url, origin)
    try:
        sql = 'insert into book(book_name,author,press,book_date,price,com_num,book_size,book_number,book_type,img,url,origin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            name, author, press, date, price, com_num, size, number, type, img, url, origin))
        connect.commit()
        print('--------------mysql数据插入成功--------------------')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    for type_url in get_type():
       for detail_url in get_detail_url(type_url):
           try:
               get_book_date(detail_url)
               time.sleep(random.uniform(0.5, 3.5))
           except:
               continue
