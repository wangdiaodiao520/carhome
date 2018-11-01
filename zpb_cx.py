from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import csv
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
#browser = webdriver.Chrome()

def get_one(url):
    browser.get(url)
    soup = BeautifulSoup(browser.page_source,'lxml')
    uiboxs = soup.select('.uibox')[2:]
    for uibox in uiboxs:
        yield uibox
    
def get_two(uibox):
    pps = uibox.select('div')[1].select('dl')
    for pp in pps:
        yield pp
        
def get_three(pp,jb):
    pp_name = pp.select('dt div a')[0].get_text()
    cjs = pp.select('dd .h3-tit')
    uls = pp.select('dd ul')
    for cj in cjs:
        cj_name = cj.select('a')[0].get_text()
        cj_uls = uls[cjs.index(cj)]
        cxs = cj_uls.select('li')
        for cx in cxs:
            try:
                cx_name = cx.select('h4 a')[0].get_text()
                cx_url = cx.select('h4 a')[0]['href']
            except IndexError:
                pass
            url = "https:" + cx_url
            browser.get(url)
            soup = BeautifulSoup(browser.page_source,'lxml')
            nows = soup.select('.dropdown dl dd')[:-1]
            old = soup.select('.dropdown dl dd')[-1].select('a')[0]['href']
            data_list = []
            for now in nows:
                year = now.select('a')[0].get_text().strip()
                if "未上市" in year:
                    year = year.split('\n')
                    data_list.append([year[0],"3000",'未上市'])
                else:
                    year_url = "https://www.autohome.com.cn" + now.select('a')[0]['href']
                    browser.get(year_url)
                    soup = BeautifulSoup(browser.page_source,'lxml')
                    cs_url = "https:" + soup.select('#navTop ul li')[1].select('a')[0]['href']
                    browser.get(cs_url)
                    html = etree.HTML(browser.page_source)
                    prices = html.xpath('//div[@class="conbox"]/table[1]/tbody/tr[1]/td/div/text()')
                    price = min(prices) + "-" + max(prices)
                    point = html.xpath('//div[@class="conbox"]/table[2]/tbody/tr[5]/th/div/span/text()')[0]
                    if "上市" in point:
                        times = html.xpath('//div[@class="conbox"]/table[2]/tbody/tr[5]/td/div/text()')
                        time = min(times)
                    else:
                        time = "无"
                    cla = html.xpath('//div[@class="conbox"]/table[2]/tbody/tr[4]/td[1]/div/text()')[0]
                    data_list.append([year,time,price,'在售'])
            time_list = [data[1] for data in data_list]
            if min(time_list) > "2017.11":
                if "###" in old:
                    pass
                else:
                    old_url = "https://www.autohome.com.cn" + soup.select('.dropdown dl dd')[-1].select('a')[0]['href']
                    browser.get(old_url)
                    html = etree.HTML(browser.page_source)
                    year = html.xpath('/html/body/div[2]/div[3]/div[1]/div/div/ul/li[1]/a/text()')[0]
                    cs_data = html.xpath('//*[@id="tab1-1"]/div/div[1]/div[2]/a[2]/@href')[0].split('/')
                    cs_url = "https://car.autohome.com.cn/config/series/" + cs_data[0] + "-" + cs_data[1] +".html"
                    browser.get(cs_url)
                    html = etree.HTML(browser.page_source)
                    prices = html.xpath('//div[@class="conbox"]/table[1]/tbody/tr[1]/td/div/text()')
                    price = min(prices) + "-" + max(prices)
                    point = html.xpath('//div[@class="conbox"]/table[2]/tbody/tr[5]/th/div/span/text()')[0]
                    if "上市" in point:
                        times = html.xpath('//div[@class="conbox"]/table[2]/tbody/tr[5]/td/div/text()')
                        time = min(times)
                    else:
                        time = "无"
                    cla = html.xpath('//div[@class="conbox"]/table[2]/tbody/tr[4]/td[1]/div/text()')[0]
                    data_list.append([year,time,price,'停售'])
            data = [jb,pp_name,cj_name,cx_name,cla,data_list]
            save_data(data)
                
def save_data(data):
    f = open('C:/Users/wyl/Desktop/test.csv','a',newline='')
    csv_write = csv.writer(f,dialect='excel')
    csv_write.writerow(data)
            
           
    
    
if __name__ == "__main__":
    point_list = ['a00','a0','a','b','c','d','suva0','suva','suvb','suvc','suvd','mpv','s','p']
    for point in point_list:
        if point == "a00":
            jb = "微型车"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "a0":
            jb = "小型车"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "a":
            jb = "紧凑型车"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "b":
            jb = "中型车"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "c":
            jb = "中大型车"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "d":
            jb = "大型车"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "suva0":
            jb = "小型suv"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "suva":
            jb = "紧凑型suv"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "suvb":
            jb = "中型suv"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "suvc":
            jb = "中大型suv"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "suvd":
            jb = "大型suv"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "mpv":
            jb = "MPV"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "s":
            jb = "跑车"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'
        elif point == "p":
            jb = "皮卡"
            url = 'https://www.autohome.com.cn/' +point + '/1_1-0.0_0.0-0-0-0-0-0-0-0-0/'    
        for uibox in get_one(url):
            for pp in get_two(uibox):
                data = get_three(pp,jb)
        
    


