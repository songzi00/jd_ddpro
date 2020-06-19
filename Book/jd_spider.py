import requests,random,re,json,time
from sql_setting.config import cursor,connect
from bs4 import BeautifulSoup


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



# 获取分类url
def get_type():
    url = 'https://book.jd.com/booksort.html'
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers, timeout=10)
    file = response.content.decode('gbk')
    soup = BeautifulSoup(file,'lxml')

    type_list = []
    list_url = []

    # 获取分类url中的id数字，从而拼凑图书列表页的URL
    computer = soup.select('#booksort > div.mc > dl > dt:nth-child(67) > a')[0]['href']     #计算机类
    novel = soup.select('#booksort > div.mc > dl > dt:nth-child(1) > a')[0]['href']         #小说类
    history = soup.select('#booksort > div.mc > dl > dt:nth-child(49) > a')[0]['href']      #历史类
    sciences = soup.select('#booksort > div.mc > dl > dt:nth-child(65) > a')[0]['href']     #社会科学类
    foreign = soup.select('#booksort > div.mc > dl > dt:nth-child(89) > a')[0]['href']      #外语

    type_list.extend((computer,novel,history,sciences,foreign))
    for type in type_list:
        type_id = re.findall('\d+',type)
        type_url = 'https://list.jd.com/list.html?cat=' + ','.join(type_id)
        # 设置分页链接，京东的page的间隔是2，s是60，所以循环设置url
        for i, z in zip(range(1, 21, 2), range(30, 571, 60)):
            page_url = '{0}&page={1}&s={2}&click=0'.format(type_url,i, z)
            list_url.append(page_url)
    return list_url


# 获取详情页url
def get_dateil(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers, timeout=10)
    file = response.content.decode('utf-8')
    soup = BeautifulSoup(file, 'lxml')

    dateil_list = []
    id_list = soup.select('#J_goodsList > ul > li') #获取所有的图书li

    for id in id_list:
        dateil_id = id['data-sku'] #获取图书li中的data-sku中的详情页id，从而拼凑详情页URL
        dateil_url = 'https://item.jd.com/{}.html'.format(dateil_id)
        dateil_list.append(dateil_url)

    return dateil_list


# 获取数据
def get_date(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers, timeout=10)
    file = response.content.decode('utf-8')
    soup = BeautifulSoup(file, 'lxml')
    name = soup.select('.sku-name')[0].get_text()  #获取标题
    name = name.strip()

    author = soup.select('#p-author')[0].get_text()  # 作者
    author = author.strip()

    # 因为每个商品的数据可能不全，所以设置默认值，如果商品中没有此信息，便显示默认值
    press = ''
    date = ''
    number = ''
    size = ''

    data_ul = soup.select('#parameter2 > li')
    date_list = [li.get_text() for li in data_ul]

    for d in date_list:
        if '出版社' in d:
            press = d.split('：')[1].strip()
        elif '出版时间' in d:
            date = d.replace('出版时间：', '')
        elif 'ISBN' in d:
            number = d.replace('ISBN：', '')
        elif '开本' in d:
            size = d.replace('开本：', '')


    pro_id = soup.select('#summary-price > .dd > a')[0]['data-sku']  #获取id

    # 评论人数
    # 通过抓包获取评论链接组成，将每个商品的id填入进去，便得到一个json数据
    comments_url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(pro_id)
    comments_json = requests.get(comments_url).text
    s = re.compile(r'fetchJSON_comment.*?\(')
    uesless = str(s.findall(comments_json))
    jd = json.loads(comments_json.lstrip(uesless).rstrip(');'))
    com_list = jd['productCommentSummary']
    global com_num  #将评论人数变量设置为全局变量
    for i in com_list:
        if i == 'commentCountStr':
            com_num = com_list[i]


    # 价格
    price = []
    priceurl = "https://p.3.cn/prices/mgets?callback=jQuery6775278&skuids=J_" + str(pro_id)  # 请求价格的URL
    pricedata = requests.get(priceurl)
    pricepat = '"p":"(.*?)"}'  # 建立匹配模式
    thisprice = re.compile(pricepat).findall(pricedata.text)  # 查找url
    price = price + thisprice
    price = price[0]
    if ',' in price:
        price = price.split('"')[0]

    type = soup.select('#crumb-wrap > div > div.crumb.fl.clearfix > div:nth-child(3) > a')[0].get_text()  # 分类

    img = soup.select('#spec-n1 > img')[0]['src']  # 图片
    img = 'https:' + img

    url = url
    origin = '京东图书'

    print(name, author, press, date, price,com_num, size, number, type, img, url, origin)
    try:
        sql = 'insert into book(book_name,author,press,book_date,price,com_num,book_size,book_number,book_type,img,url,origin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        cursor.execute(sql, (
        name, author, press, date, price,com_num, size, number, type, img, url, origin))
        connect.commit()
        print('--------------mysql数据插入成功--------------------')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    for type_url in get_type():
        for dateil_url in get_dateil(type_url):
            try:
                get_date(dateil_url)
                time.sleep(random.uniform(0.5, 3.5))
            except:
                print('图书无法解析,链接为{}'.format(dateil_url))
                continue


