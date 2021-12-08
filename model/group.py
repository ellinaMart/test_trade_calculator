
class Group:
    def __init__(self, instrument=None, account_type=None, leverage=None, lot=None, currency=None):
        self.instrument = instrument
        self.account_type = account_type
        self.leverage = leverage
        self.lot = lot
        self.currency = currency

    def __repr__(self):
        return "%s: %s: %s: %s: %s" %(self.instrument, self.account_type, self.leverage, self.lot, self.currency)