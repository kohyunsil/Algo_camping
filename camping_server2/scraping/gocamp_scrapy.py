import requests
import re
import pandas as pd
from scrapy.http import TextResponse


class GocampCrawl:

    def view_crawler(self):
        url = "https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=3000&searchKrwd=&listOrdrTrget=last_updusr_pnttm"

        req = requests.get(url)
        response = TextResponse(req.url, body=req.text, encoding="utf-8")
        link = str(response.xpath('//*[@id="cont_inner"]/div/div/ul/li/div/a/@href').extract()).replace('read01', '')
        contentId = re.findall("\d+", link)
        view = str(response.xpath('//*[@id="cont_inner"]/div/div/ul/li/div/div/p/span[3]/text()').extract())
        view = re.findall("\d+", view)
        readcount = pd.concat([pd.DataFrame(contentId), pd.DataFrame(view)], 1)
        readcount.columns = ['content_Id', 'readcount']

        return readcount

if __name__ == '__main__':
    c = GocampCrawl()
    c.view_crawler()
