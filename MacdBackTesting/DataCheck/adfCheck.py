# -*- encoding: utf-8 -*-
"""
@File    :   adfCheck.py    
@Contact :   liuhaobwjc@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019-01-22 16:38   liuhao      1.0         None
"""
import pandas as pd
import statsmodels.tsa.stattools as ts


class NewMACD:
    EMA12 = []
    EMA26 = []
    DIFF = []
    DEA9 = []
    MACD = []
    NewMACD = []
    data = []

    def init(self, data):
        self.data = data
        self.EMA12 = self.EMA(data, 12)
        self.EMA26 = self.EMA(data, 26)
        self.DIFF = self.Diff(self.EMA12, self.EMA26)
        self.DEA9 = self.EMA(self.DIFF, 9)
        self.MACD = self.Diff(self.DIFF, self.DEA9)
        self.NewMACD = self.NewMACD()
        return self.EMA12, self.EMA26, self.DIFF, self.DEA9, self.MACD, self.NewMACD

    def EMA(self, inputData, days):
        temp = []
        for i in range(len(inputData) - 1):
            if i == 0:
                temp.append(inputData[1])
            else:
                temp.append(((temp[i - 1]) * (days - 1) + 2 * inputData[i + 1]) / (days + 1))
        return temp

    def Diff(self, inptu1, input2):
        temp = []
        for i in range(len(inptu1) - 1):
            temp.append(inptu1[i] - input2[i])
        return temp

    def NewMACD(self):
        temp = []
        for i in range(len(self.MACD) - 1):
            if i < 35:
                temp.append(0)
            else:
                temp.append(self.MACD[i] / self.data[i - 34])
        return temp


csv_data = pd.read_csv("tick_data_adf.csv")
addListMap = ['macd', 'newMacd']
for index in addListMap:
    csv_data[index] = 0
data1 = csv_data
macdEnginer = NewMACD()
data = data1['Close'].head(100000)

EMA12, EMA26, DIFF, DEA9, MACD, NewMACD = macdEnginer.init(data)
print("new :" + str(ts.adfuller(NewMACD[26952*2:26952 * 3], 1)))
print("old :" + str(ts.adfuller(MACD[26952*2:26952 * 3], 1)))
