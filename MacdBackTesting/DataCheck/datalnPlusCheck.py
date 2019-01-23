#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   datalnPlusCheck.py
@Contact :   liuhaobwjc@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019-01-22 18:49   liuhao      1.0         None
检验一年的数据0.5s对数增量符合adf检验
(-2595.2863711207233, 0.0, 1, 6307108, {'5%': -2.8615404582608499, '1%': -3.4303510368147587, '10%': -2.5667702439153484}, -94120636.835572585)
"""

import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts

csv_data = pd.read_csv('tick_data.csv')
addMap = {'ln', 'delta'}
for index in addMap:
    csv_data[index] = 0
csv_data['ln'] = np.log(csv_data['Close'])
data = csv_data['ln']
print(data.head(10))
diff_data = data.diff().dropna()
diff_data1s = data.diff(periods=2).dropna()
diff_data5s = data.diff(periods=10).dropna()
diff_data10s = data.diff(periods=20).dropna()
diff_data15s = data.diff(periods=30).dropna()
diff_data20s = data.diff(periods=40).dropna()
diff_data30s = data.diff(periods=60).dropna()
diff_data50s = data.diff(periods=100).dropna()
diff_data60s = data.diff(periods=120).dropna()
print(ts.adfuller(diff_data, 1))
print(ts.adfuller(diff_data1s, 1))
print(ts.adfuller(diff_data5s, 1))
print(ts.adfuller(diff_data10s, 1))
print(ts.adfuller(diff_data15s, 1))
print(ts.adfuller(diff_data20s, 1))
print(ts.adfuller(diff_data30s, 1))
print(ts.adfuller(diff_data50s, 1))
print(ts.adfuller(diff_data60s, 1))


# (-2595.2877601362115, 0.0, 1, 6307107, {'5%': -2.8615404582609227, '1%': -3.430351036814923, '10%': -2.566770243915387}, -94120626.928191945)
# (-2533.0354850006024, 0.0, 1, 6307106, {'5%': -2.8615404582609951, '1%': -3.4303510368150878, '10%': -2.5667702439154256}, -92833325.001819223)
# (-920.03114219749943, 0.0, 1, 6307098, {'5%': -2.8615404582615764, '1%': -3.4303510368164027, '10%': -2.5667702439157352}, -90238198.714439034)
# (-672.18551390814207, 0.0, 1, 6307088, {'5%': -2.861540458262303, '1%': -3.4303510368180468, '10%': -2.566770243916122}, -89887409.629148424)
# (-553.72180875421043, 0.0, 1, 6307078, {'5%': -2.8615404582630295, '1%': -3.4303510368196903, '10%': -2.5667702439165088}, -89746857.633085102)
# (-481.65974286505252, 0.0, 1, 6307068, {'5%': -2.861540458263756, '1%': -3.4303510368213344, '10%': -2.5667702439168956}, -89674986.724490613)
# (-396.71912549292483, 0.0, 1, 6307048, {'5%': -2.8615404582652095, '1%': -3.4303510368246224, '10%': -2.5667702439176687}, -89600620.160658136)
# (-312.68251015408379, 0.0, 1, 6307008, {'5%': -2.8615404582681156, '1%': -3.430351036831198, '10%': -2.5667702439192159}, -89539393.050587371)
# (-287.82538909879844, 0.0, 1, 6306988, {'5%': -2.8615404582695692, '1%': -3.4303510368344861, '10%': -2.5667702439199891}, -89526561.363202974)