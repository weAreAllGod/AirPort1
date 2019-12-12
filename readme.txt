AirPort##主程序文件
    |
    |--dataProcessing--|
    |                  |
    |                  |--digPosibleParkingPoints.py##疑似停车位挖掘主程序
    |                  |
    |                  |--digTimeBetweenPoints.py##任意两点间挖掘主程序
    |                  |
    |                  |--service.py##接口函数定义文件
    |                  |
    |                  |--mapper.py##数据库处理层函数
    |                  |
    |                  |--utils.py##辅助函数
    |                  |
    |                  |--showData.py##数据展示函数
    |
    |--state##临时文件等静态数据的存放地
    |
    |--tools##通用的工具函数
对于planning文件夹下各个脚本关系的解释
columnGenaration：最朴素的列生成思想实现，这里不考虑机型机位之间的关系，什么都不考虑
属于最朴素的组合优化问题
withGateTypeAndInternational：加入业务场景并且用cplex求解的初级版本,这里是加入了
机型机位，国际国内的限制
withGateTypeAndInitialsata:考虑初始条件

上面的算法只是从降维和降低运算时间考虑，还没有考虑分支定价的思想。
以下几个文件开始从分支定价进行考虑：
branchPrice:分支定价的初级实现，以遍历为基础
branchPrice1:是子啊branchPrice的基础上进行的添加和改动
branchPrice2:此处加入了构建子问题的过程
以上文件还只是停留在对列生成方法的实现上，没有构建整数规划。
trueBranchPrice:此处开始构建分支的过程，寻找整数规划最优解。