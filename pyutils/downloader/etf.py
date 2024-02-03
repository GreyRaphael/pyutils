import asyncio
import random
import os
import json
import csv
import time
import httpx
import re


class EtfShDownloader:
    def __init__(self):
        self._client = httpx.AsyncClient(limits=httpx.Limits(max_connections=20))
        self._headers = self._generate_headers()

    def _generate_headers(self) -> dict:
        num = random.randint(90, 120)
        return {
            "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{num}.0) Gecko/20100101 Firefox/{num}.0",
            "Referer": "http://www.sse.com.cn/",
        }

    async def _fetch_url(self, url) -> dict:
        response = await self._client.get(url, headers=self._headers, timeout=None)
        print(f"==> {url}")
        return response.text

    async def _fetch_urls(self, urls: list):
        tasks = [self._fetch_url(url) for url in urls]
        return await asyncio.gather(*tasks)

    def _craw_etf_list(self) -> dict:
        """获取ETF代码列表, source: http://www.sse.com.cn/assortment/fund/etf/list/"""
        # subClass=01, 沪ETF
        # subClass=03, 沪深京ETF
        # subClass=08, 沪深港京ETF
        # subClass=09, 科创板ETF
        # subClass=31, 科创板plus ETF
        subclass_list = ["01", "03", "08", "09", "31"]
        url_list = [f"http://query.sse.com.cn/commonSoaQuery.do?jsonCallBack=jsonpCallback87795546&sqlId=FUND_LIST&fundType=00&subClass={subc}" for subc in subclass_list]

        loop = asyncio.get_event_loop()
        txt_list = loop.run_until_complete(self._fetch_urls(url_list))

        etf_list = []
        for txt in txt_list:
            j_data = json.loads(txt[22:-1])
            code_list = [record["fundCode"] for record in j_data["result"]]
            etf_list.extend(code_list)
        return etf_list

    def _craw_etf_details(self, code_list) -> dict:
        url_list = [f"http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback24328638&FUNDID2={code}&sqlId=COMMON_SSE_CP_JJLB_ETFJJGK_GGSGSHQD_COMPONENT_C" for code in code_list]

        loop = asyncio.get_event_loop()
        txt_list = loop.run_until_complete(self._fetch_urls(url_list))

        all_details = {}
        for code, txt in zip(code_list, txt_list):
            j_data = json.loads(txt[22:-1])
            all_details[code] = j_data["result"]
        return all_details

    @classmethod
    def write_details(cls, directory: str, etf_details: dict):
        os.makedirs(directory, exist_ok=True)
        for code in etf_details:
            data_dict = etf_details[code]
            # 保留成分股数量<=50
            if len(data_dict) > 50:
                continue
            with open(f"{directory}/{code}.csv", "w", encoding="utf8") as f:
                fields = ["INSTRUMENT_ID", "QUANTITY", "CREATION_PREMIUM_RATE", "REDEMPTION_DISCOUNT_RATE", "SUBSTITUTION_FLAG", "SUBSTITUTION_CASH_AMOUNT"]
                csv_writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                csv_writer.writeheader()
                csv_writer.writerows(data_dict)


class EtfSzDownloader:
    def __init__(self):
        self._client = httpx.AsyncClient(limits=httpx.Limits(max_connections=20))
        self._headers = self._generate_headers()

    def _generate_headers(self) -> dict:
        num = random.randint(90, 120)
        return {
            "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{num}.0) Gecko/20100101 Firefox/{num}.0",
        }

    async def _fetch_url(self, url) -> dict:
        response = await self._client.get(url, headers=self._headers, timeout=None)
        print(f"==> {url}")
        return response.text

    async def _fetch_urls(self, urls: list):
        tasks = [self._fetch_url(url) for url in urls]
        return await asyncio.gather(*tasks)

    def _craw_etf_list(self) -> dict:
        """获取ETF代码列表, source: https://www.szse.cn/market/product/list/etfList/"""
        data = httpx.get("https://www.szse.cn/api/report/ShowReport/data?CATALOGID=1945&loading=first", headers=self._headers).json()
        tot_page_num = data[1]["metadata"]["pagecount"]
        url_list = [f"https://www.szse.cn/api/report/ShowReport/data?CATALOGID=1945&tab1PAGENO={i}" for i in range(1, tot_page_num + 1)]

        loop = asyncio.get_event_loop()
        txt_list = loop.run_until_complete(self._fetch_urls(url_list))

        etf_code_list = []
        for txt in txt_list:
            j_data = json.loads(txt)
            for record in j_data[1]["data"]:
                etf_code_list.append(record["fund_code"])
        return etf_code_list

    def _craw_etf_details(self, code_list) -> dict:
        date_str = time.strftime("%Y%m%d")
        url_list = [f"http://reportdocs.static.szse.cn/files/text/etf/ETF{code}{date_str}.txt" for code in code_list]

        loop = asyncio.get_event_loop()
        txt_list = loop.run_until_complete(self._fetch_urls(url_list))

        pat = re.compile(r" \d{6}.+")
        for code, txt in zip(code_list, txt_list):
            for line in pat.findall(txt):
                line_list = re.split(r"\s+", line)


if __name__ == "__main__":
    # sh_downloader = EtfShDownloader()
    # etf_code_list = sh_downloader._craw_etf_list()
    # print("etf length:", len(etf_code_list))
    # etf_details = sh_downloader._craw_etf_details(etf_code_list)
    # EtfShDownloader.write_details("sh_etf", etf_details)
    # print("write_csv done")

    sz_downloader = EtfSzDownloader()
    etf_code_list = sz_downloader._craw_etf_list()
    print("etf length:", len(etf_code_list))
