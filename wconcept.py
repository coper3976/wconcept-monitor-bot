#-*-encoding:utf8:-*-
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from discord_hooks import Webhook
import json
import urllib3
urllib3.disable_warnings()

my_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'accept': 'application/json, text/javascript, */*; q=0.01'
}

print(">>> Start Parsing")
resp = requests.get('https://www.wconcept.co.kr/Search?type=direct&kwd=%EC%A1%B0%EB%8D%98', headers=my_header)
resp.encoding = ''
bs = BeautifulSoup(resp.text, 'lxml')

soup = bs.find('div',class_='thumbnail_list')
divs = soup.find_all('li')

for div in divs:
    img = "https://" + div.find('div', class_='img').img['src'].lstrip('//').replace('?RS=300', '')
    title = div.find('div', class_='product ellipsis multiline').text.strip()
    price = div.find('span', class_='discount_price').text.strip()
    productLink = 'https://www.wconcept.co.kr' + div.find('a', class_='')['href'].strip().replace('?rccode=pc_search', '')
    
if __name__ == "__main__":
    ''' --------------------------------- Main --------------------------------- '''
    MONITOR_DELAY = 5
    # 기존 상품정보 가져오기
    print("DB 생성중...")
    resp = requests.get('https://www.wconcept.co.kr/Search?type=direct&kwd=%EC%A1%B0%EB%8D%98', headers=my_header)
    resp.encoding = ''
    bs = BeautifulSoup(resp.text, 'lxml')

    soup = bs.find('div',class_='thumbnail_list')
    divs = soup.find_all('li')
    product_db = dict()

    for div in divs:
        img = "https://" + div.find('div', class_='img').img['src'].lstrip('//').replace('?RS=300', '')
        title = div.find('div', class_='product ellipsis multiline').text.strip()
        price = div.find('span', class_='discount_price').text.strip()
        productLink = 'https://www.wconcept.co.kr' + div.find('a', class_='')['href'].strip().replace('?rccode=pc_search', '')   
        product_db[title] = [title, price, img, productLink] 

    #테스트
    product_db.pop('조던 슈즈 스케이트보더 레서 팬다 머플러 [ BLACK ]')

    #모니터링 시작
    print("<모니터링 시작>")
    for loopCnt in tqdm(range(int(3))):
        resp = requests.get('https://www.wconcept.co.kr/Search?type=direct&kwd=%EC%A1%B0%EB%8D%98', headers=my_header)
        resp.encoding = ''
        bs = BeautifulSoup(resp.text, 'lxml')
        soup = bs.find('div',class_='thumbnail_list')
        divs = soup.find_all('li')

        for div in divs:
            img = "https://" + div.find('div', class_='img').img['src'].lstrip('//').replace('?RS=300', '')
            title = div.find('div', class_='product ellipsis multiline').text.strip()
            price = div.find('span', class_='discount_price').text.strip()
            productLink = 'https://www.wconcept.co.kr' + div.find('a', class_='')['href'].strip().replace('?rccode=pc_search', '')
            
            product_db[4] = [title, price, img, productLink] 
            if title not in product_db.keys():
                product_db[title] = [title, price, img, productLink]
                print("제품명 :", title, "가격 :", price, "제품 링크 :", productLink, "제품 사진 :", img)
        time.sleep(MONITOR_DELAY)

