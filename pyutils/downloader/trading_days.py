import sys
import json
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Referer": "http://www.szse.cn/aboutus/calendar/index.html",
}


def download_calendar(year: str, output_dir: str = "."):
    print("↓ trading days of", year)
    trading_days = []
    for i in range(1, 13):
        url = f"http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={year}-{i:02d}"
        print("↓", url)
        j_data_list = requests.get(url, headers=HEADERS).json().get("data")
        trading_records = [record["jyrq"] for record in j_data_list if record["jybz"] == "1"]
        trading_days += trading_records

    with open(f"{output_dir}/{year}.json", "w") as file:
        json.dump(trading_days, file, indent=4)
    print("finish trading days of", year)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pyutils/downloader/trading_days.py <year>")
        exit(0)
    else:
        year_str = sys.argv[1]
        download_calendar(year_str)
