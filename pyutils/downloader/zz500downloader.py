import json
import httpx

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Cookie": "qgqp_b_id=b89b70b81a62bfe73ccd706e520187ac; st_si=62862110755884; st_pvi=30142892225396; st_sp=2023-11-15%2014%3A53%3A47; st_inirUrl=; st_sn=4; st_psi=20240110100025767-113200301321-8227203147; st_asi=20240110100025767-113200301321-8227203147-Web_so_srk-4; HAList=ty-1-000852-%u4E2D%u8BC11000%2Cty-1-688538-%u548C%u8F89%u5149%u7535-U%2Cty-0-000961-%u4E2D%u5357%u5EFA%u8BBE%2Cty-0-300116-%u4FDD%u529B%u65B0%2Cty-1-600022-%u5C71%u4E1C%u94A2%u94C1%2Cty-1-600028-%u4E2D%u56FD%u77F3%u5316%2Cty-0-000001-%u5E73%u5B89%u94F6%u884C%2Cty-1-601012-%u9686%u57FA%u7EFF%u80FD%2Cty-1-600000-%u6D66%u53D1%u94F6%u884C%2Cty-0-300200-%u9AD8%u76DF%u65B0%u6750; JSESSIONID=059027C739F620230EFFE179727229A1",
}


def download_zz500() -> list[dict]:
    response = httpx.get(
        "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery11230023591033888216595_1704874224569&sortColumns=SECURITY_CODE&sortTypes=-1&pageSize=500&pageNumber=1&reportName=RPT_INDEX_TS_COMPONENT&columns=SECUCODE%2CSECURITY_CODE%2CTYPE%2CSECURITY_NAME_ABBR%2CCLOSE_PRICE%2CINDUSTRY%2CREGION%2CWEIGHT%2CEPS%2CBPS%2CROE%2CTOTAL_SHARES%2CFREE_SHARES%2CFREE_CAP&quoteColumns=f2%2Cf3&quoteType=0&source=WEB&client=WEB&filter=(TYPE%3D%223%22)",
        headers=HEADERS,
        timeout=None,
    )
    print("zz500 downloaded")
    response_dict = json.loads(response.text[44:-2])
    return response_dict["result"]["data"]


def write2json(data_dicts: list[dict]) -> None:
    new_data_dicts = [
        {
            "code": f"{record['SECURITY_CODE']}.SS" if record["SECURITY_CODE"].startswith("6") else f"{record['SECURITY_CODE']}.SZ",
            "price": record["f2"],
            "volume": 200 if record["SECURITY_CODE"].startswith("68") else 100,
        }
        for record in data_dicts
    ]
    with open("zz500.json", "w", encoding="utf-8") as f:
        json.dump(new_data_dicts, f)
    print("zz500 written to ./zz500.json")

def write2csv(data_dicts: list[dict]) -> None:
    new_data_dicts = [
        {
            "code": f"{record['SECURITY_CODE']}.SS" if record["SECURITY_CODE"].startswith("6") else f"{record['SECURITY_CODE']}.SZ",
            "vol": 200 if record["SECURITY_CODE"].startswith("68") else 100,
            "price": record["f2"],
        }
        for record in data_dicts
    ]

    with open("zz500.csv", "w", encoding="utf-8") as file:
        file.write("code,vol,price\n")
        for record in new_data_dicts:
            file.write(f"{record['code']},{record['vol']},{record['price']}\n")


if __name__ == "__main__":
    data_list = download_zz500()
    # write2json(data_list)
    write2csv(data_list)
