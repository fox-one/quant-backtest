import math


class Swapper(object):
    def __init__(self, price, debug=True):
        self.setup_with_base_quote(1/price, 1, debug)

    def setup_with_base_quote(self, base, quote, debug=True):
        self.debug = debug
        self.base = base
        self.base_open = base
        self.quote_open = quote
        self.quote = quote
        self.bases = [base]
        self.quotes = [quote]
        self.prices = [quote / base]
        self.profits_base = [0]

    def price(self):
        return self.quote / self.base

    def profit(self):
        b = self.base_open + self.quote_open / self.price()
        c = self.base * 2
        return (c - b) / b

    def append_status(self):
        self.bases.append(self.base)
        self.quotes.append(self.quote)
        self.prices.append(self.price())
        self.profits_base.append(self.profit())

    # k = base * quote
    # k = (base + x) * (quote + y)
    # p = quote_new / base_new
    # 要让价格下跌，base增加，quote减少，收base手续费:
    #   base_new = base + x + x * 0.003009 (手续费)
    #   quote_new = quote + y
    #   k / p = (base + x * 1.003009) * (base + x)
    #   0 = 1.003009 * x * x + 2.003009 * base * x + (base * base - k / p)
    # 要让价格上涨，base减少，quote增加，收quote手续费:
    #   base_new = base + x
    #   quote_new = quote + y + y * 0.003009 (手续费)
    #   k * p = (quote + y) * (quote + y * 1.003009)
    #   0 = 1.003009 * y * y + 2.003009 * quote * y + (quote * quote - k * p)
    def set_price(self, price):
        # print("open price: %f\nclose price: %f" % (self.price(), price))
        if price == self.price():
            return

        k = self.base * self.quote
        a = 1 + 0.003 / 0.997

        # 要让价格下跌，base增加，quote减少，收base手续费:
        #   base_new = base + x + x * 0.003009 (手续费)
        #   quote_new = quote + y
        #   k / p = (base + x * 1.003009) * (base + x)
        #   0 = 1.003009 * x * x + 2.003009 * base * x + (base * base - k / p)
        if price < self.price():
            b = (1 + a) * self.base
            c = self.base * self.base - k / price
            x = (math.sqrt(b * b - 4 * a * c) - b) / 2 / a
            y = k / (self.base + x) - self.quote
            base_new = self.base + a * x
            quote_new = self.quote + y
            if self.debug:
                print("base: %f + %f * %f => %f\nquote: %f + %f => %f\nprice: %f => %f" %
                      (self.base, a, x, base_new, self.quote, y, quote_new, self.quote/self.base, quote_new/base_new))
            self.base = base_new
            self.quote = quote_new
            self.append_status()
            return

        # 要让价格上涨，base减少，quote增加，收quote手续费:
        #   base_new = base + x
        #   quote_new = quote + y + y * 0.003009 (手续费)
        #   k * p = (quote + y) * (quote + y * 1.003009)
        #   0 = 1.003009 * y * y + 2.003009 * quote * y + (quote * quote - k * p)
        if price > self.price():
            b = (1 + a) * self.quote
            c = self.quote * self.quote - k * price
            y = (math.sqrt(b * b - 4 * a * c) - b) / 2 / a
            x = k / (self.quote + y) - self.base
            base_new = self.base + x
            quote_new = self.quote + a * y
            if self.debug:
                print("base: %f + %f => %f\nquote: %f + %f * %f => %f\nprice: %f => %f" %
                      (self.base, x, base_new, self.quote, a, y, quote_new, self.price(), quote_new / base_new))
            self.base = base_new
            self.quote = quote_new
            self.append_status()
            return
