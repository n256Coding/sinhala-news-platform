import datetime

from bs4 import BeautifulSoup
import requests


class Spider:

    def crowl(self, date: datetime = None):
        news_link_list = self.__load_todays_news_list()
        for news_link in news_link_list:
            page_html_response = self.__load_page(news_link)
            heading, content, timestamp = self.__parse_news_page(page_html_response)

    def __load_todays_news_list(self):
        url = f"https://sinhala.adaderana.lk/sinhala-hot-news.php?pageno={1}"
        response = requests.get(url, headers={
            'User-Agent': 'PostmanRuntime/7.39.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Accept': '*/*',
        })

        # div.news-story:nth-child(26) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)
        soup = BeautifulSoup(response.content, 'html.parser')
        story_texts = soup.select('div.news-story > div.story-text')
        links = []

        for story in story_texts:
            anchor = story.select('h2 > a')
            links.append(f'https://sinhala.adaderana.lk/{anchor[0]["href"]}')
        
        return links

    def __load_page(self, url):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': '_gid=GA1.2.1653110678.1717174201; _fbp=fb.1.1717174203676.1725022162; PHPSESSID=14c8qmvalfes6911a5sj8oajv0; AWSALB=c7ZODjObrxvFaKgLeD2wBsr4K2uClNVyEqwGvdmZdj8kQJ7zSpT4whvz/w+PgJY5BTOuAhj1SLrzGCYl5+HcZPK27+toKcd0h6m6+5JrKdg47nuDg7bc2V9ABD8X; __gads=ID=2e58620b51e9efef:T=1717174204:RT=1717178666:S=ALNI_MYGlu4wBvTF3WHWnZY7qwxxyovT9Q; __gpi=UID=00000e38d29b357d:T=1717174204:RT=1717178666:S=ALNI_MYRcq40O-xAnClttF6eS1DxhZBubw; __eoi=ID=b0fd7d55940f9669:T=1717174204:RT=1717178666:S=AA-AfjYGfJuwN6W0Ap4ODBmTTjOR; _ga_NTDE7CCHZ8=GS1.1.1717178666.2.0.1717178666.60.0.0; _ga=GA1.1.1034007929.1717174201; _ga_D88CRC88HS=GS1.1.1717178666.2.0.1717178666.60.0.0; _ga_W9DVK73Q0S=GS1.1.1717178666.2.0.1717178666.60.0.0; cto_bundle=X56B1V9nYlhTcmRBUDhsR2ZzWlg5RlhIMmJuJTJCczk2aTZTclN1Q0tqa1hNcTY1cDQ2VEg1bDlXZUU0RWtUcFdud2VmZHg4JTJCbU95cjBmSmxJMHFFbjIyazJjY3BLQ2dNZFcyajZvVkduVSUyRmpoNEVBJTJGQWc1eTd2UlBmQzhwbzJJODlBamRDMndQT04wZUQxbThEZjU1MkJVYzNUZyUzRCUzRA',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        }

        response = requests.get(url, headers=headers)

        return response

    def __parse_news_page(self, response) -> tuple:
        soup = BeautifulSoup(response.content, 'html.parser')

        heading_element = soup.select_one('h1.news-heading')
        content_element = soup.select_one('div.news-content')
        content_timestamp = soup.select_one('p.news-timestamp')

        lines = content_element.text.strip().split('\r\n')
        stripped_content = ' '.join([line for line in lines if line])

        return heading_element.text, stripped_content, content_timestamp
    