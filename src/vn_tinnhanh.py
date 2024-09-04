from datetime import datetime
from pprint import pprint as pp

import pandas as pd
import requests
from bs4 import BeautifulSoup

# url = "https://www.tinnhanhchungkhoan.vn/doanh-nghiep/"


def get_news_tinnhanhck(url: str):
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, features="html.parser")

    df = []
    # =================================================================================
    # GET TOP NEWS (RANK 1)
    # =================================================================================
    rank_1 = soup.find("div", class_="rank-1")
    a1_tag = rank_1.find("h2", class_="story__heading")
    a1_title = a1_tag.find("a")["title"]
    a1_link = a1_tag.find("a")["href"]

    a1_time = rank_1.find("div", class_="story__meta").text.strip()
    publish_time = datetime.strptime(a1_time, "%d/%m/%Y %H:%M")

    df.append({"TITLE": a1_title, "LINK": a1_link, "PUBLISHED_DATE": publish_time})

    # =================================================================================
    # GET NEWS (RANK 2)
    # =================================================================================
    rank_2 = soup.find("div", class_="rank-2")
    articles_2 = rank_2.find_all("article", class_="story")

    for article in articles_2:
        a2_tag = article.find("h2", class_="story__heading")
        a2_title = a2_tag.find("a")["title"]
        a2_link = a2_tag.find("a")["href"]

        a2_time = article.find("div", class_="story__meta").text.strip()
        publish_time = datetime.strptime(a2_time, "%d/%m/%Y %H:%M")

        df.append({"TITLE": a2_title, "LINK": a2_link, "PUBLISHED_DATE": publish_time})

    # =================================================================================
    # GET NEWS (RANK 3)
    # =================================================================================
    rank_3 = soup.find("div", class_="box-content content-list")
    articles_3 = rank_3.find_all("article", class_="story")

    for article in articles_3:
        a3_tag = article.find("h2", class_="story__heading")
        a3_title = a3_tag.find("a")["title"]
        a3_link = a3_tag.find("a")["href"]

        a3_time = article.find("div", class_="story__meta").text.strip()
        publish_time = datetime.strptime(a3_time, "%d/%m/%Y %H:%M")

        df.append({"TITLE": a3_title, "LINK": a3_link, "PUBLISHED_DATE": publish_time})

    df = pd.DataFrame(df)
    return df


if __name__ == "__main__":
    url = "https://www.tinnhanhchungkhoan.vn/doanh-nghiep/"

    df = get_news_tinnhanhck(url=url)

    print(df)
