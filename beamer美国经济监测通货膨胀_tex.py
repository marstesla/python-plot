#####用pylatex编写latex文档，并编译输出到pdf, beamer.
###图片可先保存为pdf, 然后插入tex
# #将svg转换为pdf
#svg2pdf(ext0 = 'svg',ext2 = 'pdf',dirpath = '.\\data',savePath = '.\\data\\image_pdf')
#汪红驹修改C:\Python310\Lib\site-packages\pylatex\section.py 第27行为28行，防止中文的section 产生同样的\label{sec:}
##一行结尾如果是 {， 或}， 后面都需要加上%， 防止vbox  overfull 提醒错误
##pip install pylatex
##用##\usepackage[Export]{adjustbox} ， frame_image1 控制图片插入最大尺寸，不会超出范围
##所有图标文件名中不要用_ 下标符号，这在tex里需要用\_表示，直接写为_会报错
##处理速度较快，比pptx, docx快

###1疫情监测系列，2价格系列，3财政系列，4金融系列，5股票系列，
####6增长系列，7贸易系列，8美国系列，9欧洲系列，10一带一路系列，11高频系列+GDPNOW，

#################################################################
###准备工作
###先读取数据，计算，画图，输出文本。


######找出pdf
#my_dir=r"E:\E\python_w\data\image_pdf"
from macrobeamertex import *
#########################################
###硬盘符号
source_drive = r"I:"
source_drive = r"E:"
##输出目录
#outputpath = r'G:\E\python_w\data'
outputpath = source_drive + str(r'\E\python_w\data\\')
#outputpath = str(r'E:\E\python_w\data')
sys.path.append(source_drive + '\\E\\python_w\\')   #添加系统搜索路径
my_dir=r"E:\E\python_w\data"
filenames = os.listdir(my_dir)
piccount=0
file_count = 0
for i in filenames:   ###测试0：200，  插入SVG太多， 耗时
    if i[len(i)-3: len(i)].upper() == 'PDF': # check whether the current object is a svg file
        piccount = piccount + 1

print(piccount, " pdf images will be inserted")

#########################################################################################
fname = 'USindicator'    #latex, pdf 文件名
width = r'0.6\textwidth'
source = 'CEIC, NFID'
annotation = r""""""
###################################################################
doc = beamer(fname,  title = '全球宏观经济监测报告系列', subtitle = '美国通货膨胀')
########################################################################################
###############################
###############################################
section = Section('美国通货膨胀率')
doc.append(section)

################################################
############美国通货膨胀率######
sheetname = 'CPIUSA'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 3
US_CPI,unit = xwread(filename, sheetname, start, droprowsN)
US_CPI = clean_df(US_CPI, newcolname_0='no change', Old1='：经季节性调整后', Old2='', New1='：SA', New2='', sortby =None, index_y_m='month')
unit = clean_df(unit, newcolname_0='no change', Old1='：经季节性调整后', Old2='', New1='：SA', New2='', sortby =None, index_y_m='month')
#US_UMR.loc[:,US_UMR.columns[0]].plot()     #美国经济增长率
US_CPI_U = US_CPI.iloc[:, 1:]
unit_U = unit.iloc[:, 1:]
US_CPI_U_pct12 = US_CPI_U.pct_change(12, fill_method = None) *100
plotdata = US_CPI_U_pct12.loc['2020':,['居民消费价格指数：城镇：SA',
                               '居民消费价格指数：城镇：SA：食品和饮料',
                               '城市居民消费价格指数：SA：能源',
                               '城市居民消费价格指数：SA：所有商品',
                               '城市居民消费价格指数：SA：服务业', 
                                #'城市居民消费价格指数：SA：所有项目', 
                               '城市居民消费价格指数：SA：所有项目（不包括食品和能源）',
                               '居民消费价格指数：城镇：SA：住房',
                               '城市居民消费价格指数：SA：服务业：住所出租']].to_period('M')
plotdata = plotdata.sort_values(by = plotdata.index[-1], axis = 1, ascending=False)
fig1,ax1 = figwmarksource1(source='资料来源：CEIC',figsize=(9,6))
plotdata.plot(alpha = 0.8,ax = ax1)
ax1.legend(loc = 'upper left',framealpha = 0)
plt.title('美国消费物价指数（与上年同比）',fontsize = 12)
plt.ylabel('百分比')
lineannotate(fig1, ax1, plotdata)

