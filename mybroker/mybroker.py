# 导入所需的库和模块
import pybroker as pb
from pybroker import Strategy, ExecContext
from pybroker.ext.data import AKShare

# 启用数据源缓存，以避免重复下载数据
pb.enable_data_source_cache('my_akshare_cache', 'my_akshare_cache_dir') 

# 定义全局参数 "stock_code"（股票代码）、"percent"（持仓百分比）和 "stop_profit_pct"（止盈百分比）
pb.param(name='stock_code', value='600000')
pb.param(name='percent', value=1)
pb.param(name='stop_loss_pct', value=10)
pb.param(name='stop_profit_pct', value=10)

# 初始化 AKShare 数据源
akshare = AKShare()

# 使用 AKShare 数据源查询特定股票（由 "stock_code" 参数指定）在指定日期范围内的数据
df = akshare.query(symbols=[pb.param(name='stock_code')], start_date='20220131', end_date='20230228')

# 定义交易策略：如果当前没有持有该股票，则买入股票，并设置止盈点位
def buy_with_stop_loss(ctx: ExecContext):
    pos = ctx.long_pos()
    if not pos:
        # 计算目标股票数量，根据 "percent" 参数确定应购买的股票数量
        ctx.buy_shares = ctx.calc_target_shares(pb.param(name='percent'))
        ctx.hold_bars = 100
    else:
        ctx.sell_shares = pos.shares
        # 设置止盈点位，根据 "stop_profit_pct" 参数确定止盈点位
        ctx.stop_profit_pct = pb.param(name='stop_profit_pct')


# 创建策略配置，初始资金为 500000
my_config = pb.StrategyConfig(initial_cash=500000)

# 使用配置、数据源、起始日期、结束日期，以及刚才定义的交易策略创建策略对象
strategy = Strategy(akshare, start_date='20220131', end_date='20230228', config=my_config)

# 添加执行策略，设置股票代码和要执行的函数
strategy.add_execution(fn=buy_with_stop_loss, symbols=[pb.param(name='stock_code')])

# 执行回测，并打印出回测结果的度量值（四舍五入到小数点后四位）
result = strategy.backtest()

# 打印回测结果的度量值、订单、持仓、投资组合和交易
print(result.metrics_df.round(4)) # 查看绩效
print(result.orders)  # 查看订单
print(result.positions)  # 查看持仓
print(result.portfolio)  # 查看投资组合
print(result.trades)  # 查看交易

import matplotlib.pyplot as plt

chart = plt.subplot2grid((3, 2), (0, 0), rowspan=3, colspan=2)
chart.plot(result.portfolio.index, result.portfolio['market_value'])