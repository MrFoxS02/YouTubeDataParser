import youtube_dl
import requests
from bs4 import BeautifulSoup
import re, datetime


class YoutubeScraper:
    def __init__(self, url:list, entries:int=0):
        self.url = [u + "/videos" for u in url]
        self.entries = entries # Максималльное количество извлекаемых с канала записей, если стоит 0, то забираются все
        self.video_count = 0

    def __get_video_ids(self, url:str)->list:
        ydl_opts = {'extract_flat': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Извлекаем информацию о видео по URL
            result = ydl.extract_info(url, download=False)
            # Проверяем, есть ли видео в результате
            if 'entries' in result:
                 # Если есть, извлекаем ID каждого видео и добавляем его в список
                video_ids = [entry['id'] for entry in result['entries']]
                self.video_count = len(video_ids)
                return video_ids
            else:
                return []
    
    def get_video_url_data(self, url:str)->list:
        """Из извлечённых URL_ID формируем ссылки на видео"""
        url_ids = self.__get_video_ids(url)
        return ["https://www.youtube.com/watch?v=" + id for id in url_ids]
    
    def __subscribers_prepare(self, subscriber:str)->float:
        """Переводим категориальные данные в числовые"""
        replace_data = {"тыс":1000, "млн":1000000}
        sub = list(subscriber.split(" "))
        sub[0] = sub[0].replace(',', '.') if ',' in sub[0] else sub[0]
        category = replace_data.get(sub[1][:3], 1)
        return int(float(sub[0]) * category)


    def get_video_data(self)->dict:
        """Формирование данных со статистикой по каналу"""

        video_data = [[], [], [], [], [], []]
        channel_data = [[], [], [], []]

        for url in self.url:   
            video_url_list = self.get_video_url_data(url)

            for id,  video_url in enumerate(video_url_list[:len(video_url_list)-2]):
                resp = requests.get(video_url)
                soup = BeautifulSoup(resp.content, 'html.parser', from_encoding='utf-8')

                if id == 0:
                    chanel_name = soup.find("span", itemprop="author").next.next['content']
                    channel_data[0].append(chanel_name)
                    text = resp.text
                    pattern = r'"subscriberCountText".*?"label":"(.*?)"'
                    subscribers = re.findall(pattern, text)[0]
                    channel_data[1].append(self.__subscribers_prepare(subscribers))
                    chanel_tag = soup.find_all('meta', itemprop='genre')
                    channel_data[2].append(re.search(r'tent="(.*?)" itemprop', str(chanel_tag)).group(1))
                    channel_data[3].append(self.video_count)

                # Получение данных о видео на канале
                video_data[0].append(soup.select_one("meta[itemprop='name'][content]")["content"])
                video_data[1].append(soup.select_one("meta[itemprop='interactionCount'][content]")["content"])
                video_data[2].append(soup.find('meta', itemprop='description')['content'])
                data = soup.find('meta', itemprop='datePublished')['content']
                video_data[3].append(str(datetime.datetime.fromisoformat(data)).split(" ")[0])
                video_data[4].append(chanel_name)
                video_data[5].append(video_url)

                if (id == self.entries or id >= len(video_url_list)) and self.entries != 0:
                    break
            
        channel_dataframe = {"Chanal_name":channel_data[0], "subscribers":channel_data[1], 
                            "chanel_tag":channel_data[2], "number of videos per channel":channel_data[3]}

        video_dataframe = {
            "Chanal_name":video_data[4],
            "Titles":video_data[0],
            "Views":video_data[1],
            "Description":video_data[2],
            "Publication_data":video_data[3],
            "URL":video_data[5]}
    
        return channel_dataframe, video_dataframe