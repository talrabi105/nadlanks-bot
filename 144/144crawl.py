import pandas as pd
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote

class AddressException(Exception):
    pass

def split_to_list(s):
    return list(filter(None, re.split(r'(\d+)', s)))

def check_address(address):
    address=address.strip()
    if address != "כפר סבא" or address == "" or address == " ":
        return True
    return False


def parse_address(card):
    address=card.find("div",{"class":"card-address"}).getText()
    if  not check_address(address):
        return False

    house_address = address.split(",")[0]
    house_address=house_address.strip()
    return split_to_list(house_address)



def get_name_from_card(card):
    return card.find("h4", {"class": "card-title"}).getText().strip()

def get_link_from_card(card):
    return card.find("h4", {"class": "card-title"}).find("a",href=True)["href"]

def parse_one(data):
    art=data.find("article",{"class":"cardPrivate"})
    right=art.find("div",{"class":"card-top"}).find("div",{"class":"card-right"}).find("div",{"class":"cardDescription"})
    data_d={}
    adress=parse_address(right)
    if adress==False:
        raise AddressException()


    data_d["שם"]=get_name_from_card(right)
    data_d["רחוב"] = adress[0].strip()
    data_d["מספר בית"] = adress[1].strip()
    data_d["לינק"]=get_link_from_card(right)
    return data_d


def parse_search(data):
    result=[]
    all_cards=data.find_all("li",{"class":"card-list-item"})
    for card in all_cards:
        try:
            result.append(parse_one(card))
        except AddressException:
            print("bad adress passing")
            continue
    return result
u2 = urlopen('https://private.b144.co.il/PrivateResults.aspx?p_city=%D7%9B%D7%A4%D7%A8%20%D7%A1%D7%91%D7%90&p_name=%D7%A2%D7%93%D7%99')
a = unquote(u2.read().decode('utf-8'))

soup = BeautifulSoup(a, 'html.parser')
data=parse_search(soup)
df=pd.DataFrame.from_records(data)
df.to_csv("test.csv",index=False,encoding = 'utf-8-sig')