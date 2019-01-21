# -*- encoding: utf-8 -*-
"""
@File    :   newMacdStrategy.py    
@Contact :   liuhaobwjc@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019-01-15 15:53   liuhao      1.0         None
"""


from vnpy.trader.app.ctaStrategy.ctaTemplate import CtaTemplate
from vnpy.trader.language.english.constant import EMPTY_FLOAT
from vnpy.trader.vtUtility import BarGenerator, ArrayManager
import datetime
import pandas as pd
import heapq


class NewMacdStrategy(CtaTemplate):
    """New MACD策略Demo"""
    className = 'NewMacdStrategy'
    author = u'liu_hao'

    # 策略参数
    initDays = 0  # 初始化数据所用的天数
    barIndex = 0
    MacdList = []
    barDataList = []
    ema12 = EMPTY_FLOAT
    ema26 = EMPTY_FLOAT
    diff = EMPTY_FLOAT
    dea9 = EMPTY_FLOAT
    macd = EMPTY_FLOAT
    beforeMacd = EMPTY_FLOAT
    newMacd = EMPTY_FLOAT

    # 策略变量

    lowBand = -0.0009
    upBand = 0.0011
    fixprice = 0.2
    ontrade = 0
    adjustNum = 5000

    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol',
                 'initDays',
                 'barIndex',
                 'MacdList',
                 'barDataList',
                 'ema12',
                 'ema26',
                 'diff',
                 'dea9',
                 'macd',
                 'beforeMacd',
                 'newMacd']

    # 变量列表，保存了变量的名称
    varList = ['lowBand',
               'upBand',
               'fixprice',
               'adjustNum']

    # 同步列表，保存了需要保存到数据库的变量名称
    syncList = ['pos']

    # ----------------------------------------------------------------------

    def __init__(self, ctaEngine, setting):
        """Constructor"""
        super(NewMacdStrategy, self).__init__(ctaEngine, setting)

        self.bg = BarGenerator(self.onBar, nTick=10, onNTickBar=self.onNTickBar)
        self.am = ArrayManager()

        # 注意策略类中的可变对象属性（通常是list和dict等），在策略初始化时需要重新创建，
        # 否则会出现多个策略实例之间数据共享的情况，有可能导致潜在的策略逻辑错误风险，
        # 策略类中的这些可变对象属性可以选择不写，全都放在__init__下面，写主要是为了阅读
        # 策略时方便（更多是个编程习惯的选择）

    # ----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        self.writeCtaLog(u'new MACD演示策略初始化')
        initData = self.loadTick(self.initDays)
        for bar in initData:
            self.onBar(bar)
        self.putEvent()

    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'new MACD演示策略启动')
        self.putEvent()

    def onStop(self):
        """停止策略（必须由用户继承实现）"""

        self.writeCtaLog(u'new MACD演示策略停止')
        self.putEvent()

    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        self.bg.upDateTickBar(tick)
        # self.bg.updateBar(tick)

    def onNTickBar(self, bar):
        am = self.am
        am.updateBar(bar)
        if not am.inited:
            return
        if self.barIndex == 0:
            self.ema12 = bar.close
            self.ema26 = bar.close
            self.diff = 0
            self.dea9 = 0
        else:
            self.ema12 = self.ema(self.ema12, bar.close, 12)
            self.ema26 = self.ema(self.ema26, bar.close, 26)
            self.diff = self.ema12 - self.ema26
            self.dea9 = self.ema(self.dea9, self.diff, 9)
        self.macd = self.diff - self.dea9
        if self.barIndex < 34:
            self.newMacd = 0
        else:
            self.newMacd = self.macd / am.closeArray[-35]

        self.MacdList.append(self.beforeMacd)
        # 做多买入
        crossLowpBand = (self.diff > 0.0) and (self.dea9 > 0.0) and (self.beforeMacd < self.lowBand) and (
                    self.newMacd > self.lowBand)

        # 做多止损
        crossLimitLowBand = self.newMacd <= 1.1 * self.lowBand

        # 做空买入
        crossUpBand = (self.diff < 0.0) and (self.dea9 < 0.0) and (self.beforeMacd > self.upBand) and (
                    self.newMacd < self.upBand)

        # 做空止损
        crossLimitUpBand = self.newMacd >= 1.1 * self.upBand

        if bar.datetime.time() < datetime.time(14, 55):
            if self.pos == 0:
                if crossLowpBand:
                    self.buy(bar.close + self.fixprice, 1)
                    self.log('buy   : ' + str(bar.datetime) + " " + str(bar.close))
                elif crossUpBand:
                    self.short(bar.close - self.fixprice, 1)
                    self.log('short : ' + str(bar.datetime) + " " + str(bar.close))

            elif self.pos > 0:
                if self.newMacd >= 0:
                    self.log('sell  : ' + str(bar.datetime) + " " + str(bar.close) + "  +")
                    self.sell(bar.close - self.fixprice, 1)
                elif crossLimitLowBand:
                    self.sell(bar.close - self.fixprice, 1)
                    self.log('sell  : ' + str(bar.datetime) + " " + str(bar.close) + "  -")
            else:
                if self.newMacd <= 0:
                    self.log('cover : ' + str(bar.datetime) + " " + str(bar.close) + "  +")
                    self.cover(bar.close + self.fixprice, 1)

                elif crossLimitUpBand:
                    self.log('cover : ' + str(bar.datetime) + " " + str(bar.close) + "  -")
                    self.cover(bar.close + self.fixprice, 1)
        else:
            if self.pos > 0:
                self.log('sell  : ' + str(bar.datetime) + " " + str(bar.close))
                self.sell(bar.close - self.fixprice, 1)

            elif self.pos < 0:
                self.log('cover : ' + str(bar.datetime) + " " + str(bar.close))
                self.cover(bar.close + self.fixprice, 1)

        if self.barIndex < 35:
            self.barIndex = self.barIndex + 1
        self.beforeMacd = self.newMacd
        self.adjustParameter()

        # 发出状态更新事件
        self.putEvent()

    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        am = self.am
        am.updateBar(bar)
        if not am.inited:
            return
        if self.barIndex == 0:
            self.ema12 = bar.close
            self.ema26 = bar.close
            self.diff = 0
            self.dea9 = 0
        else:
            self.ema12 = self.ema(self.ema12, bar.close, 12)
            self.ema26 = self.ema(self.ema26, bar.close, 26)
            self.diff = self.ema12 - self.ema26
            self.dea9 = self.ema(self.dea9, self.diff, 9)
        self.macd = self.diff - self.dea9
        if self.barIndex < 34:
            self.newMacd = 0
        else:
            self.newMacd = self.macd / am.closeArray[-35]

        self.MacdList.append(self.beforeMacd)
        # 做多买入
        crossLowpBand = (self.diff > 0.0) and (self.dea9 > 0.0) and(self.beforeMacd < self.lowBand) and (self.newMacd > self.lowBand)

        # 做多止损
        crossLimitLowBand = self.newMacd <= 1.1 * self.lowBand

        # 做空买入
        crossUpBand = (self.diff < 0.0) and (self.dea9 < 0.0) and (self.beforeMacd > self.upBand) and (self.newMacd < self.upBand)

        # 做空止损
        crossLimitUpBand = self.newMacd >= 1.1 * self.upBand

        if bar.datetime.time() < datetime.time(14, 55):
            if self.pos == 0:
                if crossLowpBand:
                    self.buy(bar.close+self.fixprice, 1)
                    self.log('buy   : '+str(bar.datetime)+" "+str(bar.close))
                elif crossUpBand:
                    self.short(bar.close-self.fixprice, 1)
                    self.log('short : '+str(bar.datetime)+" "+str(bar.close))

            elif self.pos > 0:
                if self.newMacd >= 0:
                    self.log('sell  : '+str(bar.datetime)+" "+str(bar.close)+"  +")
                    self.sell(bar.close-self.fixprice, 1)
                elif crossLimitLowBand:
                    self.sell(bar.close-self.fixprice, 1)
                    self.log('sell  : '+str(bar.datetime)+" "+str(bar.close)+"  -")
            else:
                if self.newMacd <= 0:
                    self.log('cover : '+str(bar.datetime)+" "+str(bar.close)+"  +")
                    self.cover(bar.close+self.fixprice, 1)
            
                elif crossLimitUpBand:
                    self.log('cover : '+str(bar.datetime)+" "+str(bar.close)+"  -")
                    self.cover(bar.close+self.fixprice, 1)
        else:
            if self.pos > 0:
                self.log('sell  : '+str(bar.datetime)+" "+str(bar.close))
                self.sell(bar.close-self.fixprice, 1)
                
            elif self.pos < 0:
                self.log('cover : '+str(bar.datetime)+" "+str(bar.close))
                self.cover(bar.close+self.fixprice, 1)

        if self.barIndex < 35:
            self.barIndex = self.barIndex + 1
        self.beforeMacd = self.newMacd
        self.adjustParameter()

        # 发出状态更新事件
        self.putEvent()

    def onOrder(self, order):
        pass

    def onTrade(self, trade):
        self.ontrade = 0

    def onStopOrder(self, so):
        pass

    def ema(self, beforeValue, newData, days):
        temp = ((days - 1) * beforeValue + 2 * newData) / (days + 1)
        return temp

    def log(self,message):
        if True:
            print message

    def adjustParameter(self):
        if len(self.MacdList) < self.adjustNum:
            return
        else:
            tempList = self.MacdList[(-1*self.adjustNum):]
            max_10_list = heapq.nlargest(1000, tempList)
            min_10_list = heapq.nsmallest(1000, tempList)
            self.upBand = sum(max_10_list)/len(max_10_list)
            self.lowBand = sum(min_10_list)/len(min_10_list)
            # self.log(self.lowBand)
            # self.log(self.upBand)