plotdata = US_CPI_U_pct12.loc['2020':,['城市居民消费价格指数：SA：所有商品',
                                     '城市居民消费价格指数：SA：商品（不包括食品和能源商品）',
                               '城市居民消费价格指数：SA：服务业', 
                               '城市居民消费价格指数：SA：能源',
                               '城市居民消费价格指数：SA：所有项目（不包括食品和能源）',
                               '居民消费价格指数：城镇：SA：住房',
                               '城市居民消费价格指数：SA：服务业：住所出租']]
title = '美国城市居民消费物价指数（与上年同比）'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(plotdata, title, ylabel, savename, outputpath,
                     lgncols =1, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 

doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

###################分品类列出CPI中各项目图线
doc = twolines(US_CPI_U,US_CPI_U_pct12,  doc, outputpath, suptitle_='城市居民CPI分品类（经季节调整后）',freq='每月', 
               ylabel0=unit_U,ylabel1='百分比',  
               start='2022', doctex = True, figsource = '资料来源：美国BEA', doctexsource = 'CEIC, NFID')

###############################################################################
sheetname = 'CPIU'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 3
US_CPIU,unit = xwread(filename, sheetname, start, droprowsN, freq='M', interp = True)
#US_CPIU = clean_df(US_CPIU, newcolname_0='no change', Old1='：经季节性调整后', Old2='', New1='：SA', New2='', sortby =None, index_y_m='month')

US_CPIU_pct12 = US_CPIU.pct_change(12, fill_method = None) *100
plotdata = US_CPIU.loc['2021':,['CPI：城镇',
                               'CPI：城镇：食品和饮料',
                               '城镇CPI：能源',
                               '城镇CPI：所有商品',
                               '城镇CPI：服务业', 
                                #'城镇CPI：所有项目', 
                               '城镇CPI：所有项目、不包括食品和能源',
                               '城镇CPI：住房：住房',
                               '城镇CPI：服务业：住房出租']]
title =  '美国城镇消费物价指数'
ylabel = '1982-1984=100'
savename = title
fig, ax = fig1_lines(plotdata, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), ylinetick= None, source ='资料来源：BEA,国家金融与发展实验室') 


plotdata = US_CPIU_pct12.loc['2000':,['城镇CPI：食品和饮料：食品', '城镇CPI：能源',
                               '城镇CPI：所有商品',
                               '城镇CPI：服务业', 
                                #'城镇CPI：所有项目', 
                               '城镇CPI：所有项目、不包括食品和能源',
                               '城镇CPI：住房：住房',
                               '城镇CPI：服务业：住房出租', 
                               '城镇CPI：教育和通信商品']]
