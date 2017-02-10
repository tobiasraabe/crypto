#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import poloniex
import zipfile
import io
import json




polo = poloniex.Poloniex()

fullList = []
while True:
    try:
        potcoin = polo.marketTradeHist('BTC_POT')
    except:
        pass
    time.sleep(1) # every 0.2 seconds
    fullList = set(fullList)
    potcoin2 = set([str(x) for x in potcoin])
    fullList.update(potcoin2 - fullList)
    print(len(fullList))
    if(len(fullList)>=1000):
        print(len(fullList))
        fullList = list(fullList)
        storeList = fullList[:900]  # cut out first X elements
        fullList = fullList[900:]  # keep last X  elements

        #s = io.BytesIO()  # make file like string object
        with open("/media/91E8-D799/poloniex_data/"+str(time.time())+'.txt','w') as outfile:
            for i in range(0,len(storeList)):
                json.dump(eval(storeList[i]),outfile)
        outfile.close()
        print("wrote file at "+time.ctime())
