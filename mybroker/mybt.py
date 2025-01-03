import backtrader as bt
''' 首先引入 backtrader '''
cerebro = bt.Cerebro()
''' 创建一个Cerebro引擎实例 '''

# Cerebro 引擎在后台创建了 broker(经纪人)实例，系统默认每个broker的初始资金为10000.0
print('Starting portfolio value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final portfolio value: %.2f' % cerebro.broker.getvalue())
