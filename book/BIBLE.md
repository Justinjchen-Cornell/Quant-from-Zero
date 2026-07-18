# BIBLE placeholder
# 从零开始跑量化 — 项目圣经

> 全书唯一规范来源。所有章节、图表、引用必须对齐此文档。
> 每次修改先更新 Bible，再改章节。

---

## 前提

一本面向量化初学者的中文入门书。核心主张：
**这些策略不是用来跑量化交易的——它们是思维训练工具。**

## 读者画像

- 想学量化但被公式劝退的人
- 做了几年投资想识破回测骗局的人
- 想把量化思维迁移到本行业的人
- 阅读场景：GitHub 在线浏览 + 本地 Jupyter 边读边跑代码

## 语调与风格

- 语气：对话式、直接。像朋友在咖啡店给你讲——不是教授在讲台上讲
- 句子长度：短句为主。超过 40 字的句子拆成两句
- 代码：每段不超过 10 行，必须有输出示例
- 术语：第一次出现括号标注英文
- 禁止：不用希腊字母，全部用英文或中文替代
- 强制：每章必须有课堂问答小节，至少 2 组 Q&A

## 章节模板（每章必须包含）

X.0 策略概述 / X.1 真实故事 / X.2 核心代码 / X.3 真实数据+图表
X.4 为什么有效/失效 / X.5 课堂问答 / X.6 五点总结 / X.7 下节预告

## 图表规范

- 命名：output/charts/lessonX_topic.png
- 书中引用：图 X-Y：[描述]。
- dpi=150, 尺寸 14x8, 字体 SimHei
- 配色：蓝#1971c2 绿#2b8a3e 红#c92a2a 橙#f08c00 灰#868e96
- 每章至少 1 张图表

### 缺失图表清单
- [ ] 图 1-1: 16 指数年化收益排名
- [ ] 图 1-2: 收益 vs 波动率散点图
- [ ] 图 3-1: PE 与动态 +/-2 标准差区间
- [ ] 图 5-1: 138 笔交易收益分布
- [ ] 图 8-1: 在线 vs 离线均值对比
- [ ] 图 10-1: 16 指数夏普比排名

## 数据规范

- 来源：akshare，免费中国金融数据 Python 库
- 主数据：data/index_updated.csv（16指数x8683天，1990-2026）
- PE数据：data/*_pe_weekly.csv（CSI300/SH50/CSI500/SZ Dividend）
- 所有数字必须有出处

## 引用规范

- 数据引用：[来源: akshare, 拉取日期 2026-07-18]
- 代码引用：本章完整代码：code/lessonX_xxx.py
- 交叉引用：（见第X课）
- 外部引用：[作者, 书名/论文名, 年份]

## 参考文献

- Markowitz, H. Portfolio Selection, 1952
- Sharpe, W.F. Capital Asset Prices, 1964
- Fama, E.F. & French, K.R. The Cross-Section of Expected Stock Returns, 1992
- Jegadeesh, N. & Titman, S. Returns to Buying Winners and Selling Losers, 1993
- Taleb, N.N. The Black Swan, 2007
- akshare Documentation, https://akshare.akfamily.xyz/

## 结构概览

| 章 | 标题 | 代码 | 图表 |
|:--:|------|------|:--:|
| 0 | 前言 | — | — |
| 1 | 描述性统计 | lesson1 | MISSING 3 |
| 2 | PE分位数 | lesson2 | OK |
| 3 | 均值-标准差 | lesson3 | MISSING |
| 4 | 蒙特卡洛 | lesson4 | OK |
| 5 | 信号交易 | lesson5 | MISSING |
| 6 | 收益分布 | lesson6 | OK |
| 7 | 日历效应 | lesson7 | OK |
| 8 | 在线统计 | lesson8 | MISSING |
| 9 | 动量策略 | lesson9 | OK |
| 10 | 夏普比 | lesson10 | MISSING |
| 11 | 强弱势 | lesson11 | OK |
| 12 | 终章 | — | — |

## 连续性追踪器

- +44.5%->+0.1% 贯穿全书 (Ch2首现, Ch8深入, 终章总结)
- 不是用来跑量化 首尾呼应 (前言+终章+README)
- 从股票到你的行业 迁移指南 (终章)
- 待验证：每章下节预告链接
- 待建立：Karpathy四原则在代码中的体现

---
*Bible v1.0 | 2026-07-18*
