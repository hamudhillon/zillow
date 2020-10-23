import os
import pandas as pd
from pprint import pprint as pp
import json
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import xlwt
import xlrd
import time


# soup=BeautifulSoup(driver.page_source,u'html.parser')
session = HTMLSession()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Referer': 'https://www.zillow.com/homedetails/949-W-Hawthorn-St-APT-32-San-Diego-CA-92101/67712352_zpid/',
    'content-type': 'text/plain',
    'Origin': 'https://www.zillow.com',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

# rb = xlrd.open_workbook(input_filename) 
# sheet = rb.sheet_by_index(0)
row=0
running_city=[]
main_arr=[]
# pagination=str('{"pagination":"currentPage":1}')
# url='https://www.zillow.com/san-diego-ca/condos/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-117.23793983459473%2C%22east%22%3A-117.10301399230957%2C%22south%22%3A32.68056297457832%2C%22north%22%3A32.770821270041424%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A54296%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22wat%22%3A%7B%22value%22%3Atrue%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D'
def zillow_get(url):
    r =session.get(url,headers=headers)

    # print(r.html.absolute_links)
    # g_resp=requests.get(link,headers=headers)
    soup=BeautifulSoup(r.content,u'html.parser')
    # print(soup)
    list_results_arr=[]
    list_results=soup.find('div',attrs={'id':'grid-search-results'}).find('ul',attrs={'class':'photo-cards'}).findAll('a',attrs={'class':'list-card-link'})
    for l in list_results:
        try:
            # print(l['href'])
            if 'homedetails' in l['href']:
                list_results_arr.append(l['href'])
            
        except:
            continue
    print(len(list_results_arr))
    for lists in list_results_arr:
        # print(lists)
        try:
            list_link=lists
            # ld_json=lists.find('script')
            print(list_link)
            zpid=list_link.split('_zpid/')[0].split('/')[-1]
            # print(zpid)
            con = session.get(
                list_link, headers=headers)
        
            soup = BeautifulSoup(con.text, u"html.parser")
            main_arr=[]
            s=con.html.find('#hdpApolloPreloadedData',first=True)
            scc=str(s.text)
            try:
                print(type(json.loads(scc)))
            except:
                import sys
                print(sys.exc_info())
            
            dataa=json.loads(scc)
            datta=json.loads(dataa['apiCache'])['VariantQuery{\"zpid\":'+str(zpid)+'}']
            data2=json.loads(dataa['apiCache'])['ForSaleDoubleScrollFullRenderQuery{\"zpid\":'+str(zpid)+',\"contactFormRenderParameter\":{\"zpid\":'+str(zpid)+',\"platform\":\"desktop\",\"isDoubleScroll\":true}}']
            
            st_address=datta['property']['streetAddress']
            print(st_address)
            zipcode=datta['property']['zipcode']
            print(zipcode)
            
            city=datta['property']['city']
            print(city)
            state=datta['property']['state']
            print(state)
            price=datta['property']['price']
            print(price)
            bathrooms=datta['property']['bathrooms']
            print(bathrooms)
            bedrooms=datta['property']['bedrooms']
            print(bedrooms)
            
            zestimate=datta['property']['zestimate']
            print(zestimate)
            import datetime
            print(str(data2['property']['datePosted'])[:-3])
            list_date=datetime.datetime.fromtimestamp(int(str(data2['property']['datePosted'])[:-3]))
            print(list_date)
            desc=data2['property']['description']
            pictures=data2['property']['hugePhotos']
            for pic in pictures:
                pic=pic['url']
                print(pic)
            facts=data2['property']['resoFacts']
            print(facts)
            home_fact=data2['property']['homeFacts']
            agent_name=data2['property']['listingProvider']['agentName']
            agent_number=data2['property']['listingProvider']['phoneNumber']
            agent_broke=data2['property']['listingProvider']['postingWebsiteLinkText']
            agent_pic=data2['property']['contactFormRenderData']['data']['contact_recipients'][0]['image_data']['url']
            print(agent_pic)
            main={
             
                "Address":st_address,
                "City":city
            }
            main_arr.append(main)
            print('__________'*30)
            
            break
        except:
            import sys
            print(sys.exc_info())
            continue
    return main_arr
# zillow_get(url)