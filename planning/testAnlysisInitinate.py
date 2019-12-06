import numpy as np
import pandas as pd
from tools import dataBase
if __name__ == '__main__':
    mydataBase=dataBase.myDataBase()
    initalData,mydata=mydataBase.getDataThree()
    initalData = initalData.loc[initalData["parkinggate"].isin(range(101, 169))]
    allData=pd.concat([initalData,mydata]).reset_index(drop=True)
