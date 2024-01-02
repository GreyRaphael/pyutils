import asyncio
import httpx
import random
import time


class StockDownloader:
    def __init__(self):
        self._client = httpx.AsyncClient()
        self._headers = self._generate_headers()

    def _generate_headers(self) -> dict:
        num = random.randint(90, 120)
        return {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{num}.0) Gecko/20100101 Firefox/{num}.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": "http://quote.eastmoney.com/",
            "Cookie": r"qgqp_b_id=b89b70b81a62bfe73ccd706e520187ac; st_si=62862110755884; st_asi=delete; HAList=ty-0-399481-%u4F01%u503A%u6307%u6570%2Cty-1-000001-%u4E0A%u8BC1%u6307%u6570%2Cty-0-300781-%u56E0%u8D5B%u96C6%u56E2%2Cty-1-512820-%u94F6%u884C%u4E1AETF%2Cty-1-688538-%u548C%u8F89%u5149%u7535-U; st_pvi=30142892225396; st_sp=2023-11-15%2014%3A53%3A47; st_inirUrl=; st_sn=3; st_psi=20231222152456914-113200301321-8601090459",
        }

    async def _fetch_url(self, url) -> dict:
        response = await self._client.get(url, headers=self._headers, timeout=None)
        txt = response.text[56:-2]
        return eval(txt)["data"]

    async def _fetch_urls(self, urls: list):
        tasks = [self._fetch_url(url) for url in urls]
        return await asyncio.gather(*tasks)

    def _craw_stocks(self, code_list: list[str]) -> list[dict]:
        urls = []
        for code in code_list:
            market = 1 if code.startswith("6") else 0
            timestamp_end = int(time.time() * 1000)
            timestamp_start = timestamp_end - 4

            url = f"http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&volt=2&fields=f152,f288,f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f198,f259,f260,f261,f171,f277,f278,f279,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f20,f19,f18,f17,f16,f15,f14,f13,f12,f11,f531,f59&secid={market}.{code}&cb=jQuery35108346946561699186_{timestamp_start}_={timestamp_end}"
            urls.append(url)
        stock_list = asyncio.run(self._fetch_urls(urls))
        # print("finish ↓ all stockinfo")
        return stock_list

    def get_quotes(self, code_list: list[str]) -> list[dict]:
        # filter stockinfo
        stockinfo_list = []
        for j_data in self._craw_stocks(code_list):
            stockinfo = {}
            stockinfo["SECUCODE"] = f'{j_data["f57"]}.SH' if j_data["f57"].startswith("6") else f'{j_data["f57"]}.SZ'
            # 最新价
            stockinfo["last"] = j_data["f43"]
            # 最高价
            stockinfo["high"] = j_data["f44"]
            # 最低价
            stockinfo["low"] = j_data["f45"]
            # 开盘价
            stockinfo["open"] = j_data["f46"]
            # 昨收价
            stockinfo["preclose"] = j_data["f60"]
            # 涨停价
            stockinfo["high_limit"] = j_data["f51"]
            # 跌停价
            stockinfo["low_limit"] = j_data["f52"]
            # 涨跌幅
            stockinfo["pctchange"] = j_data["f170"]
            # 涨跌额
            stockinfo["change"] = j_data["f169"]
            # 卖5~卖1: 挂单价+挂单股数
            stockinfo["offer_prices"] = [
                j_data["f31"],
                j_data["f33"],
                j_data["f35"],
                j_data["f37"],
                j_data["f39"],
            ]
            stockinfo["offer_volumes"] = [
                100 * j_data["f32"] if isinstance(j_data["f32"], float) else "-",
                100 * j_data["f34"] if isinstance(j_data["f34"], float) else "-",
                100 * j_data["f36"] if isinstance(j_data["f36"], float) else "-",
                100 * j_data["f38"] if isinstance(j_data["f38"], float) else "-",
                100 * j_data["f40"] if isinstance(j_data["f40"], float) else "-",
            ]
            # 买1~买5: 挂单价+挂单股数
            stockinfo["bid_prices"] = [
                j_data["f19"],
                j_data["f17"],
                j_data["f15"],
                j_data["f13"],
                j_data["f11"],
            ]
            stockinfo["bid_volumes"] = [
                100 * j_data["f20"] if isinstance(j_data["f20"], float) else "-",
                100 * j_data["f18"] if isinstance(j_data["f18"], float) else "-",
                100 * j_data["f16"] if isinstance(j_data["f16"], float) else "-",
                100 * j_data["f14"] if isinstance(j_data["f14"], float) else "-",
                100 * j_data["f12"] if isinstance(j_data["f12"], float) else "-",
            ]
            # 总市值
            stockinfo["total_market_value"] = j_data["f116"]
            # # 流通市值
            # stockinfo['total_circulate_value']=j_data['117']
            # 总股本
            stockinfo["total_share"] = j_data["f84"]
            # # 流通股本
            # stockinfo['circulate_share']=j_data['f85']
            # 成交量
            stockinfo["total_volume_trade"] = j_data["f47"] * 100
            # 成交额
            stockinfo["total_value_trade"] = j_data["f48"]

            stockinfo_list.append(stockinfo)
        return stockinfo_list


if __name__ == "__main__":
    example_list = ["000001", "300116", "600022", "688538"]
    obj = StockDownloader()
    stockinfo_list = obj.get_quotes(example_list)
    print(stockinfo_list)
