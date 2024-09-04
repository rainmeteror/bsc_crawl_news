from datetime import datetime
from pprint import pprint as pp

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://vneconomy.vn/kinh-te-the-gioi.htm"
# url = "https://vneconomy.vn/dia-oc.htm"
# url = "https://vneconomy.vn/chung-khoan.htm?trang=1"


def get_news_vneconomy(url: str):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")

    df = []
    # =================================================================================
    # GET TOP NEWS (RANK 1)
    # =================================================================================
    highlights = soup.find("section", class_="zone zone--highlight")
    first_col = highlights.find("div", class_="col-12 col-lg-6")

    top_news = first_col.find("figure", class_="story__thumb")
    top_news_title = top_news.find("a")["title"]
    top_news_href = top_news.find("a")["href"]

    df.append({"TITLE": top_news_title, "LINK": top_news_href})

    # =================================================================================
    # GET TOP NEWS (RANK 1)
    # =================================================================================
    second_col = highlights.find("div", class_="row")
    news_3 = second_col.find_all("div", class_="col-md-6")

    for news in news_3[:-1]:
        new = news.find("figure", class_="story__thumb")
        title = new.find("a")["title"]
        link = new.find("a")["href"]

        df.append({"TITLE": title, "LINK": link})

    # =================================================================================
    # GET TOP NEWS (RANK 3)
    # =================================================================================
    news_4 = soup.find_all("article", class_="story story--featured story--timeline")

    for news in news_4[1:]:
        new = news.find("h3", class_="story__title")

        title = new.find("a")["title"]
        link = new.find("a")["href"]
        publish_time = news.find("div", class_="story__meta").text

        df.append({"TITLE": title, "LINK": link, "PUBLISHED_DATE": publish_time})

    df = pd.DataFrame(df)

    return df


if __name__ == "__main__":
    base = "https://vneconomy.vn"
    end_url = ["tieu-diem.htm", "dau-tu.htm", "tai-chinh.htm", "kinh-te-the-gioi.htm"]

    with pd.ExcelWriter(
        r"/Users/rainmeteror/bsc_daily_morning/src/data/vn_economy.xlsx",
        engine="openpyxl",
    ) as writer:
        for i in end_url:
            url = base + "/" + i

            df = get_news_vneconomy(url=url)
            print(f"Saving {i}")

            df.to_excel(writer, sheet_name=i, index=False)
