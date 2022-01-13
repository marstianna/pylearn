class Result:
    columns = ['stock_code','action','price','date','strategy','profit','intension','current_hold','stop_loss_line']

    def __init__(self,stock_code,action,price,date,strategy,profit=0,intension=0,current_hold=0,stop_loss_line=0):
        self.stock_code = stock_code
        self.action = action
        self.price = price
        self.date = date
        self.strategy = strategy
        self.profit = profit
        self.intension = intension
        self.current_hold = current_hold
        self.stop_loss_line = stop_loss_line

    def get_dict(self):
        return {'stock_code':self.stock_code,
                'action':self.action,
                'price':self.price,
                'date':self.date,
                'strategy':self.strategy,
                'profit':self.profit,
                'intension':self.intension,
                'current_hold':self.current_hold,
                'stop_loss_line':self.stop_loss_line}

    def __repr__(self):
        return repr((self.stock_code,self.action,self.price,self.date,self.strategy,self.profit,self.intension,self.current_hold,self.stop_loss_line))