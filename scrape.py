import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


mainurl = "https://www.bkmkitap.com"
baseurl = "https://www.bkmkitap.com/edebiyat-kitaplari?pg="


def get_pageurl(baseurl, pagenumber):
    urllist = [baseurl + str(page) for page in range(1, pagenumber + 1)]
    return urllist


urllist = get_pageurl(baseurl, 100)


def get_products_url(urllist):
    products_url_list = []
    for ln in urllist:
        soup = get_url(ln)
        products = soup.find_all("div", attrs={
            "class": "col col-3 col-md-4 col-sm-6 col-xs-6 p-right mb productItem zoom ease"})
        for pro in products:
            products_url_list.append(mainurl + pro.a.get("href"))

    return products_url_list


product_url_list = get_products_url(urllist)


def get_attirbute(product_url_list):
    products_detail_list = []
    for ln in product_url_list:
        print(ln)
        soup = get_url(ln)
        text = soup.find("div", attrs={"id": "productDetailTab"}).text.strip()
        title = soup.find("h1", attrs={"id": "productName"}).text.strip()

        tur_column = soup.find_all("div", attrs={"class": "fl col-6"})
        for i in tur_column:
            if i.span.text.strip() == "Türü:":
                tur = i.find_all("span")[1].text.strip()
                print(tur)

        products_detail_list.append([ln, title, tur, text])

    return products_detail_list


details = get_attirbute(product_url_list)


def save_excel(data, name):
    df = pd.DataFrame(data)
    df.columns = ["url", "title", "description"]
    df.to_excel(f"{name}.xlsx")


save_excel(details, "bkmkitap_100")
