# chiness_chess_jieqi
一个最简单的揭棋项目， 包含一个最基本的 mixmax 机器人，默认是黑白对下，可以改成人工走子与机器人对下。

感谢 https://github.com/horse007666/Chinese-chess-python 在他的框架上引入了揭棋的规则及加入了机器人程序

作为19年清明节带孩子之余的一个尝试性活动，之前也有考虑使用类似 alphazero 的算法实现，不过看了 https://github.com/NeymarL/ChineseChess-AlphaZero 项目，发现这个坑有点深，没敢轻易踏入

# 关于揭棋算法

一个很直观的想法是评估函数采用期望值给暗子打分，我也基本是这样实现的。但面对的问题是一旦多层预测时，暗子变成不通明子的走法是不一样的，这就会一下增加不少搜索负责度。

# 运行方式

python chess.py
可以修改 394-397 行注释选择黑白棋的走棋逻辑或人工输入与机器人对下

# 尴尬

目前黑白对下，走的棋子，偶尔会出现让人看不懂的招数，猜想可能是实现有bug或没有想清楚算法。毕竟 “程序会按你写的方式运行而不是你想的方式...”。

# 揭棋很好玩，感觉直接把象棋的有趣程度提高了一大截，但天天象棋每天只能评测6把，太少了哇
# 目前最高打到 揭4-1，加油！ 
