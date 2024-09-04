from datetime import datetime
from pprint import pprint as pp

import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = "https://vietnamfinance.vn/"
end_url = ["tai-chinh-quoc-te", "tieu-diem", "ngan-hang", "bat-dong-san", "dau-tu"]


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

    with pd.ExcelWriter(
        r"/Users/rainmeteror/bsc_daily_morning/src/data/vn_finance.xlsx",
        engine="openpyxl",
    ) as writer:
        for i in end_url:
            url = base_url + i + "/"

            df = get_news_vietnam_finance(url=url)
            print(f"Saving {i}")

            df.to_excel(writer, sheet_name=i, index=False)
