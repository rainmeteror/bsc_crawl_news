from pprint import pprint as pp
import pandas as pd
import urllib3
import datetime as dt

import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def news_dbtt(source_url: str, source_path = str):
    r = requests.get(url=source_url, headers=headers, verify=False)
    
    if r.status_code == 200:
        df = []
        for i in range(0, 3):
            url = f"https://dubaotiente.io/tieu-diem-thi-truong.html?page={i}"

            r = requests.get(url=url, headers=headers, verify=False)
            soup = BeautifulSoup(r.content, features="html.parser")
            articles = soup.find_all('article', class_='story focus-item btn-link click-href')

            for article in articles:    
                title = article.find('h2', class_='detail__title').text.strip()
                time = article.find('div', class_="detail__meta").text.strip()
                contents = article.find('div', class_="detail__content").text.strip()

                df_dict = {
                    "TITLE": title,
                    "TIME": time,
                    "CONTENTS": contents
                }
                
                df.append(df_dict)
                
        df = pd.DataFrame(df)
        df.to_excel(source_path)
        print("Finish")
    else:
        print("We cannot access the website.")
        
if __name__ == "__main__":
    print("1. Start")
    print("2. Processing...")
    news_dbtt(
        source_url="https://dubaotiente.pro/tieu-diem-thi-truong.html",
        source_path=r"V:\09. Báo cáo team VMTT\2. Bình thường\Data\NEWS_DBTT_LASTEST.xlsx"
    )
    print("Saving...")
    print("Finish successfully.")