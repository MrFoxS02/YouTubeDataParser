### YouTubeDataParser
A class for extracting data from YouTube channels. You can use it for your data science projects in order to conduct various kinds of statistical analysis.

### Use example

```python
from youtubescraper import *
import pandas as pd

URL = ["https://www.youtube.com/@ros8970", "https://www.youtube.com/@FeelBro"]
scraper = YoutubeScraper(URL, 5)
channel_data, video_data = scraper.get_video_data()

video_data_df = pd.DataFrame(video_data)
channel_data_df = pd.DataFrame(channel_data)
video_data_df["Publication_data"] = pd.to_datetime(video_data_df['Publication_data'])
video_data_df.head(3)
channel_data_df.head()

```
### Results

<table border="1" bordercolor="grey">
<caption>video_data_df.head(3)</caption>
<tr> <th>Chanal_name</th> <th>Titles</th> <th>Views</th> <th>Description</th> <th>Publication_data	</th> <th>URL</th> </tr> 
<tr> <td>Нейros</td> <td>Программирование робота...</td> <td>571</td> <td>Поддержка проекта...</td> <td>2021-05-31</td> <td>https://www.youtube.com/watch?v=...</td> </tr> 
<tr> <td>Нейros</td> <td>Создание модели робота...</td> <td>504</td> <td>Поддержка проекта...</td> <td>2021-05-26</td> <td>https://www.youtube.com/watch?v=...</td> </tr> 
<tr> <td>FeelBro</td> <td>КАК ТИКТОКЕРША СТАЛА...</td> <td>99539</td> <td>Успей купить...</td> <td>2024-01-27</td> <td>https://www.youtube.com/watch?v=...</td> </tr> 
</table>

<table border="1" bordercolor="grey">
<caption>hannel_data_df.head()</caption>
<tr> <th>Chanal_name</th> <th>subscribers</th> <th>chanel_tag</th> <th>number of videos per channel</th> </tr> 
<tr> <td>Нейros</td> <td>78</td> <td>Education</td> <td>11</td> </tr> 
<tr> <td>FeelBro</td> <td>182000</td> <td>People &amp; Blogs	</td> <td>102</td> </tr> 
</table>

