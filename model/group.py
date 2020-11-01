
class Group:
    def __init__(self, instrument =  None, form_type = None, leverage = None, lot = None, symbol = None, user_currency = None):
        self.instrument = instrument
        self.form_type = form_type
        self.leverage = leverage
        self.lot = lot
        self.symbol = symbol
        self.user_currency = user_currency

    def __repr__(self):
        return "%s: %s: %s: %s: %s: %s" %(self.form_type, self.instrument, self.symbol, self.lot, self.leverage, self.user_currency)