import requests


class Candle(object):
    def __init__(self, d):
        self.open = float(d['open'])
        self.high = float(d['high'])
        self.low = float(d['low'])
        self.close = float(d['close'])
        self.volume = float(d['volume'])
        self.time = d['time']


class BigONE(object):
    def __init__(self, debug=True):
        self.debug = debug

    def parse_candles(self, arr):
        candles = []
        for c in arr:
            candles.append(Candle(c))
        return candles

    def read_candles(self, symbol, count):
        limit = 100
        url = "https://www.bigonezh.com/api/v3/asset_pairs/%s/candles?period=day1&limit=%d&time=" % (
            symbol, limit)
        offset = ""
        candles = []
        while True:
            r = requests.get(url + offset).json()
            if r['code'] != 0:
                print("read candles failed", r['code'], r)
                return None
            arr = self.parse_candles(r['data'])
            if len(candles) + len(arr) > count:
                arr = arr[:count-len(candles)]
            candles.extend(arr)
            if len(arr) < limit:
                break
            offset = arr[-1].time
        return candles[::-1]
