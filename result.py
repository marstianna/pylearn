class Result:
    columns = ['stock_code','action','price','date','strategy','profit','intension','current_hold']

    def __init__(self,stock_code,action,price,date,strategy,profit=0,intension=0,current_hold=0):
        self.__stock_code = stock_code
        self.__action = action
        self.__price = price
        self.__date = date
        self.__strategy = strategy
        self.__profit = profit
        self.__intension = intension
        self.__current_hold = current_hold

    def get_dict(self):
        return {'stock_code':self.__stock_code,
                'action':self.__action,
                'price':self.__price,
                'date':self.__date,
                'strategy':self.__strategy,
                'profit':self.__profit,
                'intension':self.__intension,
                'current_hold':self.__current_hold}