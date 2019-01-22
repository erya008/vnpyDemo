# -*- encoding: utf-8 -*-
"""
@File    :   runBacktesting.py    
@Contact :   liuhaobwjc@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019-01-15 16:04   liuhao      1.0         None

展示如何执行策略回测。
"""

from __future__ import division
import matplotlib.pyplot as plt
import newMacdStrategy
import statsmodels.tsa.stattools as ts
from vnpy.trader.app.ctaStrategy.ctaBacktesting import BacktestingEngine, MINUTE_DB_NAME
from vnpy.trader.app.ctaStrategy.strategy.strategyKingKeltner import KkStrategy
if __name__ == '__main__':


    # 创建回测引擎
    engine = BacktestingEngine()

    # 设置引擎的回测模式为K线
    engine.setBacktestingMode(engine.TICK_BAR_MODE)

    # 设置回测用的数据起始日期
    engine.setStartDate('20130104', initDays=0)
    engine.setEndDate('20130111')

    # 设置产品相关参数
    engine.setSlippage(0.2)  # 股指1跳
    engine.setRate(0.23 / 10000)  # 万0.3
    engine.setSize(1)  # 股指合约大小
    engine.setPriceTick(0.2)  # 股指最小价格变动

    # 设置使用的历史数据库
    engine.setDatabase(MINUTE_DB_NAME, 'tick_data')

    # 在引擎中创建策略对象
    d = {}
    engine.initStrategy(newMacdStrategy.NewMacdStrategy, d)

    # 开始跑回测
    engine.runBacktesting()

    # 显示回测结果
    engine.showBacktestingResult()
    # dajiid

    print ts.adfuller(newMacdStrategy.NewMacdStrategy.MacdList, 1)

    plt.figure(1)
    plt.plot(newMacdStrategy.NewMacdStrategy.MacdList)
    plt.show()