title = '美国城镇消费物价指数（与上年同比）'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(plotdata, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 

###################分品类列出CPI中各项目图线
doc = twolines(US_CPIU,US_CPIU_pct12,  doc, outputpath, suptitle_='美国城镇CPI分品类',freq='每月', 
               ylabel0=unit,ylabel1='百分比', sharex = False, dropna=False, 
               start='2000', doctex = True, figsource = '资料来源：美国BEA', doctexsource = 'CEIC, NFID')


##########PCEPI###消费支出价格指数
#######################
sheetname = 'PCE价格指数MB'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 4
US_PCEPI,unit = xwread(filename, sheetname, start, droprowsN)
US_PCEPI_pct = US_PCEPI.pct_change(12, fill_method = None)*100
linedata = US_PCEPI_pct.loc['2000':,['PCE：PI：SA：基于市场（MB）',
                               'PCE：PI：SA：MB：食品及能源',
                               'PCE：PI：SA：MB：食品与能源除外',
                               'PCE：PI：SA：MB：SE：住房']]
title =  '美国消费支出物价指数（基于市场，与上年同比）'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(linedata, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

#######################
sheetname = 'PCE价格指数'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 4
US_PCEPI,unit = xwread(filename, sheetname, start, droprowsN)
US_PCEPI = clean_df(US_PCEPI, newcolname_0='no change', Old1='个人消费支出：价格指数：经季节性调整后：',
                    Old2='', New1='', New2='', sortby =None, index_y_m='month')
unit = clean_df(unit, newcolname_0='no change', Old1='个人消费支出：价格指数：经季节性调整后：',
                    Old2='', New1='', New2='', sortby =None, index_y_m='month')

US_PCEPI_pct = US_PCEPI.pct_change(12, fill_method = None)*100
linedata = US_PCEPI_pct.loc[:,['个人消费支出：价格指数：经季节性调整后', '商品',
                               '耐用消费品', 
                              '食品及能源',
                              '服务业',
                              '食品与能源除外'
                              ]]
title =  '美国消费支出物价指数（与上年同比）'
ylabel = '百分比'

savename = title
fig, ax = fig1_lines(linedata, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

linedata = US_PCEPI_pct.loc[:,['商品（不包括食品和能源）',  
                              '食品与能源除外',
                              '服务（不包括能源）']]
title =  '美国消费支出物价指数（不包括食品和能源，与上年同比）'
ylabel = '百分比'

savename = title
fig, ax = fig1_lines(linedata, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')
#####################################################################
###################分品类列出CPI中各项目图线
doc = twolines(US_PCEPI.iloc[:, :5],US_PCEPI_pct.iloc[:, :5],  doc, outputpath, suptitle_='美国消费支出物价指数分品类（季节调整后）',freq='每月', 
               ylabel0=unit.iloc[:, :5],ylabel1='百分比',  
               start='2022', doctex = True, figsource = '资料来源：美国BEA', doctexsource = 'CEIC, NFID')
####################################################################################


#######################
##商品价格指数
#######################
sheetname = '具体商品CPI价格'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 4
US_CPI_com, unit = xwread(filename, sheetname, start, droprowsN)
US_CPI_com = clean_df(US_CPI_com, newcolname_0='no change', Old1='消费价格：平均：',
                    Old2='', New1='', New2='', sortby =None, index_y_m='month')
unit = clean_df(unit, newcolname_0='no change', Old1='消费价格：平均：',
                    Old2='', New1='', New2='', sortby =None, index_y_m='month')
##前向插值
US_CPI_com.interpolate(method='linear', axis=0, limit=None, limit_direction='forward', inplace=True)

US_CPI_com_pct = US_CPI_com.pct_change(12, fill_method = None)*100
linedata0 = US_CPI_com.loc['2000':,['面粉', '米', '意大利面和通心粉', '面包', '所有未煮过的碎牛肉',
       '所有未煮过的烤牛肉', '生牛排', '所有猪排',
       '去骨鸡胸肉', '一磅绞碎的牛肉，100%牛肉', '绞碎的牛肉，100%牛肉',
       '带骨里脊肉块',
       '去骨肉块', '新鲜鸡肉',
       '带骨鸡胸肉']]
title =  '美国部分商品消费价格'
ylabel = '美元/镑'

savename = title
fig, ax = fig1_lines(linedata0, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

linedata1 = US_CPI_com_pct.loc['2022':,linedata0.columns]
title =  '美国部分商品消费价格（与上年同比）'
ylabel = '百分比'

savename = title
fig, ax = fig1_lines(linedata1, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')
#####################################################################
###################分品类列出CPI中各项目图线

doc = twolines(US_CPI_com,US_CPI_com_pct,  doc, outputpath, suptitle_='消费价格：平均',freq='每月', 
               ylabel0=unit,ylabel1='百分比',  
               start='2010', doctex = True, figsource = '资料来源：美国BEA', doctexsource = 'CEIC, NFID')
####################################################################################
#######################
##商品价格指数
#######################
sheetname = '农业价格指数'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 4
US_CPI_agt, unit = xwread(filename, sheetname, start, droprowsN)
US_CPI_agt = clean_df(US_CPI_agt, newcolname_0='no change', Old1='农业价格指数：',
                    Old2='', New1='', New2='', sortby =None, index_y_m='month')
unit = clean_df(unit, newcolname_0='no change', Old1='农业价格指数：',
                    Old2='', New1='', New2='', sortby =None, index_y_m='month')
##前向插值,xwread()已完成
#US_CPI_agt = US_CPI_agt.resample('ME').last()
#US_CPI_agt.interpolate(method='linear', axis=0, limit=None, limit_direction='forward', inplace=True)

US_CPI_agt_pct = US_CPI_agt.pct_change(12, fill_method = None)*100
linedata0 = US_CPI_agt.loc['2000':,:].iloc[:, :3]
title =  '美国农业价格指数'
ylabel = '2011=100'

savename = title
fig, ax = fig1_lines(linedata0, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

linedata1 = US_CPI_agt_pct.loc['2022':,:]
title =  '美国农业价格指数（与上年同比）'
ylabel = '百分比'

savename = title
fig, ax = fig1_lines(linedata1, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BEA,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')
#####################################################################
###################分品类列出CPI中各项目图线

doc = twolines(US_CPI_agt,US_CPI_agt_pct,  doc, outputpath, suptitle_='消费价格：平均',freq='每月', 
               ylabel0=unit,ylabel1='百分比',  
               start='2010', doctex = True, figsource = '资料来源：美国BEA', doctexsource = 'CEIC, NFID')
####################################################################################


####################################################
#进出口价格指数北美工业
sheetname = '进出口价格指数北美工业'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 4
US_impexp_PI,unit = xwread(filename, sheetname, start, droprowsN, dropDC=True)
#US_impexp_PI, US_imexp_PI_nan = clscols(US_impexp_PI, indicator1 = '' , indicator2 = '（停止更新）')

US_imp_PI, US_exp_PI = clscols(US_impexp_PI, indicator1 = 'IP' , indicator2 = 'EP')
unit_US_imp_PI, unit_US_exp_PI = clscols(unit, indicator1 = 'IP' , indicator2 = 'EP')

US_imp_PI =  clean_df(US_imp_PI, newcolname_0='no change',
                    Old1='IP:', New1='')
unit_US_imp_PI =  clean_df(unit_US_imp_PI, newcolname_0='no change',
                    Old1='IP:', New1='')

US_exp_PI =  clean_df(US_exp_PI, newcolname_0='no change',
                    Old1='EP：', New1='')
unit_US_exp_PI =  clean_df(unit_US_exp_PI, newcolname_0='no change',
                    Old1='EP：', New1='')

US_imp_PI_pct = US_imp_PI.pct_change(12, fill_method = None)*100

#########################分别展示各项##########
US_imp_PI_pct.fillna(0, inplace = True)
doc = twolines(US_imp_PI, US_imp_PI_pct,  doc, outputpath,  datafreq0 = 'M',datafreq1 = 'M', roundn =1, suptitle_='美国进口价格指数',freq='每月', title0='规模',title1='同比', 
             start='2000', ylabel0=unit_US_imp_PI, ylabel1 = '百分比', doctex = True, figsource = '资料来源：BLS', doctexsource = 'CEIC, NFID')

######进出口价格指数最终用途
#################
sheetname = '进出口价格指数最终用途'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 4
US_impexp_PI,unit = xwread(filename, sheetname, start, droprowsN, dropDC=True)
#US_impexp_PI, US_imexp_PI_nan = clscols(US_impexp_PI, indicator1 = '' , indicator2 = '（停止更新）')

US_imp_PI, US_exp_PI = clscols(US_impexp_PI, indicator1 = '进口价格指数' , indicator2 = '出口价格指数')
unit_US_imp_PI, unit_US_exp_PI = clscols(unit, indicator1 = '进口价格指数' , indicator2 = '出口价格指数')

US_imp_PI =  clean_df(US_imp_PI, newcolname_0='no change',
                    Old1='进口价格指数：', New1='')
unit_US_imp_PI =  clean_df(unit_US_imp_PI, newcolname_0='no change',
                    Old1='进口价格指数：', New1='')

US_exp_PI =  clean_df(US_exp_PI, newcolname_0='no change',
                    Old1='出口价格指数：', New1='')
unit_US_exp_PI =  clean_df(unit_US_exp_PI, newcolname_0='no change',
                    Old1='出口价格指数：', New1='')

US_imp_PI_pct = US_imp_PI.pct_change(12, fill_method = None)*100
linedata = US_imp_PI_pct.loc['2000':,['进口价格指数', '所有进口（不包括石油）','工业用品和材料', 
                             '资本货物', '汽车、零件和发动机', '消费品（不包括汽车）',
                             '消费品：耐用制成品']]
title =  '美国进口价格指数最终用途（与上年同比）'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(linedata, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BLS,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

linedata = US_imp_PI.loc['2000':,['进口价格指数', '所有进口（不包括石油）','工业用品和材料', 
                             '资本货物', '汽车、零件和发动机', '消费品（不包括汽车）',
                             '消费品：耐用制成品']]
title =  '美国进口价格指数最终用途（2000年=100）'
ylabel = '2000年=100'

savename = title
fig, ax = fig1_lines(linedata, title, ylabel, savename, outputpath,
                     lgncols =2, figsize = (9, 6), source ='资料来源：BLS,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')


####################################

doc = seasline(US_imp_PI_pct.iloc[:, :3],US_imp_PI_pct.iloc[:, :3], doc, outputpath,  suptitle_='进口价格指数分品类',freq='每月', ylabel0 = '百分比', ylabel1='百分比',
             start='2022', doctex = True, figsource = '资料来源：BLS', doctexsource = 'CEIC, NFID')

#########################分别展示各项##########
US_imp_PI_pct.fillna(0, inplace = True)
doc = twolines(US_imp_PI, US_imp_PI_pct,  doc, outputpath,  datafreq0 = 'M',datafreq1 = 'M', roundn =1, suptitle_='美国进口价格指数',freq='每月', title0='规模',title1='同比', 
             start='2000', ylabel0=unit_US_imp_PI, ylabel1 = '百分比', doctex = True, figsource = '资料来源：BLS', doctexsource = 'CEIC, NFID')

######进口价格指数来源国
#################
sheetname = '进口价格指数来源国'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 4
US_imp_PI_C,unit_C = xwread(filename, sheetname, start, droprowsN)
US_imp_PI_C =  clean_df(US_imp_PI_C, newcolname_0=US_imp_PI_C.columns[0],
                    Old1='进口价格指数：', New1='')
unit_C =  clean_df(unit_C, newcolname_0=unit_C.columns[0],
                    Old1='进口价格指数：', New1='')

US_imp_PI_C_pct = US_imp_PI_C.pct_change(12, fill_method = None)*100
linedata = US_imp_PI_C_pct.loc['2000':,['进口价格指数：所有进口（不包括食品和燃料）', '德国','加拿大', 
                             '墨西哥', '日本', '中国',]]
title =  '美国进口价格指数来源国（与上年同比）'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(linedata, title, ylabel, savename, outputpath,ylinetick=None, 
                     lgncols =2, figsize = (9, 6), source ='资料来源：BLS,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

linedata = US_imp_PI_C.loc['2000':,['进口价格指数：所有进口（不包括食品和燃料）', '德国','加拿大', 
                             '墨西哥', '日本', '中国',]]
title =  '美国进口价格指数来源国'
ylabel = '2000年=100'
savename = title
fig, ax = fig1_lines(linedata, title, ylabel, savename, outputpath, ylinetick=None, 
                     lgncols =2, figsize = (9, 6), source ='资料来源：BLS,国家金融与发展实验室')
ax.legend = ['进口价格指数：所有进口，不包括食品和燃料（2000=100）', '德国（2003=100）','加拿大（2000=100）', 
                             '墨西哥（2003.12=100）', '日本（2000=100）', '中国（2003.12=100）',]
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')
#########################分别展示各项##########
US_imp_PI_C_pct.fillna(0, inplace = True)
doc = twolines(US_imp_PI_C, US_imp_PI_C_pct,  doc, outputpath,  datafreq0 = 'M',datafreq1 = 'M', roundn =1, suptitle_='美国进口价格指数',freq='每月', title0='定基',title1='同比', 
             start='2005', ylabel0=unit_C, ylabel1 = '百分比', doctex = True, figsource = '资料来源：BLS', doctexsource = 'CEIC, NFID')

#############美国PPI，最终需求#####
############美国PPI###
sheetname = 'PPI最终需求中间需求商品分类行业分类'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 3
US_PPI_FD,unit = xwread(filename, sheetname, start, droprowsN,freq='M')
US_PPI_FD_pct12 = US_PPI_FD.pct_change(12, fill_method = None) *100
US_PPI_FD_pct1 = US_PPI_FD.pct_change(1, fill_method = None) *100
plotdata = US_PPI_FD.loc['2008':, ['生产者价格指数：最终需求', '生产者价格指数：最终：货物', 
                     '生产者价格指数：最终：服务业', '生产者价格指数：最终：建筑业', 
                     '生产者价格指数（PPI）：商品类型（CT）：中间需求（ID）：加工产品（PG）', 
                     '生产者价格指数']]

title = '美国生产者价格指数（2009年11月=100）'
ylabel = ''
savename = title
fig, ax = fig1_lines(plotdata, title, ylabel, savename, outputpath,ylinetick=100, 
                     lgncols =1, figsize = (9, 6), source ='资料来源：BLS,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

##############
plotdata = US_PPI_FD_pct12.loc['2008':, ['生产者价格指数：最终需求', '生产者价格指数：最终：货物', 
                     '生产者价格指数：最终：服务业', '生产者价格指数：最终：建筑业', 
                     '生产者价格指数（PPI）：商品类型（CT）：中间需求（ID）：加工产品（PG）', 
                     '生产者价格指数']]

title = '美国生产者价格指数（与上年同比）'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(plotdata, title, ylabel, savename, outputpath,
                     lgncols =1, figsize = (9, 6), source ='资料来源：BLS,国家金融与发展实验室') 
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

#######################################################
sheetname = 'PPI中间需求生产阶段'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 3
US_PPI_id,unit = xwread(filename, sheetname, start, droprowsN,freq='M')
US_PPI_id_pct12 = US_PPI_id.pct_change(12, fill_method = None) *100
US_PPI_id_pct1 = US_PPI_id.pct_change(1, fill_method = None) *100
US_PPI_id_pct12.plot()

sheetname = 'PPI商品分类详细'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 3
US_PPI_item,unit = xwread(filename, sheetname, start, droprowsN,freq='M')
US_PPI_item_pct12 = US_PPI_item.pct_change(12, fill_method = None) *100
US_PPI_item_pct1 = US_PPI_item.pct_change(1, fill_method = None) *100

############美国PPI###
sheetname = 'PPI商品分类行业分类'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 3
US_PPI,unit = xwread(filename, sheetname, start, droprowsN,freq='M')
US_PPI, US_PPI_non = clscols(US_PPI,indicator1 = '' , indicator2 = '（停止更新）') ##区分原序列和SA序列
unit = unit.loc[:, US_PPI.columns]
US_PPI_pct12 = US_PPI.pct_change(12, fill_method = None) *100
US_PPI_pct1 = US_PPI.pct_change(1, fill_method = None) *100


pd.DateOffset(days=1)

#plt.figure()

US_PPI.loc['2008':, ['生产者价格指数', '生产者价格指数：农产品', '生产者价格指数：加工食品和饲料', '生产者价格指数：工业商品（不包括燃料）',
       '生产者价格指数：工业商品', '生产者价格指数：农产品、加工食品和饲料', '生产者价格指数：纺织品及服装',
       '生产者价格指数：生皮、皮革及制品', '生产者价格指数：燃料、燃料产品和能源', '生产者价格指数：化学品及相关产品',
       '生产者价格指数：橡胶和塑料', '生产者价格指数：木材和木头', '生产者价格指数：纸浆、纸及相关产品',
       '生产者价格指数：金属和金属制品', '生产者价格指数：机械和设备', '生产者价格指数：家具和家居耐用品', '生产者价格指数：非金属矿物',
       '生产者价格指数：交通运输设备', '生产者价格指数：其他产品、不另详述', '生产者价格指数（PPI）：采矿业',
       '生产者价格指数（PPI）：公用事业', '生产者价格指数（PPI）：制造业', '生产者价格指数（PPI）：服务业',
       '生产者价格指数（PPI）：建筑业', '生产者价格指数（PPI）：Special Indices (SI)']]
US_PPI_pct12.loc['2008':, ['生产者价格指数', '生产者价格指数：农产品', '生产者价格指数：加工食品和饲料', '生产者价格指数：工业商品（不包括燃料）',
       '生产者价格指数：工业商品', '生产者价格指数：农产品、加工食品和饲料', '生产者价格指数：纺织品及服装',
       '生产者价格指数：生皮、皮革及制品', '生产者价格指数：燃料、燃料产品和能源', '生产者价格指数：化学品及相关产品',
       '生产者价格指数：橡胶和塑料', '生产者价格指数：木材和木头', '生产者价格指数：纸浆、纸及相关产品',
       '生产者价格指数：金属和金属制品', '生产者价格指数：机械和设备', '生产者价格指数：家具和家居耐用品', '生产者价格指数：非金属矿物',
       '生产者价格指数：交通运输设备', '生产者价格指数：其他产品、不另详述', '生产者价格指数（PPI）：采矿业',
       '生产者价格指数（PPI）：公用事业', '生产者价格指数（PPI）：制造业', '生产者价格指数（PPI）：服务业',
       '生产者价格指数（PPI）：建筑业', '生产者价格指数（PPI）：Special Indices (SI)']]


US_PPI.loc['1986':, ['生产者价格指数', '生产者价格指数（PPI）：采矿业', '生产者价格指数（PPI）：公用事业',
                     '生产者价格指数（PPI）：制造业', '生产者价格指数（PPI）：服务业',
                     '生产者价格指数（PPI）：建筑业', '生产者价格指数（PPI）：Special Indices (SI)']].plot()

plotdata = US_PPI_pct12.loc['1986':, ['生产者价格指数', '生产者价格指数（PPI）：采矿业', '生产者价格指数（PPI）：公用事业',
                     '生产者价格指数（PPI）：制造业', '生产者价格指数（PPI）：服务业',
                     '生产者价格指数（PPI）：建筑业', '生产者价格指数（PPI）：Special Indices (SI)']]

#plotdata = plotdata.sort_values(by = plotdata.index[-1], axis = 1, ascending=False)

title = '美国分行业生产者价格指数（与上年同比）'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(plotdata, title, ylabel, savename, outputpath,
                     lgncols =1, figsize = (9, 6), source ='资料来源：BLS,国家金融与发展实验室') 

doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')
####################分品类图线#####################
doc = twolines(US_PPI,US_PPI_pct12, doc, outputpath,
               suptitle_='美国PPI',title0 = '定基', title1 = '同比', ylabel0 = unit, ylabel1='百分比',
             start='2022', doctex = True, figsource = '资料来源：BLS', doctexsource = 'CEIC, NFID')

#######################################################
'''Index(['居民消费价格指数：同比：月度：SA：美国', '居民消费价格指数：同比：月度：SA：中国台湾', '生产者价格指数：同比：月度：中国',
       '居民消费价格指数：同比：月度：SA：印度', '居民消费价格指数：同比：月度：SA：中国香港特别行政区',
       '居民消费价格指数：同比：月度：日本', '居民消费价格指数：同比：月度：印度', '居民消费价格指数：同比：月度：中国',
       '核心居民消费价格指数：同比：月度：印度', '核心居民消费价格指数：同比：月度：中国', '生产者价格指数：同比：月度：SA：印度',
       'M2：同比：月度：美国', 'M2：同比：月度：印度', 'M2：同比：月度：中国', '生产者价格指数：同比：月度：美国',
       '核心居民消费价格指数：同比：月度：日本', '生产者价格指数：同比：月度：SA：日本', 'M2：同比：月度：日本',
       'M2：同比：月度：SA：中国', 'M2：同比：月度：SA：印度', 'M2：同比：月度：SA：日本', 'M2：同比：月度：SA：美国',
       'M2：同比：月度：SA：法国', 'M2：同比：月度：SA：德国', 'M2：同比：月度：俄罗斯', 'M2：同比：月度：英国',
       'M2：同比：月度：法国', 'M2：同比：月度：欧元区', '货币供应 M2：百万美元：月度：中国',
       '货币供应 M2：百万美元：月度：印度', '货币供应 M2：百万美元：月度：日本', '货币供应 M2：百万美元：月度：法国',
       '货币供应 M2：百万美元：月度：欧元区', '货币供应 M2：百万美元：月度：英国', '货币供应 M1：SA', '货币供应 M2：SA',
       '货币供应 M2：SA：小额定期存款', '货币供应 M1', '货币供应 M2', '货币供应 M2：小额定期存款'],'''
##################################################################################

sheetname = 'M1M2'
filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
start = 'A1'; droprowsN = 3
US_M1M2,unit = xwread(filename, sheetname, start, droprowsN,freq='M')
US_M1M2 = US_M1M2*10     ##亿美元

#####美国M2与CPI
US_M1M2['生产者价格指数：同比：月度：美国'] = US_PPI_FD_pct12['生产者价格指数']
US_M1M2['生产者价格指数：最终需求：同比：月度：美国'] = US_PPI_FD_pct12['生产者价格指数：最终需求']

US_M1M2['城市居民消费价格指数：SA：所有项目，扣除食品和能源：同比：月度：美国'] =  US_CPI_U_pct12[
    '城市居民消费价格指数：SA：所有项目（不包括食品和能源）']

plotdata = US_M1M2.loc[:,['居民消费价格指数：同比：月度：SA：美国','M2：同比：月度：SA：美国']]    ###调整单位
plotdata.plot(alpha = 0.8)

#####延长时间，
shift_ls = 18
#out_index = pd.date_range(plotdata.index[-1], periods=30, freq="ME") +  pd.DateOffset(days=1)  转换为月初数据
out_index = pd.date_range(plotdata.index[-1], periods=31, freq="ME")
out_US_M1M2 = pd.DataFrame(index=out_index[1:], columns=US_M1M2.columns)
snsdata = pd.concat([US_M1M2, out_US_M1M2], axis=0)
snsdata['M2：同比：月度：美国(前置18个月)'] =  snsdata['M2：同比：月度：美国'].shift(shift_ls)
snsdata['M2：同比：月度：SA：美国'] = snsdata['货币供给M2：经季节性调整后'].pct_change(12, fill_method = None)*100
snsdata['M2：同比：月度：SA：美国(前置18个月)'] =  snsdata['M2：同比：月度：SA：美国'].shift(shift_ls)   

snsdata['M1：同比：月度：SA：美国'] = snsdata['货币供给M1：经季节性调整后'].pct_change(12, fill_method = None)*100
snsdata['M1：同比：月度：SA：美国(前置18个月)'] =  snsdata['M1：同比：月度：SA：美国'].shift(shift_ls)   

pdata =  snsdata.loc['2000':, ['M2：同比：月度：美国(前置18个月)',
                               '生产者价格指数：同比：月度：美国',
                               '居民消费价格指数：同比：月度：美国']]


title = '美国M2、PPI和CPI同比'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(pdata, title, ylabel, savename, outputpath)
doc = frame_image1(doc, title, savename + r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')

############################################################

###美国PPI和CPI##############
pdata =  US_M1M2.loc['2000':, ['生产者价格指数：同比：月度：美国','生产者价格指数：最终需求：同比：月度：美国', 
                               '居民消费价格指数：同比：月度：美国',
                               '城市居民消费价格指数：SA：所有项目，扣除食品和能源：同比：月度：美国' ]]
pdata = pdata.dropna(axis = 0)
#pdata = pdata.sort_values(by = pdata.index[-1], ascending = False, axis =1)

title = '美国PPI和CPI同比'
ylabel = '百分比'
savename = title
fig, ax = fig1_lines(pdata, title, ylabel, savename, outputpath,
                     lgncols =1, figsize = (9, 6), source ='资料来源：BLS,国家金融与发展实验室') 


doc = frame_image1(doc, title, title+ r'.pdf', '''''', 
                source, width = r'0.8\textwidth',height = r'0.8\textheight')               


#########################################################
lastpartsalmon(doc, outputname = 'beamer_USeconomy_inflation' )

##############################################################
#打开tex 文件，用xetex+index 形成pdf文件
#######################################################