import sys
from b1api import BigONE
from swapper import Swapper


class FswapQuant(object):
    def __init__(self, symbol, days=365, debug=True):
        self.debug = debug
        self.bigone = BigONE(debug)
        self.candles = self.bigone.read_candles(symbol, days)
        if self.candles is None or len(self.candles) == 0:
            return

        ohlc = self.backtest_ohlc()
        print("backtest: OPEN => HIGH => LOW => CLOSE")
        self.print_result(ohlc)

        oc = self.backtest_oc()
        print("\n")
        print("backtest: OPEN => CLOSE")
        self.print_result(oc)

    def print_result(self, swapper):
        open_price = swapper.quote_open / swapper.base_open
        close_price = swapper.price()
        price_change = (close_price - open_price) / open_price

        print("open price: %f" % open_price)
        print("close price: %f" % close_price)
        print("open base: %f" % swapper.base_open)
        print("open quote: %f" % swapper.quote_open)
        print("close base: %f" % swapper.base)
        print("close quote: %f" % swapper.quote)
        print("price change: %.4f%%" % (price_change * 100))
        print("profit: %.4f%%" % (swapper.profit()*100))

    def backtest_ohlc(self, times=1):
        swapper = Swapper(self.candles[0].open, debug=self.debug)
        for _ in range(times):
            for c in self.candles:
                swapper.set_price(c.open)
                swapper.set_price(c.high)
                swapper.set_price(c.low)
                swapper.set_price(c.close)

        return swapper

    def backtest_oc(self, times=1):
        swapper = Swapper(self.candles[0].open, debug=self.debug)
        for _ in range(times):
            for c in self.candles:
                swapper.set_price(c.open)
                swapper.set_price(c.close)

        return swapper


def main():
    if len(sys.argv) != 3:
        print("""python 4swap.py symbol days
for example: python 4swap.py XIN-BTC 100""")
        return

    symbol = sys.argv[1]
    days = int(sys.argv[2])
    FswapQuant(symbol=symbol, days=days, debug=False)


if __name__ == "__main__":
    main()
