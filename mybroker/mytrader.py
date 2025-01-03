# import matplotlib.pyplot as plt
# squares = [1, 4, 9, 16, 25]
# plt.plot(squares)
# plt.show()


from hky_init import *

# 定义回测时间
start_date = Datetime(20200101)
end_date = Datetime(20240429)

# 指定分析对象
stk = sm['sh510050']
print(stk)
k = stk.get_kdata(Query(start_date, end_date))

# 策略描述
slow_n = 120
fast_n = 20
slow_ma = MA(CLOSE, slow_n)
fast_ma = MA(CLOSE, fast_n)

# 默认的 k 数据较多，绘制看不清，这里取当前最后的200个k线作为示意
k.close.plot(legend_on=True, label='收盘价')
slow_ma(k).plot(new=False, legend_on=True, label=f'{slow_n}日均线')
fast_ma(k).plot(new=False, legend_on=True, label=f'{fast_n}日均线')

buy_ind = fast_ma > slow_ma
sell_ind = NOT(buy_ind)
buy_ind(k).plot()


# 定义回测账户，并指定成本算法
my_tm = crtTM(start_date, init_cash=100000, cost_func=TC_FixedA2017())

# 创建信号指示器
my_sg = SG_Bool(buy_ind, sell_ind)

# 创建资金管理算法
my_mm = MM_Nothing()

# 移滑价差, 后续可以自行尝试移滑价差的影响
my_sp = SP_FixedValue(0.05)

# 创建交易系统
my_sys = SYS_Simple(tm=my_tm, sg=my_sg, mm=my_mm, sp=my_sp)


# 执行交易系统回测，并查看系统绩效
my_sys.run(stk, Query(start_date, end_date))
my_sys.performance()