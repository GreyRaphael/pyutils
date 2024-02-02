import httpx
import asyncio
import random


class EtfShDownloader:
    def __init__(self):
        self._client = httpx.AsyncClient()
        self._headers = self._generate_headers()

    def _generate_headers(self) -> dict:
        num = random.randint(90, 120)
        return {
            "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{num}.0) Gecko/20100101 Firefox/{num}.0",
            "Referer": "http://www.sse.com.cn/",
        }

    async def _fetch_url(self, url) -> dict:
        response = await self._client.get(url, headers=self._headers, timeout=None)
        return response.text

    async def _fetch_urls(self, urls: list):
        tasks = [self._fetch_url(url) for url in urls]
        return await asyncio.gather(*tasks)

    def _craw_etf_list(self) -> dict:
        """获取ETF列表, source: http://www.sse.com.cn/assortment/fund/etf/list/"""
        # subClass=01, 沪ETF
        # subClass=03, 沪深京ETF
        # subClass=08, 沪深港京ETF
        # subClass=09, 科创板ETF
        # subClass=31, 科创板plus ETF
        subclass_list = ["01", "03", "08", "09", "31"]
        url_list = [f"http://query.sse.com.cn/commonSoaQuery.do?jsonCallBack=jsonpCallback87795546&sqlId=FUND_LIST&fundType=00&subClass={subc}" for subc in subclass_list]
        txt_list = asyncio.run(self._fetch_urls(url_list))
        etf_list = []
        null = None
        for txt in txt_list:
            j_data = eval(txt[22:-1])
            code_list = [record["fundCode"] for record in j_data["result"]]
            etf_list.extend(code_list)
        return etf_list


if __name__ == "__main__":
    sh_downloader = EtfShDownloader()
    etfs = sh_downloader._craw_etf_list()
    print(etfs)