from datetime import datetime
from pprint import pprint as pp
import urllib3

import pandas as pd
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings()


class GetNewsVnFinance:
    
    """ An attempt to get news from VietNam Finance """
    
    def __init__(self, base: str) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        self.base = base
        
    def _get_subheader_news(self, links: str):
        r = requests.get(url=links, headers=self.headers, verify=False)
        soup = BeautifulSoup(r.content, features="html.parser")
        
        subhead = soup.find("h2", class_="detail-sapo fs-20 fw-500 mb-20 lh-150 tracking-036").get_text().strip()
        
        return subhead
    
    def get_news(self, end_point_url: str):
        url = self.base + end_point_url + "/"
        r = requests.get(url=url, headers=self.headers, verify=False)
        soup = BeautifulSoup(r.content, features="html.parser")
        
        df = []
        # =================================================================================
        # GET TOP NEWS
        # =================================================================================
        top_news = soup.find("div", class_="article-large")
        head_news = top_news.find("div", class_="article__content pt-10")

        a_tag = head_news.find("a", class_="fix-text3")

        title_text = a_tag.text
        title_href = a_tag.get("href")
        subhead = self._get_subheader_news(links=title_href)

        df.append(
            {
                "TITLE": title_text, 
                "SUBHEAD": subhead,
                # "LINK": self.base + "/" + title_href
                "LINK": title_href
            }
        )
        
        # =================================================================================
        # GET TOP NEWS (TIER 2)
        # =================================================================================
        tier_2_news = soup.find("div", class_="articles-small")
        articles = tier_2_news.find_all("div", class_="article hover-red-8c")

        for article in articles:
            title_news_tier_2 = article.find("a", class_="expthumb image-wrapper")

            tier_2_title = title_news_tier_2.get("title")
            tier_2_href = title_news_tier_2.get("href")
            subhead = self._get_subheader_news(links=tier_2_href)

            df.append(
                {
                    "TITLE": tier_2_title, 
                    "SUBHEAD": subhead,
                    "LINK": tier_2_href
                }
            )
        
        # =================================================================================
        # GET TOP NEWS (TIER 3)
        # =================================================================================
        tier_3_news = soup.find("div", class_="articles d-2xl-grid col-3 gap-20")

        articles_3 = tier_3_news.find_all("div", class_="article hover-red-8c")
        for article in articles_3:
            title_news_tier_3 = article.find(
                "h3", class_="article__title fix-text3 fs-17 lh-130 fw-700 hover-red-8c"
            )

            tier_3_tile = title_news_tier_3.text
            tier_3_href = title_news_tier_3.find("a")["href"]
            subhead = self._get_subheader_news(links=tier_3_href)

            df.append(
                {
                    "TITLE": tier_3_tile, 
                    "SUBHEAD": subhead,
                    "LINK": tier_3_href
                }
            )
            
        # =================================================================================
        # GET TOP NEWS (TIER 4)
        # =================================================================================
        tier_4_box = soup.find("div", class_="cate-box-two")
        articles_4 = tier_4_box.find_all(
            "div", class_="article d-2xl-flex border-b-e5 py-20 article_last"
        )

        for article in articles_4:
            last_push = datetime.strptime(article.get("last-push"), "%Y-%m-%d %H:%M:%S")

            a_tag = article.find("a", class_="expthumb image-wrapper")
            tier_4_title = a_tag.get("title")
            tier_4_href = a_tag.get("href")
            subhead= self._get_subheader_news(links=tier_4_href)

            df.append(
                {
                    "PUBLISHED_DATE": last_push, 
                    "TITLE": tier_4_title, 
                    "SUBHEAD": subhead,
                    "LINK": tier_4_href
                }
            )
        
        df = pd.DataFrame(df)
        
        return df

def get_news_vietnam_finance(url: str):
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, features="html.parser")

    # =================================================================================
    # MAKE AN EMPTY DICT
    # =================================================================================
    df = []

    # =================================================================================
    # GET TOP NEWS
    # =================================================================================
    top_news = soup.find("div", class_="article-large")
    head_news = top_news.find("div", class_="article__content pt-10")

    a_tag = head_news.find("a", class_="fix-text3")

    title_text = a_tag.text
    title_href = a_tag.get("href")

    df.append({"TITLE": title_text, "LINK": title_href})

    # =================================================================================
    # GET TOP NEWS (TIER 2)
    # =================================================================================
    tier_2_news = soup.find("div", class_="articles-small")
    articles = tier_2_news.find_all("div", class_="article hover-red-8c")

    for article in articles:
        title_news_tier_2 = article.find("a", class_="expthumb image-wrapper")

        tier_2_title = title_news_tier_2.get("title")
        tier_2_href = title_news_tier_2.get("href")

        df.append({"TITLE": tier_2_title, "LINK": tier_2_href})

    # =================================================================================
    # GET TOP NEWS (TIER 3)
    # =================================================================================
    tier_3_news = soup.find("div", class_="articles d-2xl-grid col-3 gap-20")

    articles_3 = tier_3_news.find_all("div", class_="article hover-red-8c")
    for article in articles_3:
        title_news_tier_3 = article.find(
            "h3", class_="article__title fix-text3 fs-17 lh-130 fw-700 hover-red-8c"
        )

        tier_3_tile = title_news_tier_3.text
        tier_3_href = title_news_tier_3.find("a")["href"]

        df.append({"TITLE": tier_3_tile, "LINK": tier_3_href})

    # =================================================================================
    # GET TOP NEWS (TIER 4)
    # =================================================================================
    tier_4_box = soup.find("div", class_="cate-box-two")
    articles_4 = tier_4_box.find_all(
        "div", class_="article d-2xl-flex border-b-e5 py-20 article_last"
    )

    for article in articles_4:
        last_push = datetime.strptime(article.get("last-push"), "%Y-%m-%d %H:%M:%S")

        a_tag = article.find("a", class_="expthumb image-wrapper")
        tier_4_title = a_tag.get("title")
        tier_4_href = a_tag.get("href")

        df.append(
            {"PUBLISHED_DATE": last_push, "TITLE": tier_4_title, "LINK": tier_4_href}
        )

    df = pd.DataFrame(data=df)

    return df


if __name__ == "__main__":
    base_url = "https://vietnamfinance.vn/"
    end_url = ["tai-chinh-quoc-te", "tieu-diem", "ngan-hang", "bat-dong-san", "dau-tu"]

    news = GetNewsVnFinance(base=base_url)
    with pd.ExcelWriter(
        # r"V:\09. Báo cáo team VMTT\2. Bình thường\Data\MORNING_NEWS\VN_FINANCE.xlsx",
        r"C:\Users\tungtt1\OneDrive - Cong ty Co Phan Chung Khoan Ngan Hang Dau Tu va Phat trien Viet Nam\Team VMTT\Morning\DATA_NEWS\VN_FINANCE.xlsx",
        engine="openpyxl",
    ) as writer:
        for i in end_url:
            df = news.get_news(end_point_url=i)
            print(f"Saving {i}")

            df.to_excel(writer, sheet_name=i, index=False)
    
    print(df)