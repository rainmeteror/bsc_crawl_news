from datetime import datetime
from pprint import pprint as pp
import urllib3

import pandas as pd
import requests
from bs4 import BeautifulSoup


urllib3.disable_warnings()

class GetNewsVnEconomy:
    
    def __init__(self, base: str) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        self.base = base
    
    def _get_subheader_news(self, end_point_links: str):
        url = self.base + end_point_links
        
        r = requests.get(url=url, headers=self.headers, verify=False)
        soup = BeautifulSoup(r.content, features="html.parser")
        
        subhead = soup.find("h2", class_="detail__summary").get_text().strip()
        
        return subhead
    
    def get_news(self, end_point_url: str):
        url = self.base + "/" + end_point_url
        
        r = requests.get(url=url, headers=self.headers, verify=False)
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
        subhead = self._get_subheader_news(end_point_links=top_news_href)
        
        df.append(
            {
                "TITLE": top_news_title,
                "SUBHEAD": subhead,
                "LINK": self.base + top_news_href 
            }
        )
        
        # =================================================================================
        # GET TOP NEWS (RANK 2)
        # =================================================================================
        second_col = highlights.find("div", class_="row")
        news_3 = second_col.find_all("div", class_="col-md-6")
        
        for news in news_3[:-1]:
            new = news.find("figure", class_="story__thumb")
            title = new.find("a")["title"]
            link = new.find("a")["href"]
            subhead = self._get_subheader_news(end_point_links=link)

            df.append(
                {
                    "TITLE": title, 
                    "SUBHEAD": subhead,
                    "LINK": self.base + link
                }
            )
            
        # =================================================================================
        # GET TOP NEWS (RANK 3)
        # =================================================================================
        news_4 = soup.find_all("article", class_="story story--featured story--timeline")

        for news in news_4[1:]:
            new = news.find("h3", class_="story__title")

            title = new.find("a")["title"]
            link = new.find("a")["href"]
            subhead = self._get_subheader_news(end_point_links=link)
            publish_time = news.find("div", class_="story__meta").text

            df.append(
                {
                    "TITLE": title, 
                    "SUBHEAD": subhead,
                    "LINK": self.base + link, 
                    "PUBLISHED_DATE": publish_time
                }
            )
        
        df = pd.DataFrame(df)
        
        return df

def get_news_vneconomy(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    r = requests.get(url=url, headers=headers, verify=False)
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
    # GET TOP NEWS (RANK 2)
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

    news = GetNewsVnEconomy(base=base)
    
    with pd.ExcelWriter(
        # r"V:\09. Báo cáo team VMTT\2. Bình thường\Data\MORNING_NEWS\VN_ECONOMY.xlsx",
        r"C:\Users\tungtt1\OneDrive - Cong ty Co Phan Chung Khoan Ngan Hang Dau Tu va Phat trien Viet Nam\Team VMTT\Morning\DATA_NEWS\VN_ECONOMY.xlsx",
        engine="openpyxl",
    ) as writer:
        for i in end_url:
            df = news.get_news(end_point_url=i)
            print(f"Saving {i}")
            print(df)
            df.to_excel(writer, sheet_name=i, index=False)