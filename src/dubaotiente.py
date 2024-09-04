from datetime import datetime
from pprint import pprint as pp

import pandas as pd
import requests
from bs4 import BeautifulSoup


class GET_NEWS_DBTT:

    def __init__(self, url: str):
        self.url = url

    def _get_content_dbtt(self, links: str):
        r = requests.get(url=links)
        soup = BeautifulSoup(r.content, features="html.parser")

        news_detail = soup.find("div", class_="zone__content")
        contents = news_detail.find("div", class_="detail__content")

        text_df = []
        # Extract the text from the p elements
        p_elements = contents.find_all("p")
        for p in p_elements:
            text_df.append(p.text.strip())
            # print(p.text.strip())

        # Extract the text from the li elements
        li_elements = contents.find_all("li")
        for li in li_elements:
            text_df.append(li.text.strip() + "\n")
            # print(li.text.strip())

        texts = " ".join(text_df)
        return texts

    def get_news(self):
        df = []
        r = requests.get(url=self.url)
        soup = BeautifulSoup(r.content, features="html.parser")

        spot_lights = soup.find("div", id="tab-all")
        spots = spot_lights.find_all("a", class_="focus-item")

        for i in range(0, len(spots)):
            link = spots[i].get("href")
            title = spots[i].find("h3", class_="detail__title").find("p")["title"]
            published_date = (
                spots[i].find("div", class_="detail__meta").find("time").text.strip()
            )

            content = self._get_content_dbtt(links=link)

            df.append(
                {
                    "PUBLISHED_DATE": published_date,
                    "TITLE": title,
                    "CONTENT": content,
                }
            )

            print(published_date, title, content)
            print("\n")

        df = pd.DataFrame(df)
        return df


if __name__ == "__main__":
    url = "https://dubaotiente.io/"

    obj = GET_NEWS_DBTT(url=url)
    df = obj.get_news()

    print(df)
