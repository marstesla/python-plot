############
#######https://www.lfd.uci.edu/~gohlke/pythonlibs/
######清华大学镜像
###py -3.9 -m pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple   some-package
###py -3.10 -m pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple   some-package

#scripts to demo operate Excel via VBA
#这一部分是汪红驹编写的读写xlsx, 作图模板，汪红驹
#万德数据下载后作图,#CEIC 数据，各省数据
#在C:\Program Files\Anaconda3\Lib\site-packages\matplotlib\mpl-data中的matplotlibrc, copy 到C:\Users\rongxiw\.matplotlib里，修改
#font.sans-serif   ： SimHei
#axes.unicode_minus:  False
#axes.prop_cycle: cycler('color',['1f77b4', 'aec7e8', 'ff7f0e', 'ffbb78', '2ca02c', '98df8a', 'd62728', 'ff9896', '9467bd', 'c5b0d5', '8c564b', 'c49c94', 'e377c2', 'f7b6d2', '7f7f7f', 'c7c7c7', 'bcbd22', 'dbdb8d', '17becf', '9edae5'])

#mpl ,plt.show()中断进程，close figure 以后才能继续
#PPI_CS.astype('float64')     #所有数据应转换为numpy.float64   同一个dataframe的数据必须同类型

###docx输出word 文档
#from docx import Document
#from docx.shared import Pt
#from docx.enum.text import WD_ALIGN_PARAGRAPH
#from docx.oxml.ns import qn
#from docx.shared import RGBColor
#from docx.shared import Inches

#####从wind提取美国国债收益率
from pylatex.utils import italic, bold, NoEscape, escape_latex

from WindPy import w
####
from pandas_datareader import wb
import textwrap
import statsmodels.formula.api as smf
import statsmodels.api as sm

from colorama import Fore,Back,Style,init
init(autoreset=True)
import matplotlib as mpl
#mpl.get_backend()
#mpl.use('Qt4Agg')
mpl.use('TkAgg')
mpl.interactive(True)     #打开interactive mode
#mpl.is_interactive()
#mpl.rcParams['backend'] = 'SVG'
import os, sys
#import win32com.client
from collections import OrderedDict
import pandas as pd

# Changing option to consider infinite as nan
#pd.set_option_context('mode.use_inf_as_na', True)
pd.option_context('mode.use_inf_as_na', True)
import math
from pandas import Series, DataFrame
import numpy as np
from scipy import *
import datetime as dt
import matplotlib.pyplot as plt
#mpl.get_configdir()  ## 'C:\\Users\\hjuw2\\.matplotlib'
#plt.ion()   #turn on interactive mode, plt.ioff()  #turn off
import matplotlib.ticker as ticker
#plt.rcdefaults()
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import BoxStyle
from matplotlib.path import Path
from matplotlib.dates import DAILY
import time
import xlwings as xw
from matplotlib import cm   #colormap
import re   
import seaborn as sns     #修改了mpl.get_backend(),为agg,修改了 plot   style  ,颜色平淡，不用seaborn， 采用文件matplotlibrc自定义的颜色，可以获得好看的颜色
#有问题axes.prop_cycle: cycler('color',['1f77b4', 'aec7e8', 'ff7f0e', 'ffbb78', '2ca02c', '98df8a', 'd62728', 'ff9896', '9467bd', 'c5b0d5', '8c564b', 'c49c94', 'e377c2', 'f7b6d2', '7f7f7f', 'c7c7c7', 'bcbd22', 'dbdb8d', '17becf', '9edae5'])
mpl.use('TkAgg')
#mpl.use('qtagg')    ###已经安装pyQt6
mpl.interactive(True)     #打开interactive mode


from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#plt.style.use('seaborn-whitegrid')
#sns.set(style='ticks', palette='Set2')    #中文显示有问题，需要修改
mpl.rcParams['font.sans-serif'] = ['SimHei']  #指定默认字体
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
mpl.rcParams['savefig.dpi'] = 600
mpl.rcParams['lines.linewidth'] = 3
#from cycler import cycler  #不能转换为RGB,有问题
#mpl.rcParams['axes.prop_cycle'] = plt.cycler(color=['1f77b4', 'aec7e8', 'ff7f0e', 'ffbb78', '2ca02c', '98df8a', 'd62728', 'ff9896', '9467bd', 'c5b0d5', '8c564b', 'c49c94', 'e377c2', 'f7b6d2', '7f7f7f', 'c7c7c7', 'bcbd22', 'dbdb8d', '17becf', '9edae5'])
#mpl.rcParams['axes.prop_cycle'] = plt.cycler(color=['r', 'g', 'b', 'y'])
#linestyles = [(0, (1, 0)),(0, (1, 10)),(0, (1, 1)),(0, (2, 1)),(0, (5, 10)),(0, (5, 5)),(0, (5, 1)),(0, (3, 10, 1, 10)),(0, (3, 5, 1, 5)),(0, (3, 1, 1, 1)),(0, (3, 5, 1, 5, 1, 5)),(0, (3, 10, 1, 10, 1, 10)),(0, (3, 1, 1, 1, 1, 1))]
#mpl.rcParams['axes.prop_cycle'] = plt.cycler(linestyle=linestyles)
#plt.style.use('tableau-colorblind10')
#plt.style.use('ggplot')
#import mplcursors
#import seaborn as sns
#sns.set(style='ticks', palette='Set2')    #中文显示有问题，需要修改
#sns.despine()
#mpl.rcParams['font.sans-serif'] = ['SimHei']  #指定默认字体
#mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
# Remove top and right axes lines ("spines")

'''
########设计曲线颜色+ 线形
##方案1
from cycler import cycler
cc = (cycler(color=list('rgby')) +
                  cycler(linestyle=['-', '--', ':', '-.']))
plt.rc('lines', linewidth=3)
plt.rc('axes', prop_cycle=cc)
##方案2
from cycler import cycler
cc = (cycler(color=list('rgby')) *
                  cycler(linestyle=['-', '--', ':', '-.']))
plt.rc('lines', linewidth=3)
plt.rc('axes', prop_cycle=cc)

##方案3
colors = list('krgbmy')
linestyles = [(0, (1, 0)),(0, (1, 0.5)),(0, (1, 1)),(0, (2, 0.5)),(0, (2, 1)),(0, (3, 0.5)),(0, (5, 1)),(0, (2, 1, 1, 1)),(0, (3, 0.5, 1, 0.5)),(0, (3, 1, 1, 1)),(0, (2, 1, 1, 0.5, 1, 0.5)),(0, (3, 0.5, 1, 0.5, 1, 0.5)),(0, (3, 1, 1, 1, 1, 1))]
from cycler import cycler
cc = (cycler(color=colors) *
      cycler(linestyle=linestyles))
plt.rc('lines', linewidth=3)
plt.rc('axes', prop_cycle=cc)
'''



######
import subprocess
import os
#inkscapePath = r"C:\Inkscape\bin\inkscape.exe"
#savePath= r"G:\E\python_w\data"
def export_Emf(savePath, plotName, fig=None, keepSVG=False):
    """Save a figure as an emf file

    Parameters
    ----------
    savePath : str, the path to the directory you want the image saved in
    plotName : str, the name of the image 
    fig : matplotlib figure, (optional, default uses gca)
    keepSVG : bool, whether to keep the interim svg file
    """
    #plotName = 'sine_emf'
    figFolder = savePath + r"\{}.{}"
    svgFile = figFolder.format(plotName,"svg")
    emfFile = figFolder.format(plotName,"emf")
    #pdfFile = figFolder.format(plotName,"pdf")
    if fig:
        use=fig
    else:
        use=plt
    use.savefig(svgFile)
#    subprocess.run([inkscapePath, svgFile, '--export-emf', emfFile])
    subprocess.call(r"C:\inkscape\bin\inkscape.exe"+ " --export-filename="
                    +emfFile + " " +svgFile)
    #subprocess.call(r"C:\inkscape\bin\inkscape.exe"+ " --export-filename="
    #                +pdfFile + " " +svgFile)    
    if not keepSVG:
        os.system('del "{}"'.format(svgFile))
#Example Usage
#savePath= r"G:\E\python_w\data"
#import numpy as np
#tt = np.linspace(0, 2*3.14159)
#plt.plot(tt, np.sin(tt))
#export_Emf_pdf(savePath, 'sine_emf',keepSVG=True)
##################################
def svg2pdf(ext0 = 'svg',ext2 = 'pdf',dirpath = '.\\data',savePath = '.\\data\\image_pdf'):
    """把ext0  转换为ext2,批量转
    有些svg 不能转换为pdf, 数据遗失， 用plt.savefig(...., '....pdf')更好
    Parameters
    ----------
    savePath : str, the path to the directory you want the image saved in
    """
    #
    #files = [f for f in os.listdir('.\\data') if os.path.isfile(f)]
    #files = [f for f in os.listdir('./data')]
    #files = filter(lambda f: f.endswith(('.pdf','.PDF')), files)    
    #file_list = list(files)    
    #ext0 = 'svg'; ext2 = 'pdf';dirpath = '.\\data';savePath = '.\\data'
    from os import path
    from glob import glob  
    import subprocess
    file_list = glob(path.join(dirpath,"*.{}".format(ext0)))  #svg图文件名的list
    #file_list = glob(".\\data\\*.svg")  #也可以写出 svg图片的文件名的list
    for ii,svgFile in enumerate(file_list):
        pdfFile = savePath + r"\\" +svgFile.rstrip('.svg').lstrip(dirpath) + ".pdf"
        subprocess.call(r"C:\inkscape\bin\inkscape.exe"+ " --export-filename="
                    +pdfFile + " " +svgFile)    
        print('图'+str(ii), svgFile.lstrip('.\\data\\').rstrip('.svg'))
    
#################################################################################

def NBERdate_plot(ax1):
    ###NBER 经济周期日期
    sheetname = 'NBER chronology'
    #filename = source_drive + r"\D\www\macromodels\IECASS\NBER_chronology_062020.xlsx"
    filename = source_drive + r"\D\www\macromodels\IECASS\NBER_chronology_072021.xlsx"
    #start = 'C3'; droprowsN = 0
    #US_GDP_depression = xwread(filename, sheetname, start, droprowsN)
    sht = xw.Book(filename).sheets[sheetname]
    
    date_recession = sht.range((27,3),(38,4)).value
    #df = sht.range(start).options(pd.DataFrame, expand='table',empty = np.nan).value
    #date_recession[-1] = ['February 2020','April 2020']   #结束日期暂定为 June 2020，方便作图，20200719NBER公告202002-202004是峰-谷衰退期
    for dr in date_recession:
        #xmin = dr[0]
        #xmax = dr[1]
        #[re.findall(".*:(.*):.*",col)[0] for col in list(PPI.columns)]    #匹配两个 : 之间的字符
        if '\xa0' in dr[0]:
            xmin = re.findall("\A(.*)\xa0", dr[0])[0]
        else:
            xmin = re.findall("\A(.*) ",dr[0])[0]   #删除' '之后的字符
        if '\xa0' in dr[1]:
            xmax = re.findall("\A(.*)\xa0", dr[1])[0]
        else:
            xmax = re.findall("\A(.*) ",dr[1])[0]   #删除' '之后的字符
        ax1.axvspan(xmin, xmax,facecolor='0.8', alpha=0.5)
    return(date_recession)
##########################################################

#################################################
###月度累计值转变为单个月度的增加值
def  csm2m(csm, mode = 'normal'):   #月累计转换为单月值
    if mode == 'normal':
        AAA = csm-csm.shift(1)
        AAA[AAA.index.month==1] = csm[csm.index.month==1].values           #一月份序列
    elif mode == 'm1=m2':
        AAA = csm-csm.shift(1)
        AAA[AAA.index.month==1] = (csm[csm.index.month==2] /2).values           #一月份序列
        AAA[AAA.index.month==2] = (csm[csm.index.month==2] /2).values            #二月份序列
    AAA_grth = AAA.div(AAA.shift(12))*100
    return(AAA)

###月度累计值转变为单个季度的增加值
def csm2q(csm):
    csm_Q = csm.resample('QE').last()
    BBB = csm_Q-csm_Q.shift(1)
    BBB[BBB.index.month==3] = csm_Q[csm_Q.index.month==3]           #一季度序列
    BBB_grth = BBB.div(BBB.shift(4))*100
    return(BBB)
#####################################################################
def m2csm(trade_m_bycountry, start = 1):
    ###start = 1, 表示1月开始，  10，表示10月开始,美国财年
    if start == 1:
        aaa = trade_m_bycountry.groupby([trade_m_bycountry.index.year,
                                         trade_m_bycountry.index.month]).last()  #按年， 月排列，pivot
        aaa.rename_axis(index = ['年度','月份'],inplace = True)
        trade_csm_bycountry = aaa.groupby(level =0).cumsum()
        trade_csm_bycountry.index = trade_m_bycountry.index
    elif start > 1:  
        trade_m_bycountry.index = trade_m_bycountry.index.shift(13-start)
        aaa = trade_m_bycountry.groupby([trade_m_bycountry.index.year,
                                             trade_m_bycountry.index.month]).last()  #按年， 月排列，pivot
        aaa.rename_axis(index = ['年度','月份'],inplace = True)
        trade_csm_bycountry = aaa.groupby(level =0).cumsum()
        trade_csm_bycountry.index = trade_m_bycountry.index.shift(start-13)        
        trade_m_bycountry.index = trade_m_bycountry.index.shift(start-13)   #将原始数据index 复原
    return(trade_csm_bycountry)
#######################################################
def m2lj(trade):   #求累计值，累计同比
    aaa = trade.groupby([trade.index.year,trade.index.month]).sum()  #按年， 月排列，pivot
    aaa.rename_axis(index = ['年度','月份'],inplace = True)
    ###累计同比
    trade_csm = aaa.groupby(level =0).cumsum()
    trade_csm.index = trade.index
    #trade_csm_pct = trade_csm.pct_change(periods = 12)*100
    trade_csm_pct = (trade_csm/trade_csm.shift(+12)-1)*100
    return(trade_csm,trade_csm_pct)
##################################################################
def w2lj(unemployment_state0, mask0 = True):   #求累计值，累计同比
    date = unemployment_state0.reset_index().iloc[:, 0]
    week = date.apply(lambda x: x.week)
    weekdf = pd.DataFrame(data=week.values, index = unemployment_state0.index, columns =['week'])
    unemployment_state0_week = pd.concat([unemployment_state0, weekdf], axis=1)
    unemployment_state0_week_yw = unemployment_state0_week.groupby([unemployment_state0_week.index.year,unemployment_state0_week['week']]).sum().copy(deep = True)
    unemployment_state0_week_yw.rename_axis(index = ['年度','周'],inplace = True)
    if mask0 == True:
        unemployment_state0_week_yw.mask(unemployment_state0_week_yw==0,np.nan,inplace = True)
       
    ###累计同比
    unemployment_state0_week_csm = unemployment_state0_week_yw.groupby(level =0).cumsum()
    unemployment_state0_week_csm.index = unemployment_state0.index
    #trade_csm_pct = trade_csm.pct_change(periods = 12)*100
    unemployment_state0_week_csm_pct = (unemployment_state0_week_csm/unemployment_state0_week_csm.shift(+52)-1)*100
    return(unemployment_state0_week_csm,unemployment_state0_week_csm_pct)

#######################################################################
def despine(ax):
    #输入图像的ax,  ++++=====>ax = plt.gca()
    #import seaborn as sns
    #sns.set_style("white")
    #sns.set_style("ticks")
    #mpl.rcParams['font.sans-serif'] = ['SimHei']
    #mpl.rcParams['axes.unicode_minus'] = False  #显示中文
    # sns.despine(offset=10, trim=True)
    #sns.despine(left=deleftspine,offset = offset, trim = trim)
    #ax = plt.gca()
    ax.tick_params(axis='y', which='both', right='True', direction='out', labelleft='True', labelright='True')
    for spine in ['left','right','top']:
        ax.spines[spine].set_visible(False)
    ax.legend(frameon=False)
def seasplot(deficit,start,column,title,ylabel,newfig = True,detail = True, legcolsn = 1,legend = True, mask0 = True):
    deficit_ym = deficit.groupby([deficit.index.year,deficit.index.month]).sum().copy(deep = True)
    deficit_ym.rename_axis(index = ['年度','月份'],inplace = True)
    if mask0 == True:
        deficit_ym.mask(deficit_ym==0,np.nan,inplace = True)
    snsdata = deficit_ym.unstack().loc[start:,(column)].T
    if newfig:
        plt.figure()        
    if detail== True:     ####画每年的曲线
        #snsdata.plot(title = title,linewidth = 3)  #比较不同年份，相同月份  图线为实线
        if legcolsn > 0:
            sns.lineplot(data=snsdata, palette="tab10", linewidth=3)
            plt.legend(ncols = legcolsn)
        elif legcolsn ==0:
            sns.lineplot(data=snsdata, palette="tab10", linewidth=3)
            plt.legend().set_visible(False)
            
    elif detail == 'mean': ####画前些年的均值
        mean = snsdata.iloc[:,0:-1].mean(axis =1)
        mini = snsdata.iloc[:,0:-1].min(axis =1)
        maxi = snsdata.iloc[:,0:-1].max(axis =1)
        plt.plot(snsdata.index,snsdata.iloc[:,-1],'r')
        plt.fill_between(mini.index, mini,maxi, color="b", alpha=0.2)
        plt.plot(mean.index,mean,'b',linewidth = 1)
        plt.plot(snsdata.index,snsdata.iloc[:,-2],'g')
        #plt.plot(snsdata.index,snsdata.iloc[:,-1])
        #plt.fill_between(mini.index, mini,maxi, color="b", alpha=0.2)
        #plt.plot(mean.index,mean,linewidth = 1)
        #plt.plot(snsdata.index,snsdata.iloc[:,-2])
        if legcolsn > 0:            
            plt.legend([str(snsdata.columns[-1])+'年',
                        str(snsdata.columns[0]) +'-' + str(snsdata.columns[-2])+'年',
                        '均值',
                        str(snsdata.columns[-2])+'年'], ncols = legcolsn)
    if legend == False:
        ax1.get_legend().set_visible(False)
    plt.ylabel(ylabel),plt.title(title)
    return(deficit_ym)
def seasplot1(fig1, ax1,deficit,start,column,title,ylabel,detail = True, legloc = 'upper left', legcolsn = 1,legend = True, mask0=True):
    deficit_ym = deficit.groupby([deficit.index.year,deficit.index.month]).sum().copy(deep = True)
    deficit_ym.rename_axis(index = ['年度','月份'],inplace = True)
    if mask0 == True:
        deficit_ym.mask(deficit_ym==0,np.nan,inplace = True)
    snsdata = deficit_ym.unstack().loc[start:,(column)].T
    if detail== True:     ####画每年的曲线
        #snsdata.plot(title = title,linewidth = 3)  #比较不同年份，相同月份  图线为实线
        sns.lineplot(ax = ax1,data=snsdata, palette="tab10", linewidth=3)
        ax1.legend(ncols = legcolsn, loc =legloc)
    elif detail == 'mean': ####画前些年的均值
        mean = snsdata.iloc[:,0:-1].mean(axis =1)
        mini = snsdata.iloc[:,0:-1].min(axis =1)
        maxi = snsdata.iloc[:,0:-1].max(axis =1)
        ax1.plot(snsdata.index,snsdata.iloc[:,[-1]],'r')
        ax1.fill_between(mini.index, mini,maxi, color="b", alpha=0.2)
        ax1.plot(mean.index,mean,'b',linewidth = 1)
        ax1.plot(snsdata.index,snsdata.iloc[:,[-2]],'g')
        #plt.plot(snsdata.index,snsdata.iloc[:,-1])
        #plt.fill_between(mini.index, mini,maxi, color="b", alpha=0.2)
        #plt.plot(mean.index,mean,linewidth = 1)
        #plt.plot(snsdata.index,snsdata.iloc[:,-2])
        ax1.legend([str(snsdata.columns[-1])+'年',
                    str(snsdata.columns[0]) +'-' + str(snsdata.columns[-2])+'年',
                    '均值',
                    str(snsdata.columns[-2])+'年'], ncols = legcolsn, loc =legloc)
    if legend == False:
        ax1.get_legend().set_visible(False)
    ax1.set_ylabel(ylabel); ax1.set_title(title); 
    return(deficit_ym,(fig1,ax1))


def seas_week_plot1(fig1, ax1,unemployment_state0,start,column,title,ylabel,detail = True, legloc = 'upper left', legcolsn = 1,legend = True, mask0=True):
    #start = '2022'; column = unemployment_state0.columns[0]
    date = unemployment_state0.reset_index().iloc[:, 0]
    week = date.apply(lambda x: x.week)
    weekdf = pd.DataFrame(data=week.values, index = unemployment_state0.index, columns =['week'])
    unemployment_state0_week = pd.concat([unemployment_state0, weekdf], axis=1)
    unemployment_state0_week_yw = unemployment_state0_week.groupby([unemployment_state0_week.index.year,unemployment_state0_week['week']]).sum().copy(deep = True)
    unemployment_state0_week_yw.rename_axis(index = ['年度','周'],inplace = True)
    if mask0 == True:
        unemployment_state0_week_yw.mask(unemployment_state0_week_yw==0,np.nan,inplace = True)
    snsdata = unemployment_state0_week_yw.unstack().loc[start:,(column)].T
    if detail== True:     ####画每年的曲线
        #snsdata.plot(title = title,linewidth = 3)  #比较不同年份，相同月份  图线为实线
        sns.lineplot(ax = ax1,data=snsdata, palette="tab10", linewidth=3)
        ax1.legend(ncols = legcolsn, loc =legloc)
    elif detail == 'mean': ####画前些年的均值
        mean = snsdata.iloc[:,0:-1].mean(axis =1)
        mini = snsdata.iloc[:,0:-1].min(axis =1)
        maxi = snsdata.iloc[:,0:-1].max(axis =1)
        ax1.plot(snsdata.index,snsdata.iloc[:,[-1]],'r')
        ax1.fill_between(mini.index, mini,maxi, color="b", alpha=0.2)
        ax1.plot(mean.index,mean,'b',linewidth = 1)
        ax1.plot(snsdata.index,snsdata.iloc[:,[-2]],'g')
        #plt.plot(snsdata.index,snsdata.iloc[:,-1])
        #plt.fill_between(mini.index, mini,maxi, color="b", alpha=0.2)
        #plt.plot(mean.index,mean,linewidth = 1)
        #plt.plot(snsdata.index,snsdata.iloc[:,-2])
        ax1.legend([str(snsdata.columns[-1])+'年',
                    str(snsdata.columns[0]) +'-' + str(snsdata.columns[-2])+'年',
                    '均值',
                    str(snsdata.columns[-2])+'年'], ncols = legcolsn, loc =legloc)
    if legend == False:
        ax1.get_legend().set_visible(False)
    ax1.set_ylabel(ylabel); ax1.set_title(title); 
    return(unemployment_state0_week_yw,(fig1,ax1))


def xwread_wind(filename,sheetname,freq='M',start = 'A2', droprowsN=2):
    #读wind下载的excel 数据
    #filename = r"E:\python_w\wind数据表.xlsx"
    #sheetname = '固定资产投资比重'
    #droprows = ['单位','来源']
    #filename = r"E:\python_w\经济增长率环比折年率.xlsx"; sheetname = '美国投资'; droprows = ['频率']
    #start='A2'
    sht = xw.Book(filename).sheets[sheetname]
    df = sht.range(start).options(pd.DataFrame, expand='table').value
    if 'Unit' in list(df.index):
        Unit = df.loc['Unit',:]    #保存单位
    elif '单位' in list(df.index):
        Unit = df.loc['单位',:    ]    #保存单位
    if type(droprowsN) is int:
        df = df.drop(df.index[:droprowsN],axis = 0)    
    elif type(droprowsN) is list:
        df = df.drop(droprowsN,axis = 0)   
    df.index.name = ''
    index = pd.to_datetime(df.index)
    df.index =index   #转换为datetime为轴的序列
    df = df.astype('float64',copy=False, errors='raise')    #转换数据类型，统一
    if freq == 'D':
        df = df.resample('D').last()
    elif freq == 'W':
        df = df.resample('W').last()
    elif freq == 'M':
        df = df.resample('ME').last()   ###月底最后一天
    elif freq == 'Q':
        df = df.resample('QE').last()
    elif freq == 'A':
        df = df.resample('YE').last()
    elif freq == 'fiscalyear':    ###美国财年，9月最后一天
        #df = df.shift(periods =1,freq = 'M')  ##index前移1个月时间
        #df = df.shift(periods =-1,freq = 'D')  ##index后移1天时间    变为09-30
        df = df.resample('YE-SEP').last()
    #df.to_period
    #return(df,Unit)
    return(df)
    #----------------------------------------------------------------------
def xwread_ceic(filename,sheetname,droprowsN=10):
    #读CEIC下载的excel 数据
    #sheetname = '税收和政府性基金收入图'
    #filename = r"H:\D\www\macromodels\Leading\Macro_Workspace_2q(jjxdtai).xlsx"
    #droprows = ['单位','来源']
    sht = xw.Book(filename).sheets[sheetname]
    df = sht.range('A1').options(pd.DataFrame, expand='table',empty = np.nan).value
    if 'Unit' in list(df.index):
        Unit = df.loc['Unit',:]    #保存单位
    elif '单位' in list(df.index):
        Unit = df.loc['单位',:]    #保存单位
    df = df.drop(df.index[:droprowsN],axis=0)   #删除第一行第二行的说明
    df.index.name = ''
    df.index = pd.to_datetime(df.index)      #转换为datetime为轴的序列
    df = df.astype('float64',copy=False, errors='raise')    #转换数据类型，统一
    if df.index.month[0] in range(1,13):
        df = df.to_period('ME')    #df.to_timestamp('M')   变回datetimeIndex
        df = df.asfreq('M',how = 'end')   #转换为月底的 periodIndex   
    #return(df,Unit)
    return(df)
def xwread(filename,sheetname,start='A1',droprowsN=10,freq = 'M', dropDC = True, interp = True):
    #freq = 'daily' 'D'
    #freq = 'quaterly'  'Q'
    #freq = 'annual      'A'
    sht = xw.Book(filename).sheets[sheetname]
    #start = 'A1'     #开始位置
    df = sht.range(start).options(pd.DataFrame, expand='table',empty = np.nan).value
    Unit = ''
    if 'Unit' in list(df.index):
        Unit = df.loc[['Unit'],:]    #保存单位
    elif '单位' in list(df.index):
        Unit = df.loc[['单位'],:]    #保存单位
    df = df.drop(df.index[:droprowsN],axis=0)   #删除第一行第二行的说明
    df.index.name = ''
    df.index = pd.to_datetime(df.index)      #转换为datetime为轴的序列, CEIC的月度数据是月初第一天，需要统一为月末的最后一天
    df = df.astype('float64',copy=False, errors='raise')    #转换数据类型，统一
    if freq == 'D':
        df = df.resample('D').last()
    elif freq == 'W':
        df = df.resample('W').last()
    elif freq == 'M':
        df = df.resample('ME').last()   ###月底最后一天
    elif freq == 'Q':
        df = df.resample('QE').last()
    elif freq == 'A':
        df = df.resample('YE').last()
    elif freq == 'fiscalyear':    ###美国财年，9月最后一天
        #df = df.shift(periods =1,freq = 'M')  ##index前移1个月时间
        #df = df.shift(periods =-1,freq = 'D')  ##index后移1天时间    变为09-30
        df = df.resample('YE-SEP').last()
    #if df.index.month[0] in range(1,13):
    #    df = df.to_period('M')    #df.to_timestamp('M')   变回datetimeIndex
    #   df = df.asfreq('M',how = 'end')   #转换为月底的 periodIndex   
    #return(df)
    Unit.index.name = None
    df = df.T.drop_duplicates().T  ##删除重复列
    df = df.drop_duplicates()  ##删除重复行
    df = df.loc[:, ~df.columns.duplicated()]  ##如果列名相同，保留第一列
    #Unit = Unit.T.drop_duplicates().T  ##删除重复列
    Unit = Unit.loc[:, ~Unit.columns.duplicated()]  ##如果列名相同，保留第一列
    if dropDC == True:
        df, df_DC = clscols(df, indicator1 = '' , indicator2 = '(DC)') ##区分原序列和DC序列
        #Unit, unit_DC = clscols(Unit, indicator1 = '' , indicator2 = '(DC)') ##区分原序列和DC序列
        df, df_DC = clscols(df, indicator1 = '' , indicator2 = '（停止更新）') ##区分原序列和DC序列
        #Unit, unit_DC = clscols(Unit, indicator1 = '' , indicator2 = '（停止更新）') ##区分原序列和DC序列
    Unit = Unit.loc[:, df.columns.to_list()]  ##与df列名一致
    if interp == True: ###插值
        df.interpolate(method='linear', axis=0, limit=None, limit_direction='forward', inplace=True)
    return(df,Unit)
#####################################################################
def xwread_daily(filename,sheetname,start='A1',droprowsN=10,freq = 'daily'):
    sht = xw.Book(filename).sheets[sheetname]
    #start = 'A1'     #开始位置
    df = sht.range(start).options(pd.DataFrame, expand='table',empty = np.nan).value
    if 'Unit' in list(df.index):
        Unit = df.loc['Unit',:]    #保存单位
    elif '单位' in list(df.index):
        Unit = df.loc['单位',:]    #保存单位
    df = df.drop(df.index[:droprowsN],axis=0)   #删除第一行第二行的说明
    df.index.name = ''
    df.index = pd.to_datetime(df.index)      #转换为datetime为轴的序列
    df = df.astype('float64',copy=False, errors='raise')    #转换数据类型，统一
    return(df)

################################################################################################
def clean_df(df,newcolname_0='no change', Old1='',Old2='',New1='',New2='',
             sortby=0,ascending = False, index_y_m='month', dropDC = False):
    #dropDC=False, 表示删除原有的DC序列
    #替换DataFrame的column names
    new_colnames = [col.replace(Old1,New1) for col in list(df.columns)]
    new_colnames = [col.replace(Old2,New2) for col in new_colnames]
    if newcolname_0 == 'no change':
        #new_colnames[0] = df.columns[0]
        df.columns = new_colnames
    elif newcolname_0 != 'no change': 
        new_colnames[0]=newcolname_0
        df.columns = new_colnames
        
    if isinstance(sortby, (int, float)):
        df_ascending = df.sort_values(by = df.index[sortby],axis =1,ascending = ascending,inplace = False,
                                kind='quicksort', na_position='last')    
    else:
        df_ascending = df        
    #if index_y_m == 'month':
    #    df = df.resample('M').asfreq()
    #
    #return df_ascending
    #df = df.sort_index(axis = 1)
    df_clean = df_ascending.dropna(axis=1, how='all')
    if dropDC == True:
        df_clean, df_DC = clscols(df_clean, indicator1 = '' , indicator2 = '(DC)') ##区分原序列和DC序列
    return(df_clean)
#############################################################################################
def sortdf_last(df,unsort_col_n,by_index=-1):   
    ###对df按照最后一行排序，其中有unsort_col_n列不参加排序，输出新的new_df,new_df_first（只含未排序
    ###的列，后面的列为nan）
    sortdf = df.iloc[:,unsort_col_n:].sort_values(axis=1, by=df.index[by_index],ascending=True, 
                                                inplace=False,kind='quicksort',
                                                na_position='last').copy(deep = True)
    new_df = pd.concat([df.iloc[:,0:unsort_col_n].copy(deep = True),sortdf],axis = 1,
                                sort = False)           #最后一个月数据排序
    new_df_first = new_df.copy();  new_df_first.iloc[:,unsort_col_n:] = np.nan
    return(new_df, new_df_first)
############################################################################################
def contrib(data, total='全国',shiftlag = 12):
    #计算各省增长对全国增长的贡献和贡献率
    data_W = data.div(data.loc[:,total],axis = 0)         #各省投资的权重（占全国投资的比重）
    data_pct= (100*(data/data.shift(shiftlag)-1)).round(1)   #各省的增长率
    data_pct_ctrs = data_pct.mul(data_W, axis = 0)                     #各省投资增长对全国增长的贡献增长率，
    data_pct_ctrs_R = data_pct_ctrs.div(data_pct_ctrs.loc[:,total],axis = 0)*100      #各省投资贡献率
    fig, ax =plt.subplots(2,1)
    data_pct_ctrs.drop(columns = [total]).iloc[-1,:].sort_values().plot.bar(title= '增长贡献',ax = ax[0])
    data_pct_ctrs_R.drop(columns = [total]).iloc[-1,:].sort_values().plot.bar(title= '贡献率',ax=ax[1])
    return(data_W, data_pct,data_pct_ctrs, data_pct_ctrs_R)
########################################################################################
def pdxl_ceic(filename,sheetname,index_col=0,skiprows=0,droprowsN=10,na_values=['NA']):
    """
    用pandas读CEIC下载的excel表格，输出 pd.DataFrame,会读出所有数据
    """
    #sheetname = '税收和政府性基金收入图'
    #filename = r"H:\D\www\macromodels\Leading\Macro_Workspace_2q(jjxdtai).xlsx"
    #index_col = 0; skiprows = 0;  droprowsN =10
    with pd.ExcelFile(filename) as xls:
        df = pd.read_excel(xls, sheetname, index_col=index_col, na_values=na_values,skiprows=skiprows)
    df = df.drop(df.index[:droprowsN],axis=0)   #删除第一行第二行的说明
    #df.index.name = ''
    df.index.name = ''
    df.index = pd.to_datetime(df.index)  #转换为datetime为轴的序列
    #new_colnames = [col.replace('CPI:','') for col in list(df.columns)]
    #new_colnames = [col.replace(':当月同比','') for col in new_colnames]
    #new_colnames[0]='CPI'
    #CPI.columns = new_colnames 
    return(df)   
#----------------------------------------------------------------------
# Setup a plot such that only the bottom spine is shown
def setup(ax):
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_minor_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    #ax.set_xlim(0, 5)
    ax.set_ylim(0, 0.1)  # set the ylim to ymin, ymax
    ax.patch.set_alpha(0.0)
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.xaxis.set_minor_locator(ticker.NullLocator())
    #ax.set_axes([0.5, 0.5, 0.001, 0.001])
def bargraph_123(ax,data_last,data_first,ylabel,title,graph_n,autotext):
    #fig,ax = plt.subplots(figsize=(12, 10))    #英寸(width, hight)
    #fig.subplots_adjust(left=0.10, right=0.95,top = 0.95,bottom=0.46)
    data = pd.concat([data_first,data_last],axis =0)
    if graph_n == 1:    #画最后一个月的bar, 只画一个序列,没有重叠
        np.transpose(data_last).plot(kind = 'bar', ax=ax);
        #ax.axhline(0, color='r',linewidth = 0.5);
        legend_labels = [str(x)+'年'+str(y)+'月' for x,y in zip(data_last.index.year,
                                                                  data_last.index.month)]
        X = np.arange(np.size(data,axis=1)); 
        Y1 = data_last.iloc[-1,:].values.tolist()
        ylim = list(ax.get_ylim())
        ylim[0] = ylim[0]-2; ylim[1] = ylim[1]+2;
        ax.set_ylim(ylim)
        if autotext == 'on':
            for x,y in zip(X,Y1):
                if np.isnan(y):
                    pass
                elif (y>=0):
                    ax.text(x, y+0.05, '%.1f' % y, ha='left', va= 'bottom',fontsize = 6)
                elif (y<0):
                    ax.text(x, y-0.5, '%.1f' % y, ha='left', va= 'top',fontsize = 6)
        elif autotext =='off':
            pass
        h, l = ax.get_legend_handles_labels()   #获取legend handles and labels
        #l = legend_labels
        [h[i].set_label(legend_labels[i]) for i,LL in enumerate(legend_labels)]
        ax.legend(loc = 'best')     #替换legend handles, labels
        #ax.legend((h[0],), ('2016年12月',))     #替换legend handles, labels
        #plt.legend((h[0],('2016年12月',))
    if graph_n == 2:    #画最后一个月的bar， 重叠,标出前 后不同颜色
        np.transpose(data).plot(kind = 'bar', ax=ax);
        legend_labels = [str(x)+'年'+str(y)+'月' for x,y in zip(data.index.year,data.index.month)]
        #ax.axhline(0, color='r');
        X = np.arange(np.size(data,axis=1));    
        Y1 = data.iloc[-1,:].values.tolist()
        ylim = list(ax.get_ylim())
        ylim[0] = ylim[0]-2; ylim[1] = ylim[1]+2;
        ax.set_ylim(ylim)
        if autotext =='on':
            for x,y in zip(X,Y1):
                if np.isnan(y):
                    pass
                elif (y>=0):
                    ax.text(x, y+0.05, '%.1f' % y, ha='left', va= 'bottom',fontsize = 6)
                elif (y<0):
                    ax.text(x, y-0.5, '%.1f' % y, ha='left', va= 'top',fontsize = 6)
        elif autotext =='off':
            pass
        np.transpose(data_first).plot(kind ='bar',color='green',ax= ax)
        h, l = ax.get_legend_handles_labels()   #获取legend handles and labels
        #l = legend_labels
        [h[i].set_label(legend_labels[i]) for i,LL in enumerate(legend_labels)]
        ax.legend(loc = 'best')     #替换legend handles, labels
    elif graph_n == 3:  #画前后两个月的bar
        np.transpose(data).plot.bar(colormap=mpl.cm.autumn,ax = ax);     
        legend_labels = [str(x)+'年'+str(y)+'月' for x,y in zip(data.index.year,data.index.month)]
        X = np.arange(np.size(data,axis=1));    
        Y1 = data.iloc[-1,:].values.tolist()
        ylim = list(ax.get_ylim())
        ylim[0] = ylim[0]-2; ylim[1] = ylim[1]+2;
        ax.set_ylim(ylim)
        if autotext =='on':
            for x,y in zip(X,Y1):
                if np.isnan(y):
                    pass
                elif (y>=0):
                    ax.text(x, y+0.05, '%.1f' % y, ha='left', va= 'bottom',fontsize = 6)
                elif (y<0):
                    ax.text(x, y-0.5, '%.1f' % y, ha='left', va= 'top',fontsize = 6)
        elif autotext =='off':
            pass      
        h, l = ax.get_legend_handles_labels()   #获取legend handles and labels
        #l = legend_labels
        [h[i].set_label(legend_labels[i]) for i,LL in enumerate(legend_labels)]
        ax.legend(loc = 'best')     #替换legend handles,
        #ax.legend((h[0],h[1],), (labels[0],labels[1],),loc = 'best')     #替换legend handles,
        #ax.axhline(0, color='r')
    #plt.ylabel(ylabel); plt.title(title,fontsize=14, fontweight='bold')
    labels = ax.get_xticklabels()
    plt.setp(labels, fontsize=8)
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_ylabel(ylabel)
    #plt.ylabel(ylabel)
    return ax

def barcross(data_last,data_first,ylabel,title,graph_n,source = '数据来源: CEIC,中国社科院财经战略研究院',figsize = (6.4,4.8),autotext = 'on'):
    if source == False:
        #fig,ax = plt.subplots(figsize=figsize)
        fig,ax = figwmarksource1(source = '')
        #fig,ax = plt.subplots(figsize=(12, 10))    #英寸
        fig.subplots_adjust(left=0.1, right=0.95,top = 0.95,bottom=0.53)
        ax= bargraph_123(ax,data_last,data_first,ylabel,title,graph_n,autotext)
        ax.set_title(title,fontsize=14, fontweight='bold')        
    else:
        """横截面柱状图"""
        fig = plt.figure(figsize = figsize)
        #用plt.subplot2grid(shape, loc, rowspan=1, colspan=1, **kwargs)定义不规则subplots
        #fig = plt.figure(figsize=(12,16))
        ax1 = plt.subplot2grid((15,18),(0,0),rowspan=1,colspan=18)
        ax2 = plt.subplot2grid((15,18),(2,0),rowspan=7,colspan=18)
        ax3 = plt.subplot2grid((15,18),(14,0),rowspan=1,colspan=18)
        #plt.setp(ax1.get_xticklabels(),visible = False)
        #plt.setp(ax1.yaxis.get_ticklabels()[0], visible = False)

        #fig, (ax1,ax2,ax3) = plt.subplots(3, 1,figsize = (12,18))
        #plt.subplots_adjust(left=0.08, right=0.98, wspace=0.3)

        # Null Locator
        setup(ax1)
        ax1.text(0.0, 0.3, title, fontsize=10, transform=ax1.transAxes)
        #ax1.set_adjustable('box')
        #ax1.set_aspect(1)

        ax2= bargraph_123(ax2,data_last,data_first,ylabel,title,graph_n,autotext)

        # Source
        #source = '数据来源: CEIC,中国社科院财经战略研究院'
        setup(ax3)
        ax3.text(0.0, -0.5, source, fontsize=10, transform=ax3.transAxes)
        plt.subplots_adjust(left=0.1, right=0.95,bottom=0.05,top = 1,hspace=0.05)
        ax = (ax1,ax2,ax3)
    #fig = plt.gcf()
    return(fig,ax)


def plotsource(data,ylabel,title,source = '数据来源: CEIC,中国社科院财经战略研究院',figsize = (6.4,4.8)):
    # source = 'on',source = 'off',
    if source == False:
        fig,ax = plt.subplots(figsize=figsize)
        #fig,ax = plt.subplots(figsize=(12, 10))    #英寸
        fig.subplots_adjust(left=0.1, right=0.95,top = 0.95,bottom=0.53)
        ax.plot(data)
        ax.set_ylabel(ylabel)
        plt.title(title,fontsize=14, fontweight='bold')        
    else:
        """线形图"""
        fig = plt.figure(figsize = figsize)
        #用plt.subplot2grid(shape, loc, rowspan=1, colspan=1, **kwargs)定义不规则subplots
        #fig = plt.figure(figsize=(12,16))
        ax1 = plt.subplot2grid((15,18),(0,0),rowspan=1,colspan=18)
        ax2 = plt.subplot2grid((15,18),(2,0),rowspan=7,colspan=18)
        ax3 = plt.subplot2grid((15,18),(14,0),rowspan=1,colspan=18)
        #plt.setp(ax1.get_xticklabels(),visible = False)
        #plt.setp(ax1.yaxis.get_ticklabels()[0], visible = False)

        #fig, (ax1,ax2,ax3) = plt.subplots(3, 1,figsize = (12,18))
        #plt.subplots_adjust(left=0.08, right=0.98, wspace=0.3)

        # Null Locator
        setup(ax1)
        ax1.text(0.0, 0.3, title, fontsize=10, transform=ax1.transAxes)
        #ax1.set_adjustable('box')
        #ax1.set_aspect(1)

        ax2.plot(data)
        ax2.set_ylabel(ylabel)

        # Source
        #source = '数据来源: CEIC,中国社科院财经战略研究院'
        setup(ax3)
        ax3.text(0.0, -0.5, source, fontsize=10, transform=ax3.transAxes)
        plt.subplots_adjust(left=0.1, right=0.95,bottom=0.05,top = 1,hspace=0.05)
        ax = (ax1,ax2,ax3)
    fig = plt.gcf()
    return(fig,ax)
##########################################################################
#def wmarksource1(watermark = '看图识字',source = "资料来源:OWID",
#                 figsize = (7,5),xy = (1/20,1/20),fontsize = 12):
def figwmarksource1(nrows = 1,ncols = 1,sharex=True,hspace = 0.1, watermark = '看图识字',
                    source = "资料来源:CEIC",logo = False, wtk = False,
                figsize = (9,6),xy = (1/20,1/20),x0y0 = (0.85,1.5/20),fontsize = 10,Grid = True):
    
    #fig1,ax1 = plt.subplots(figsize = figsize)
    
    fig1, axs = plt.subplots(nrows ,ncols, sharex=sharex,figsize = figsize)
    # Remove horizontal space between axes
    fig1.subplots_adjust(hspace=hspace)
    
    if logo :
        # reading the image
        image = plt.imread(r"E:\E\python_w\国家金融发展实验室模板\实验室logo.png")
        # OffsetBox
        image_box = OffsetImage(image, zoom=0.05)    ####图片盒,缩小，
        #插入figure图片盒位置x0y0
        ab = AnnotationBbox(image_box, x0y0, alpha = 0.2,zorder = 1,frameon=False,xycoords='figure fraction')  ####把图片盒放在(x0,y0)位置，注释
        fig1.add_artist(ab)   
        #ax1.add_artist(ab)   

    ###添加水印
    if wtk :
        fig1.text(0.5, 0.5, watermark, 
                fontsize=40, color='gray', alpha=0.2,
                ha='center', va='center', rotation=30)
    ##添加数据来源
    fig1.subplots_adjust(left = 0.12,bottom=0.2,right = 0.9,top=0.9,hspace=hspace)
    fig1.text(xy[0],xy[1], source, 
            fontsize=fontsize, 
            #color = 'blue',
            ha='left', va='center')
    #ax1.yaxis.grid(Grid)
    return(fig1,axs)

def figwmarksource2(fig1,watermark = '看图识字',source = "资料来源:OWID",logo = False,
                    wtk = False,xy = (1/20,1/20),x0y0 = (0.85,1.5/20),fontsize = 10,Grid = True):
    #fig1,ax1 = plt.subplots(figsize = figsize)
    if logo :
        # reading the image
        image = plt.imread(r"E:\E\python_w\国家金融发展实验室模板\实验室logo.png")
        # OffsetBox
        image_box = OffsetImage(image, zoom=0.05)    ####图片盒,缩小，
        #插入figure图片盒位置x0y0
        ab = AnnotationBbox(image_box, x0y0, alpha = 0.2,zorder = 1,
                            frameon=False,xycoords='figure fraction')  ####把图片盒放在(x0,y0)位置，注释
        fig1.add_artist(ab)   
        #ax1.add_artist(ab)   
    elif logo =='off':
        pass      #python 3.0以上，pass可以写或者不写
    
    ###添加水印
    if wtk:
        fig1.text(0.5, 0.5, watermark, 
        fontsize=50, color='gray', alpha=0.2,
        ha='center', va='center', rotation=30)
    ##添加数据来源
    fig1.subplots_adjust(left = 0.12,bottom=0.2,right = 0.9,top=0.9,hspace=0.15)
    fig1.text(xy[0],xy[1], source, 
            fontsize=fontsize, 
            ha='left', va='center')
    #ax1.grid(Grid)
    return(fig1)
#######################################################################

#def wmarksource1(watermark = '看图识字',source = "资料来源:OWID",
#                 figsize = (7,5),xy = (1/20,1/20),fontsize = 12):
def wmarksource1(watermark = '看图识字',source = "资料来源:OWID",logo = False,wtk=False,
                figsize = (9,6),xy = (1/20,1/20),x0y0 = (0.85,1.5/20),fontsize = 10,Grid = True):
    
    fig1,ax1 = plt.subplots(figsize = figsize)
    ###添加水印
    if wtk:
        ax1.text(0.5, 0.5, watermark, transform=ax1.transAxes,
                fontsize=40, color='gray', alpha=0.3,
                ha='center', va='center', rotation=30)
    if logo:
        # reading the image
        image = plt.imread(r"E:\E\python_w\国家金融发展实验室模板\实验室logo.png")
        # OffsetBox
        image_box = OffsetImage(image, zoom=0.05)    ####图片盒,缩小，
        #插入figure图片盒位置x0y0
        ab = AnnotationBbox(image_box, x0y0, alpha = 0.2,zorder = 1,frameon=False,xycoords='figure fraction')  ####把图片盒放在(x0,y0)位置，注释
        fig1.add_artist(ab)   
        #ax1.add_artist(ab)   
        
    ##添加数据来源
    fig1.subplots_adjust(left = 0.12,bottom=0.2,right = 0.9,top=0.9,hspace=0.05)
    #fig1.text(xy[0],xy[1], source, fontsize=fontsize, color='blue', ha='left', va='center')
    ax1.annotate(source, xy = xy,
                        xycoords='figure fraction', va="center", ha="left",fontsize=fontsize,
                        textcoords=None, arrowprops=None, annotation_clip=None)
    ax1.grid(Grid)
    return(fig1,ax1)

def wmarksource2(fig1,ax1,watermark = '看图识字',source = "资料来源:OWID",logo=False,wtk=False,
                 figsize = (9,6),xy = (1/20,1/20),x0y0 = (0.85,1.5/20),fontsize = 10,Grid = True):
    #fig1,ax1 = plt.subplots(figsize = figsize)
    if logo :
        # reading the image
        image = plt.imread(r"E:\E\python_w\国家金融发展实验室模板\实验室logo.png")
        # OffsetBox
        image_box = OffsetImage(image, zoom=0.05)    ####图片盒,缩小，
        #插入figure图片盒位置x0y0
        ab = AnnotationBbox(image_box, x0y0, alpha = 0.2,zorder = 1,frameon=False,xycoords='figure fraction')  ####把图片盒放在(x0,y0)位置，注释
        fig1.add_artist(ab)   
        #ax1.add_artist(ab)   
    ###添加水印
    if wtk :
        ax1.text(0.5, 0.5, watermark, transform=ax1.transAxes,
                fontsize=40, color='gray', alpha=0.2,
                ha='center', va='center', rotation=30)
    ##添加数据来源
    fig1.subplots_adjust(left = 0.12,bottom=0.2,right = 0.9,top=0.9,hspace=0.15)
    #fig1.text(xy[0],xy[1], source, fontsize=fontsize, color='blue', ha='left', va='center')    
    ax1.annotate(source, xy = xy,
                        xycoords='figure fraction', va="center", ha="left",fontsize=fontsize,
                        textcoords=None, arrowprops=None, annotation_clip=None)
    ax1.grid(Grid)
    return(fig1,ax1)
######画一条线
def line1(series,title1,outputpath,saven,enddate = 'True'):
    ##########线图########
    fig1,ax1 = figwmarksource1(source="资料来源:国家统计局，国家金融与发展实验室")
    line_endpoint(fig1, ax1,series.dropna())
    ax1.set_ylabel('百分比')
    ax1.set_title(title1)
    if enddate == 'True':
        yshift = (ax1.get_ylim()[1]-ax1.get_ylim()[0])/40
        ax1.text(series.index[-1],ax1.get_ylim()[0]-yshift,
                 str(series.index[-1]),va = 'top',ha = 'left')
    fig1.savefig(outputpath + r'\\'+ saven + '.svg', transparent = True,  bbox_inches='tight')
    fig1.savefig(outputpath +  r'\\'+ saven + '.pdf', transparent = True,  bbox_inches='tight')
#######################################################################
def lineannotate(fig1,ax1,plotdata,anodata=-1, roundn = 1,arrow = 'yes',
                 Grid = True,yshrink = 0.5,xshift = 0,enddate = True):
    ####对已经画线的图注释标记，箭头，anodata 是最后一个数，position是标记位于y轴的比例,xshift 是注释位置x轴偏移量,yshrink是缩减的比例，应该《0.5
    ####只标注最后日期有数据的线
    ####对plotdata最后日期的数据排序，lines按照这一顺序排序
    #计算y轴间距
    lines = ax1.get_lines()   #线 -1
    #colors = {line.get_label():line.get_color() for line in lines } #线颜色
    ylimlength = ax1.get_ylim()[1] - ax1.get_ylim()[0] #y轴长度
    xshift = (ax1.get_xlim()[1]-ax1.get_xlim()[0])/80
    #realdata = plotdata.iloc[-3:,:].dropna(axis = 1,how='all')
    if len(lines)>=2:
        endn = np.shape(plotdata.iloc[-3:,:].dropna(axis = 1,how='all'))[1]   ##最后3个日期的有效数据量,shape的列数
        ###先挑选出需要标注的线
        annolines = []
        for line0 in lines:
            if line0.get_label() in plotdata.iloc[-3:,:].dropna(axis = 1,how='all').columns:
                annolines.append(line0)
        if endn >=2:
            ##最后日期数据量大于零，才画线标注    
            ytextposition = np.linspace((ax1.get_ylim()[1] + ax1.get_ylim()[0])/2+ylimlength*yshrink*(1-1/endn),
                                        (ax1.get_ylim()[1] + ax1.get_ylim()[0])/2-ylimlength*yshrink*(1-1/endn),
                                        endn)  ###y轴从上到下排序
            if arrow == 'yes':
                for ii,datline in enumerate(annolines):
                    if not np.isnan(datline.get_data(0)[1][anodata]) :
                        ax1.annotate('  ' + str(round(datline.get_data(0)[1][anodata],roundn)), horizontalalignment='left',verticalalignment='center',
                                    xy=(datline.get_data(0)[0][anodata], datline.get_data(0)[1][anodata]), xycoords='data',transform=ax1.transAxes,
                                    xytext=(ax1.get_xlim()[-1]+xshift, ytextposition[ii]), textcoords='data',color = datline.get_color(),
                                    fontweight='extra bold', 
                                    #bbox=dict(boxstyle="round", fc="0.8"),
                                    #arrowprops=dict(arrowstyle="-",
                                    #                connectionstyle="arc,angleA = 180, armA = 0, rad =0",
                                    #                color = datline.get_color(),linewidth = 0.5),                
                                    arrowprops=dict(arrowstyle="-",
                                                    connectionstyle="arc3",color = datline.get_color(),linewidth = 0.5),
                                    #arrowprops=dict(arrowstyle="-",
                                    #                connectionstyle="arc,angleA=180,armA=0.5,angleB=88,armB=0,rad=0",color = datline.get_color(),linewidth = 0.5),
                                    )
                    elif not np.isnan(datline.get_data(0)[1][anodata-1]) :
                        ax1.annotate('  ' + str(round(datline.get_data(0)[1][anodata-1],roundn)), horizontalalignment='left',verticalalignment='center',
                                    xy=(datline.get_data(0)[0][anodata-1], datline.get_data(0)[1][anodata-1]), xycoords='data',transform=ax1.transAxes,
                                    xytext=(ax1.get_xlim()[-1]+xshift, ytextposition[ii]), textcoords='data',color = datline.get_color(),
                                    fontweight='extra bold', 
                                    #bbox=dict(boxstyle="round", fc="0.8"),
                                    #arrowprops=dict(arrowstyle="-",
                                    #                connectionstyle="arc,angleA = 180, armA = 0, rad =0",
                                    #                color = datline.get_color(),linewidth = 0.5),                
                                    arrowprops=dict(arrowstyle="-",
                                                    connectionstyle="arc3",color = datline.get_color(),linewidth = 0.5),
                                    #arrowprops=dict(arrowstyle="-",
                                    #                connectionstyle="arc,angleA=180,armA=0.5,angleB=88,armB=0,rad=0",color = datline.get_color(),linewidth = 0.5),
                                    )   
                    elif not np.isnan(datline.get_data(0)[1][anodata-2]) :
                        ax1.annotate('  ' + str(round(datline.get_data(0)[1][anodata-2],roundn)), horizontalalignment='left',verticalalignment='center',
                                    xy=(datline.get_data(0)[0][anodata-2], datline.get_data(0)[1][anodata-2]), xycoords='data',transform=ax1.transAxes,
                                    xytext=(ax1.get_xlim()[-1]+xshift, ytextposition[ii]), textcoords='data',color = datline.get_color(),
                                    fontweight='extra bold', 
                                    #bbox=dict(boxstyle="round", fc="0.8"),
                                    #arrowprops=dict(arrowstyle="-",
                                    #                connectionstyle="arc,angleA = 180, armA = 0, rad =0",
                                    #                color = datline.get_color(),linewidth = 0.5),                
                                    arrowprops=dict(arrowstyle="-",
                                                    connectionstyle="arc3",color = datline.get_color(),linewidth = 0.5),
                                    #arrowprops=dict(arrowstyle="-",
                                    #                connectionstyle="arc,angleA=180,armA=0.5,angleB=88,armB=0,rad=0",color = datline.get_color(),linewidth = 0.5),
                                    )   
                    
    
            elif arrow == 'no':
                for ii,datline in enumerate(annolines):
                    if not np.isnan(datline.get_data(0)[1][anodata]) :
                        ax1.annotate('  ' + str(round(datline.get_data(0)[1][anodata],roundn)), horizontalalignment='left',verticalalignment='center',
                                    xy=(datline.get_data(0)[0][anodata], datline.get_data(0)[1][anodata]), xycoords='data',transform=ax1.transAxes,
                                    xytext=(ax1.get_xlim()[-1]+xshift, ytextposition[ii]), textcoords='data',color = datline.get_color(),
                                    fontweight='extra bold', 
                                    #bbox=dict(boxstyle="round", fc="0.8"),
                                    )
                    elif not np.isnan(datline.get_data(0)[1][anodata-1]) :
                        ax1.annotate('  ' + str(round(datline.get_data(0)[1][anodata-1],roundn)), horizontalalignment='left',verticalalignment='center',
                                    xy=(datline.get_data(0)[0][anodata-1], datline.get_data(0)[1][anodata-1]), xycoords='data',transform=ax1.transAxes,
                                    xytext=(ax1.get_xlim()[-1]+xshift, ytextposition[ii]), textcoords='data',color = datline.get_color(),
                                    fontweight='extra bold', 
                                    #bbox=dict(boxstyle="round", fc="0.8"),
                                    )
                    elif not np.isnan(datline.get_data(0)[1][anodata-2]) :
                        ax1.annotate('  ' + str(round(datline.get_data(0)[1][anodata-2],roundn)), horizontalalignment='left',verticalalignment='center',
                                    xy=(datline.get_data(0)[0][anodata-2], datline.get_data(0)[1][anodata-2]), xycoords='data',transform=ax1.transAxes,
                                    xytext=(ax1.get_xlim()[-1]+xshift, ytextposition[ii]), textcoords='data',color = datline.get_color(),
                                    fontweight='extra bold', 
                                    #bbox=dict(boxstyle="round", fc="0.8"),
                                    )
                   
                        
    elif len(lines) ==1:
        datline = lines[0]
        if not np.isnan(datline.get_data(0)[1][anodata]) :
            ax1.annotate(str(round(datline.get_data(0)[1][anodata],roundn)), horizontalalignment='left',verticalalignment='center',
                        xy=(datline.get_data(0)[0][anodata], datline.get_data(0)[1][anodata]), xycoords='data',transform=ax1.transAxes,
                        xytext=(datline.get_data(0)[0][anodata]+xshift, datline.get_data(0)[1][anodata]), textcoords='data',
                        color = datline.get_color(),
                        fontweight='extra bold', 
                        #bbox=dict(boxstyle="round", fc="0.9"),
                        bbox=dict(boxstyle=custom_box_style, alpha=0.2),
                        )
        elif not np.isnan(datline.get_data(0)[1][anodata-1]) :
            ax1.annotate(str(round(datline.get_data(0)[1][anodata-1],roundn)), horizontalalignment='left',verticalalignment='center',
                        xy=(datline.get_data(0)[0][anodata-1], datline.get_data(0)[1][anodata-1]), xycoords='data',transform=ax1.transAxes,
                        xytext=(datline.get_data(0)[0][anodata-1]+xshift, datline.get_data(0)[1][anodata-1]), textcoords='data',
                        color = datline.get_color(),
                        fontweight='extra bold', 
                        #bbox=dict(boxstyle="round", fc="0.9"),
                        bbox=dict(boxstyle=custom_box_style, alpha=0.2),
                        )
        elif not np.isnan(datline.get_data(0)[1][anodata-2]) :
            ax1.annotate(str(round(datline.get_data(0)[1][anodata-2],roundn)), horizontalalignment='left',verticalalignment='center',
                        xy=(datline.get_data(0)[0][anodata-2], datline.get_data(0)[1][anodata-2]), xycoords='data',transform=ax1.transAxes,
                        xytext=(datline.get_data(0)[0][anodata-2]+xshift, datline.get_data(0)[1][anodata-2]), textcoords='data',
                        color = datline.get_color(),
                        fontweight='extra bold', 
                        #bbox=dict(boxstyle="round", fc="0.9"),
                        bbox=dict(boxstyle=custom_box_style, alpha=0.2),
                        )
                
        #ax1.yaxis.grid(Grid)
    if enddate :
        yshift = (ax1.get_ylim()[1]-ax1.get_ylim()[0])/40
        #ax1.text(plotdata.index[-1],ax1.get_ylim()[0]-yshift,
        #             str(plotdata.index[-1]),va = 'top',ha = 'left')
        ax1.text(ax1.get_xlim()[-1]+xshift,ax1.get_ylim()[0]-yshift,
                    str(plotdata.index[-1]),va = 'top',ha = 'left')        
    return(fig1,ax1)
    
def lineanno3(fig1,ax1,plotdata,anodata=-1,roundn = 1,arrow = 'yes',
                 Grid = True,xshift = 0,enddate = True):
    ####对线图进行简单注释标记，用于最后日期数据均匀分散时，箭头，anodata 是最后一个数，position是标记位于y轴的比例,xshift 是注释位置x轴偏移量,yshrink是缩减的比例，应该《0.5
    ####只标注最后日期有数据的线，x轴添加最后日期
    lines = ax1.get_lines()   #线 -1
    xshift = (ax1.get_xlim()[1]-ax1.get_xlim()[0])/80
    #colors = {line.get_label():line.get_color() for line in lines } #线颜色
    for datline in lines:
        ax1.annotate(str(round(datline.get_data(0)[1][anodata],roundn)), horizontalalignment='left',verticalalignment='center',
                    xy=(datline.get_data(0)[0][anodata], datline.get_data(0)[1][anodata]), xycoords='data',transform=ax1.transAxes,
                    xytext=(ax1.get_xlim()[-1]+xshift, datline.get_data(0)[1][anodata]), textcoords='data',color = 'w',
                    bbox=dict(boxstyle=custom_box_style, alpha=0.5,facecolor = datline.get_color()),
                    fontweight='extra bold', 
                    #arrowprops=dict(arrowstyle="-",
                    #                connectionstyle="arc,angleA = 180, armA = 0, rad =0",
                    #                color = datline.get_color(),linewidth = 0.5),                
                    #arrowprops=dict(arrowstyle="-",
                    #                connectionstyle="arc3",color = datline.get_color(),linewidth = 0.5),
                    #arrowprops=dict(arrowstyle="-",
                    #                connectionstyle="arc,angleA=180,armA=0.5,angleB=88,armB=0,rad=0",color = datline.get_color(),linewidth = 0.5),
                    )
        #ax1.yaxis.grid(Grid)
    if enddate :
        yshift = (ax1.get_ylim()[1]-ax1.get_ylim()[0])/40
        ax1.text(plotdata.index[-1],ax1.get_ylim()[0]-yshift,  
                     str(plotdata.index[-1]),va = 'top',ha = 'left', fontweight='extra bold',)
    return(fig1,ax1)

def custom_box_style(x0, y0, width, height, mutation_size):
    """
    Given the location and size of the box, return the path of the box around
    it.

    Rotation is automatically taken care of.

    Parameters
    ----------
    x0, y0, width, height : float
        Box location and size.
    mutation_size : float
        Mutation reference scale, typically the text font size.
    """
    # padding
    mypad = 0.3
    pad = mutation_size * mypad
    # width and height with padding added.
    width = width + 2 * pad
    height = height + 2 * pad
    # boundary of the padded box
    x0, y0 = x0 - pad, y0 - pad
    x1, y1 = x0 + width, y0 + height
    # return the new path
    return Path([(x0, y0),
                 (x1, y0), (x1, y1), (x0, y1),
                 (x0-pad, (y0+y1)/2), (x0, y0),
                  (x0, y0)],
                closed=True)

    '''
    return Path([(x0, y0),
                 (x0+pad, y0+height/2), (x1, y0+height/2), (x1, y1-height/2),
                 (x0+pad, y1-height/2), (x0, y0),
                 ],
                 closed=True)
    '''

#用上面的函数，可以画出
#fig, ax = plt.subplots(figsize=(3, 3))
#ax.text(0.5, 0.5, "Test", size=30, va="center", ha="center", rotation=30,
#        bbox=dict(boxstyle=custom_box_style, alpha=0.2))
def line_endpoint(fig1,ax1,series,linewidth = 3,linestyles='-',marker = 'o',linecolor = 'b',
                  pointcolor = 'r',xshift = 5,endpoint_legend = False,endpoint_format = '%.1f',
                  endpoint_xticklabel = True):
    #xshift 是标注点向右偏移量。 
    #fig1,ax1 = plt.subplots()
    #series = R_spread.loc['1980':]
    #ax1=axs[0]
    if series.ndim==2:
        series = series.squeeze()        #把单列的df 转变为series
    series.plot(ax = ax1,linewidth = linewidth,linestyle = linestyles, alpha = 0.9,color = linecolor)
    ax1.set_xlim(series.index[0],series.index[-1])   #x轴紧密连接曲线
    series_end = series.copy()
    series_end.iloc[:-1] = np.nan    ##只保留最后一个数，标记这个数
    #series_end.plot(ax= ax1,marker = marker,color = color)
    xshift = (ax1.get_xlim()[1]-ax1.get_xlim()[0])/80
    ax1.scatter(series_end.index,series_end.values, marker = marker,color = pointcolor,zorder = 1) 
    ax1.text(ax1.get_lines()[0].get_data(0)[0][-1]+xshift,series_end.iloc[-1],endpoint_format % series_end.iloc[-1],
                ha = 'left',va = 'center',fontsize=10,rotation = 0, color = 'w',
                fontweight='extra bold', 
                bbox=dict(boxstyle=custom_box_style, alpha=0.5,ec ='k',fc = 'k'))    
    #ax1.text(ax1.get_lines()[0].get_data(0)[0][-1]+xshift,series_end.iloc[-1],'%.2f' % series_end.iloc[-1],
    #         ha = 'left',va = 'center',fontsize=10,rotation = 0, color = ax1.get_lines()[0].get_color(),
    #         bbox=dict(boxstyle=custom_box_style, alpha=0.2,ec ='k',fc = 'k'))
    #ax1.text(ax1.get_lines()[0].get_data(0)[0][-1]+200,series_end.iloc[-1],'%.2f' % series_end.iloc[-1],
    #         ha = 'center',va = 'center',fontsize=12,rotation = 0,
    #         bbox=dict(boxstyle=custom_box_style(ax1.get_lines()[0].get_data(0)[0][-1]+200,series_end.iloc[-1],
    #                                             30, 20, 12), alpha=0.2))
    if endpoint_legend:
        #ax1.legend([series.name, str(series.index[-1].to_period('M'))],framealpha = 0.2)
        ax1.legend([series.name, str(series.index[-1])],framealpha = 0.2)    
    if endpoint_xticklabel:
        yshift = (ax1.get_ylim()[1]-ax1.get_ylim()[0])/40
        ax1.text(ax1.get_xlim()[1],ax1.get_ylim()[0]-yshift,
                  str(series.index[-1].to_period('M')),va = 'top',ha = 'left', fontweight='extra bold', )
        #ax1.text(ax1.get_xlim()[1],ax1.get_xticklabels()[-1].get_position()[1],
        #             str(series.index[-1].to_period('M')),va = 'top',ha = 'left')

    #for spine in ['left','right','top']:
    #    ax1.spines[spine].set_visible(False)    
    return(fig1,ax1)
def m_line_endpoint(plotdata,title,outputpath,savepic = True,yshift=0,xshift =0,
                    source = '资料来源：OWID',Grid = False,datelocator  = False,enddate = True):
    ####yshift，最后日期标注，沿y轴下移
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    
    plotdata = plotdata.dropna(axis = 0) ###行nan 整行消除
    fig,axs = figwmarksource1(nrows=len(plotdata.columns), hspace=0, source = source,wtk=True)
    for ii, colname in enumerate(plotdata.columns):
        line_endpoint(fig, axs[ii], plotdata.iloc[:,ii],xshift = xshift,linecolor = colors[ii],
                      endpoint_xticklabel = False)
        #axs[ii].legend([colname,str(plotdata[colname].index[-1])])
        axs[ii].legend([colname,])
        axs[ii].grid(Grid)
    if datelocator:
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)  ##自动刻度
        formatter = mdates.ConciseDateFormatter(locator)
        axs[ii].xaxis.set_major_locator(locator)
        axs[ii].xaxis.set_major_formatter(formatter)
    #axs[ii].get_xaxis().set_major_locator(mdates.MonthLocator(interval=2))
    #axs[ii].get_xaxis().set_minor_locator(mdates.MonthLocator(interval=1))
    #axs[ii].get_xaxis().set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.suptitle(title)
    if enddate:
        yshift = (axs[ii].get_ylim()[1]-axs[ii].get_ylim()[0])/10
        axs[ii].text(axs[ii].get_xlim()[1],axs[ii].get_ylim()[0]-yshift,
                     str(plotdata.iloc[:,ii-1].index[-1]),va = 'top', fontweight='extra bold', )
        #axs[ii].text(axs[ii].get_xlim()[1],axs[ii].get_xticklabels()[-1].get_position()[1],
        #             str(plotdata.iloc[:,ii-1].index[-1]),va = 'top')
    if savepic:
        fig.savefig(outputpath + r'\\' + title +'.svg', transparent = True,  bbox_inches='tight')
        fig.savefig(outputpath + r'\\'+ title +'.pdf', transparent = True,  bbox_inches='tight')
    return(fig,axs)
##############################################
def plotenddate(plotdata, titlestr,saven,outputpath,ylabel = '百分比',source = '资料来源：CEIC'):
    ###画线，表示最后日期value,在x轴添加最后日期
    fig1,ax1 = figwmarksource1(source=source)
    plotdata.plot(ax = ax1,color = ['b','r','g','orange'])
    plt.ylabel(ylabel)
    plt.title(titlestr)
    fig1,ax1 = lineannotate(fig1, ax1, plotdata,roundn = 1,arrow= 'yes')
    yshift = (ax1.get_ylim()[1]-ax1.get_ylim()[0])/40
    #ax1.text(plotdata.index[-1],ax1.get_ylim()[0]-yshift,
    #             str(plotdata.index[-1]),va = 'top',ha = 'left', fontweight='extra bold', )
    plt.savefig(outputpath + r'\\' + saven+ '.svg', transparent = True,  bbox_inches='tight')     #不能用bbox_inches = 'tight'，保存不了
    plt.savefig(outputpath + r'\\' + saven+ '.pdf', transparent = True,  bbox_inches='tight')     #不能用bbox_inches = 'tight'，保存不了
    return(fig1,ax1)
#########################################################################################
def panelline(yX,sample,outputpath, x = '每月新增确诊病例（自然对数）',
              y = '每月地方财政收入增速',location = '省市',
              title = '2022年1-6月各省市新冠确诊病例与地方财政收入增速比较',source = '资料来源：CEIC,WIND'):
    ################################################################################################
    ###选择画线的数据时间
    #start= '2022-03'; end = '2022-06'
    #sample = ['2022-03','2022-04','2022-05','2022-06','2022-07']
    yX_l = yX.loc[sample,:].reset_index()  ###取消时间为index
    
    fig = sns.lmplot(x=x, 
                     y=y, data=yX_l, hue = '时间',
                     height=6, aspect=1.5)
        
    ax = fig.axes[0][0]
    #####标示各点省份
    for i in np.arange(0,len(yX_l)):
        ax.text(yX_l.iloc[i].loc[x],
                yX_l.iloc[i].loc[y],
                yX_l.iloc[i].loc[location],
                horizontalalignment='left', fontweight='extra bold', )
    ax.get_legend().set_visible(False)
    #ax.legend([yX_l5.loc[:,'月份'].iloc[0]+'累计'+'各省市数据','拟合直线',
    #           yX_l5.loc[:,'月份'].iloc[-1]+'累计'+'各省市数据','拟合直线'])
    #ax.set_xlabel('年初至当月累计新增确诊病例（自然对数）')
    #ax.set_ylabel('年初至当月累计地方财政收入增速')
    
    plt.title(title)
    #plt.subplots_adjust(top = 0.9, bottom=0.1)
    wmarksource2(fig.figure, ax,source = source)
    plt.savefig(outputpath + r'\\' +title+'.svg', transparent = True,  bbox_inches='tight')
    ###########################################
    plt.savefig(outputpath + r'\\' +title+'.pdf', transparent = True,  bbox_inches='tight')
#######################################################################################
def duallines(df1,unit_,df2,ylabel2,legend1, legend2,suptitlestr, outputpath,ylabel1 = 'various', closefig = True):
    ###ylabel1 = 'various'， 表示取不同单位， 如果ylabel1 = '亿美元' 等等，表示取相同单位
    savenames = []  #保存的图片文件名称list
    totalcol = np.shape(df1)[1]
    for i,item in enumerate(df1.columns):
        ##sharex = True,的图，上下的线长度需一致
        df1temp = df1.loc[:,item].dropna(); df2temp = df2.loc[:,item].dropna()
        start = min(df1temp.index[0],df2temp.index[0])
        end = max(df1temp.index[-1],df2temp.index[-1])
        df1plot_i = df1.loc[start:end,item]  ;  df2plot_i = df2.loc[start:end,item] 
        fig1,axs = figwmarksource1(nrows=2, source='资料来源：CEIC',hspace=0.15, figsize=(9,6))
        df1plot_i.plot(alpha = 0.8,ax = axs[0])    ###'1982-1984=100'
        lineannotate(fig1, axs[0], df1plot_i.to_period('M'),enddate = False)
        #axs[0].legend('',loc = 'upper left',framealpha = 0)  ###完全透明，看不见
        axs[0].legend(legend1,loc = 'best')
        #axs[0].get_legend().set_visible(False)
        #suptitlestr = suptitlestr + item
        #axs[0].set_title(suptitlestr + item,fontsize = 12)
        if ylabel1 == 'various':
            ylabel = unit_.iloc[0,i]
        elif ylabel1 != 'various':
            ylabel = ylabel1
        axs[0].set_ylabel(ylabel)
        #fig.set_figwidth(8, forward=True)
        axs[0].set_xlabel('')
        df2plot_i.plot(alpha = 0.8,ax = axs[1])
        lineannotate(fig1, axs[1], df2plot_i.to_period('M'))
        #axs[1].legend([],labelcolor='linecolor',framealpha = 0)
        axs[1].legend(legend2,loc = 'best')
        fig1.suptitle(suptitlestr + item + '（%d - %s)' %(totalcol,i+1))
        axs[1].set_ylabel(ylabel2)
        fig1.subplots_adjust(top = 0.95)
        savename = item.replace(':','_')+ suptitlestr 
        savename = savename.replace('%','百分比')
        savename = savename.replace('_','')
        savename = savename.replace('<','小于')
        savename = savename.replace('>','大于')
        fig1.savefig(outputpath + str(r'\\') +suptitlestr + savename +'.svg', transparent = True,  bbox_inches='tight')
        fig1.savefig(outputpath + str(r'\\') +suptitlestr + savename +'.pdf', transparent = True,  bbox_inches='tight')
        savenames.append(savename +'.pdf')
        if closefig:
            plt.close('all')
    return(savenames)    
#########################################################
def fig1_lines(snsdata, title, ylabel, savename, outputpath, freq = 'D', new_legend = False,
               watermark='SALMON', wtk=False, alpha=0.85, dropna=False, 
               lgncols = 1, lgloc = 'best', desp = False,sort = -1, ylinetick =0, snstype = False,
               anno = True,enddate = True, roundn = 1, grid = False, NBERdate = True,linewidth=3, 
               left = 0.12,bottom=0.2,right = 0.9,top=0.9, colormap = None, 
               figsize=(9, 6), source = '数据来源：CEIC', png = False, pdf = True):
    ##snstype = True, anno = False
    #print(plt.colormaps())  # 列出所有可用colormap
    ###首先将
    #title = u'各月一般公共预算收入累计同比'
    #savename = r'\各月一般公共预算收入中央地方累计同比.svg'
    #ylabel = '百分比'
    #legend_labels =  ['一般公共预算收入累计','一般公共预算收入累计:中央本级','一般公共预算收入累计:地方本级']
    fig1, ax1 = figwmarksource1(figsize = figsize, source = source, watermark=watermark, wtk=wtk)
    snsdata = snsdata.sort_values(by =snsdata.index[sort], axis = 1, ascending = False)
    ax1.set_title(label=title, fontsize = 16, fontweight='bold')
    ax1.set_ylabel(ylabel, fontsize = 14)    
    if snsdata.index.freq == None:
        datafreq = freq
    else:
        datafreq=snsdata.index.freq
    if dropna == True:
        snsdata = snsdata.dropna(axis = 0)
    if snstype == True:
        sns.lineplot(ax = ax1, data=snsdata, palette="tab10", linewidth=3)
        anno = False           ###snstype 图线 不能用arrow 标注最后日期的数值
    if desp == True:  #取消坐标轴
        despine(ax = ax1)

    if snstype == False and snsdata.shape[1] > 1:
        #snsdata.to_period(datafreq).plot(ax = ax1, linewidth =linewidth,  alpha=alpha)
        snsdata.plot(ax = ax1, linewidth =linewidth,  alpha=alpha, colormap = colormap)
        ax1.legend(ncols = lgncols, loc = lgloc)
        #legend_labels=snsdata.columns
        #handles, labels = ax1.get_legend_handles_labels()
        #ax1.legend(handles, legend_labels, ncols = lgncols)    
        
        if isinstance(ylinetick, (int, float)):
            ax1.axhline(ylinetick, color='gray',linestyle = '--', linewidth = 1)
        if anno == True:
            lineannotate(fig1, ax1, snsdata.to_period(datafreq), enddate = enddate, roundn = roundn)
    if new_legend == True:
        legend_labels=snsdata.columns
        handles, labels = ax1.get_legend_handles_labels()
        ax1.legend(handles, legend_labels)
    if snstype == False and snsdata.shape[1] == 1:
        line_endpoint(fig1, ax1, snsdata)
        if isinstance(ylinetick, (int, float)):
            ax1.axhline(ylinetick, color='gray',linestyle = '--', linewidth = 1)
        ax1.legend().remove()
        if grid:
            ax1.grid(grid, axis ='y', linestyle=':', alpha=0.6) 
    if NBERdate == True:
        NBERdate_plot(snsdata, ax= ax1)
    fig1.subplots_adjust(left = left,bottom = bottom,right = right,top = top)
    if png == True:
        fig1.savefig(outputpath + savename+'.png', transparent = False,  bbox_inches='tight')
    if pdf == True:
            fig1.savefig(outputpath + savename+'.pdf', transparent = True,  bbox_inches='tight')           
    fig1.savefig(outputpath + savename, transparent = True,  bbox_inches='tight')
    
    return(fig1, ax1)
#########################################################
def fig2_lines(snsdata0,snsdata1, ylabel0,ylabel1, savename, outputpath,
               title0='',title1='',suptitle = '', freq0 ='M', freq1 ='M',nrows = 2,
               sharex = True, new_legend = False, watermark='SALMON', wtk=False, 
               linewidth = 3, lgncols = 1,lgloc0 ='best', lgloc1 ='best',alpha=0.85, 
               desp = False,sort = -1, ylinetick0 =0,ylinetick1 =0, snstype = False,
               anno = True, enddate = True, roundn = 1, grid = False, NBERdate = True,
               figsize=(9, 6),left = 0.12,bottom=0.2,right = 0.9,top=0.9,
               hspace=0.1, colormap=(None, None), 
               source = '数据来源：CEIC', png = False, pdf = True):
    #####画上下两图
    fig1, ax1 = figwmarksource1(nrows = nrows,sharex=sharex, hspace = hspace,
                                figsize = figsize,
                                source = source, watermark=watermark, wtk=wtk)
    snsdata0 = snsdata0.sort_values(by =snsdata0.index[sort], axis = 1, ascending = False)
    snsdata1 = snsdata1.sort_values(by =snsdata1.index[sort], axis = 1, ascending = False)
    if snsdata0.index.freq == None:
        datafreq0 = freq0
    else:
        datafreq0=snsdata0.index.freq
    if snsdata1.index.freq == None:
        datafreq1 = freq1
    else:
        datafreq1=snsdata1.index.freq
    if snstype == True:
        sns.lineplot(ax = ax1[0], data=snsdata0, palette="tab10", linewidth=3)
        sns.lineplot(ax = ax1[1], data=snsdata1, palette="tab10", linewidth=3)
        anno = False           ###snstype 图线 不能用arrow 标注最后日期的数值

    if snstype == False and snsdata0.shape[1] > 1:
        #snsdata.to_period(datafreq).plot(ax = ax1, linewidth =linewidth,  alpha=alpha)
        snsdata0.plot(ax = ax1[0], linewidth =linewidth,  alpha=alpha,colormap = colormap[0])
        ax1[0].legend(ncols = lgncols,loc=lgloc0)
        if isinstance(ylinetick0, (int, float)):
            ax1[0].axhline(ylinetick0, color='gray',linestyle = '--', linewidth = 1)
        if anno == True:
            lineannotate(fig1, ax1[0], snsdata0.to_period(datafreq0), enddate = enddate, roundn = roundn)
 
    if snstype == False and snsdata1.shape[1] > 1:
        #snsdata.to_period(datafreq).plot(ax = ax1, linewidth =linewidth,  alpha=alpha)
        snsdata1.plot(ax = ax1[1], linewidth =linewidth,  alpha=alpha, colormap = colormap[1])
        ax1[1].legend(ncols = lgncols,loc=lgloc1)
        if isinstance(ylinetick1, (int, float)):
            ax1[1].axhline(ylinetick1, color='gray',linestyle = '--', linewidth = 1)
        if anno == True:
            lineannotate(fig1, ax1[1], snsdata1.to_period(datafreq1), enddate = enddate, roundn = roundn)       
    
    if desp == True:  #取消坐标轴
        despine(ax = ax1[0])
    if new_legend == True:
        legend_labels=snsdata0.columns
        handles, labels = ax1[0].get_legend_handles_labels()
        ax1[0].legend(handles, legend_labels, loc =lgloc0)
    
        legend_labels=snsdata1.columns
        handles, labels = ax1[1].get_legend_handles_labels()
        ax1[1].legend(handles, legend_labels, loc =lgloc1)
            
    ax1[0].set_ylabel(ylabel0, fontsize = 14, fontweight='bold')
    ax1[1].set_ylabel(ylabel1, fontsize = 14, fontweight='bold')
    ax1[0].set_title(label=title0, fontsize = 14, fontweight='bold')
    ax1[1].set_title(label=title1, fontsize = 14, fontweight='bold')
  
    if snstype == False and snsdata0.shape[1] == 1:
        line_endpoint(fig1, ax1[0], snsdata0)
        ax1[0].legend(loc =lgloc0)
        if grid:
            ax1[0].grid(grid, axis ='y', linestyle=':', alpha=0.6) 

    if snstype == False and snsdata1.shape[1] == 1:
        line_endpoint(fig1, ax1[1], snsdata1)
        ax1[1].legend(loc =lgloc1)
        if grid:
            ax1[1].grid(grid, axis ='y', linestyle=':', alpha=0.6) 

        
    fig1.suptitle(suptitle, fontweight='bold', fontsize = 16)
    #fig1.subplots_adjust(left = 0.12,bottom=0.2,right = 0.9,top=0.9,hspace=hspace)
    fig1.subplots_adjust(left = left,bottom=bottom,right = right,top=top,hspace=hspace)
    if NBERdate == True:
        NBERdate_plot(snsdata0, ax= ax1[0])
        NBERdate_plot(snsdata1, ax=ax1[1])   #添加NBER衰退期阴影
    if png == True:
        fig1.savefig(outputpath + savename+'.png', transparent = False,  bbox_inches='tight')
    if pdf == True:
        fig1.savefig(outputpath + savename+'.pdf', transparent = True,  bbox_inches='tight')
    fig1.savefig(outputpath + savename, transparent = True,  bbox_inches='tight')
    return(fig1, ax1)

def imexba(source_drive, droprowsN =2, fname = r"\D\www\macromodels\Leading\进出口.xlsx",
           sheetname = '各大洲进出口美元'):
    filename = source_drive + r"\D\www\macromodels\Leading\进出口.xlsx"
    #sheetname = '各大洲进出口美元'
    #droprowsN =2
    trade,unit = xwread(filename,sheetname,droprowsN=droprowsN)
    trade_m = trade/100     #转化为亿美元
    col_1 = []
    col_2_0 = []
    for col_ in list(trade_m.columns):
        if '出口:' in col_:
            col_1.append('出口')
            col_2_0.append(col_.replace('出口:',''))   #保留各大洲的其他国家
        elif '进口:' in col_:
            col_1.append('进口')
            col_2_0.append(col_.replace('进口:',''))  #保留各大洲的其他国家
    import re
    #col_2 = [re.sub(r'^.*:','',col_2_,count = 1) for col_2_ in col_2_0]  #删除后亚洲、欧洲、北美洲等各州的其他国家，index 重复
    col_2 = [re.sub(r':其它国家','其他',col_2_,count = 1) for col_2_ in col_2_0]
    #col_2 = [re.findall(r'^(.*)\s\(中国\)',col_)[0] for col_ in list(col_2)]
    col_2 = [re.sub(r'^.*:','',col_2_,count = 1) for col_2_ in col_2]
    #col_2 = [re.findall(r'^.*:.*:(.*)\s\(中国\)',col_)[0] for col_ in list(trade_y.columns)]  #选取(.*) 中的内容
    new_colnames = [np.array(col_1),np.array(col_2)] 
    trade_m.columns = new_colnames                #multiindex
    trade_m['进口'] = trade_m['进口']*(-1)
    trade_m_sp = trade_m['出口']+trade_m['进口']
    trade_m_sp_s = trade_m_sp[trade_m_sp>=0].copy(deep = True)    #顺差国
    trade_m_sp_d = trade_m_sp[trade_m_sp<0].copy(deep = True)    #逆差国
    iterables = [['差额'], list(trade_m_sp.columns)]
    _sp_col = pd.MultiIndex.from_product(iterables)   #build a multiindex
    trade_m_sp = pd.DataFrame(trade_m_sp.values,index =trade_m_sp.index,columns = _sp_col) #build a new dataframe with multiindex
    trade_m_com = trade_m.join(trade_m_sp)   #出口，进口，差额，三大项 组合为trade_y_com
    trade = trade_m_com.swaplevel(0,1,axis = 1).sort_index(level=0,axis = 1)  #列指标排序，深度0
    trade_com = trade.reindex(['出口','进口','差额'],level = 1,axis = 1)  #列指标 重新排序，深度1
    return(trade_com)
#######################################
##########################平面图
def treemap(plotdata, cols = ['城市','土地成交价款'],unit = '百分比', titlefs =28, title = '部分城市土地成交价款累计同比负增长', source = '资料来源:CEIC', outputpath = 'E:\\E\\python_w\\data\\\\'):
    import mpl_extra.treemap as tr
    #fig, ax = plt.subplots(figsize=(10,15),subplot_kw=dict(aspect=1.156))
    fig, ax = plt.subplots(figsize=(16,10))
    #df = plotdata[plotdata<=0].reset_index()
    df = plotdata.reset_index()
    df.columns = cols
    labels = [a + '\n' + str(b) for a, b in zip(df.iloc[:, 0], df.iloc[:, 1].fillna('na'))]
    
    trc = tr.treemap(
        ax, df, area=df.columns[1], labels=labels,
        rectprops={'ec':'w', 'lw':2},
        textprops={'c':'k', 'fontstyle':'italic','reflow':True},   ###黑色字体
        fill = df.columns[0], cmap='Set3'  )
    ax.axis('off')
    #fig.suptitle('部分城市财政收入（'+str(plotdata.name.year) +'年1-' + str(plotdata.name.month) +'月累计，亿元）' )
    #ax.set_title(title +'（'+str(plotdata.name.year) +'年1-' + 
    #             str(plotdata.name.month) +'月，百分比，'+str(df.shape[0])+'个）' ,fontsize = 12)
    ax.set_title(title +'（'+str(df.shape[0])+'个，'+unit + '）' ,fontsize = titlefs)    
    #cb = fig.colorbar(trc.mappable, ax=ax, shrink=0.5)
    fig.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.95)
    #cb.ax.set_title('hdi')
    #cb.outline.set_edgecolor('w')
    #figwmarksource2(fig,source = "资料来源:CEIC")
    #fig.text(0.13, 0.09, source,
    #        ha='left', fontsize=10, color='grey')
    #fig.text(0.9, 0.09, '''国家金融与发展实验室''',
    #        ha='right', fontsize=10, color='grey')
    fig.text(0.05, 0.07, source,
            ha='left', fontsize=14, color='grey')
    #fig.text(0.95, 0.07, '''国家金融与发展实验室''',
    #        ha='right', fontsize=14, color='grey')
    savename = title + 'treemap'
    fig.savefig(outputpath + savename+'.svg')
    fig.savefig(outputpath + savename+'.pdf')
    return(fig, ax, savename)

#######################################
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts
####################################################################################################
#########图片标题，保存图片
def axtitlesave(title, savename, outputpath='E:\\E\\python_w\\data\\\\'):
    plt.title(title)
    plt.savefig(outputpath + savename + r'.svg', transparent = True,  bbox_inches='tight')
    plt.savefig(outputpath + savename + r'.pdf', transparent = True,  bbox_inches='tight')


############################################################################################
def NBERdate_plot(plotdata,ax, source_drive = 'E:\\'):
    ###NBER 经济周期日期
    sheetname = 'NBER chronology'
    #filename = source_drive + r"\D\www\macromodels\IECASS\NBER_chronology_062020.xlsx"
    filename = source_drive + r"\D\www\macromodels\IECASS\NBER_chronology_072021.xlsx"
    #start = 'C3'; droprowsN = 0
    #US_GDP_depression = xwread(filename, sheetname, start, droprowsN)
    sht = xw.Book(filename).sheets[sheetname]
    
    date_recession = sht.range((27,3),(38,4)).value
    #df = sht.range(start).options(pd.DataFrame, expand='table',empty = np.nan).value
    #date_recession[-1] = ['February 2020','April 2020']   #结束日期暂定为 June 2020，方便作图，20200719NBER公告202002-202004是峰-谷衰退期
    
    for dr in date_recession:
        xmin = dr[0][:-9]    #删除最后9个字符
        xmax = dr[1][:-9]
        #[re.findall(".*:(.*):.*",col)[0] for col in list(PPI.columns)]    #匹配两个 : 之间的字符
        #if '\xa0' in dr[0]:
        #    xmin = re.findall("\A(.*)\xa0", dr[0])[0]
        #else:
        #    xmin = re.findall("\A(.*) ",dr[0])[0]   #删除' '之后的字符
        #if '\xa0' in dr[1]:
        #    xmax = re.findall("\A(.*)\xa0", dr[1])[0]
        #else:
        #    xmax = re.findall("\A(.*) ",dr[1])[0]   #删除' '之后的字符
        if dt.datetime.strptime(xmin,'%B %Y')>=plotdata.index[0]:
            ax.axvspan(xmin, xmax,facecolor='0.8', alpha=0.5)
    return(date_recession)

################################################################################################filename = r"E:\python_w\wind数据表.xlsx"
def maximize(backend=None,fullscreen=False):
    """Maximize window independently on backend.
    Fullscreen sets fullscreen mode, that is same as maximized, but it doesn't have title bar (press key F to toggle full screen mode)."""
    if backend is None:
        backend=mpl.get_backend()
    mng = plt.get_current_fig_manager()

    if fullscreen:
        mng.full_screen_toggle()
    else:
        if backend == 'wxAgg':
            mng.frame.Maximize(True)
        elif backend == 'Qt4Agg' or backend == 'Qt5Agg':
            mng.window.showMaximized()
        elif backend == 'TkAgg':
            mng.window.state('zoomed') #works fine on Windows!
        else:
            print ("Unrecognized backend: ",backend) #not tested on different backends (only Qt)
    plt.show()

    #plt.pause(0.1) #this is needed to make sure following processing gets applied (e.g. tight_layout)

##疫情分析
'''
def twinx_plot(plot_data1,plot_data2,ax1_ylabel,ax2_ylabel):    
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel(ax1_ylabel, color=color)
    #ax1.plot(t, data1, color=color)
    plot_data1.plot(ax = ax1,color = color,linewidth = 3)
    plt.legend(loc = 'upper left')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel(ax2_ylabel, color=color)  # we already handled the x-label with ax1
    #ax2.plot(t, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plot_data2.plot(ax = ax2,color = color,linewidth = 3)
    plt.legend(loc = 'lower right')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
'''
########################################################################
def twinx_plot(plot_data1,plot_data2,ax1_ylabel,ax2_ylabel,figsize = (9, 6),
               legloc1 = 'upper left',legloc2 = 'lower left', title ='',lineanno=True,
               savename= 'savename', source ='资料来源：WIND'):    
    plot_data1 = plot_data1.sort_values(by =plot_data1.index[-1], axis = 1, ascending = False)
    plot_data2 = plot_data2.sort_values(by =plot_data2.index[-1], axis = 1, ascending = False)
    fig, ax1 = figwmarksource1(figsize=figsize, source = source)
    plot_data1.plot(ax = ax1,colormap = 'autumn',linewidth = 3,style = ['-','-.',':','--'], alpha =0.8)
    color = ax1.get_lines()[0].get_color()
    #color = 'tab:red'
    #ax1.set_xlabel()
    ax1.set_ylabel(ax1_ylabel, color=color, loc = 'center')
    #ax1.plot(t, data1, color=color)
    ax1.legend(loc = legloc1,labelcolor = color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.spines['left'].set(edgecolor=color, facecolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    plot_data2.plot(ax = ax2,colormap = 'winter',linewidth = 3,style = ['-','-.'], alpha = 0.6)
    #color = 'tab:blue'
    color = ax2.get_lines()[0].get_color()
    ax2.set_ylabel(ax2_ylabel, color=color, loc = 'center')  # we already handled the x-label with ax1
    #ax2.plot(t, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.spines['right'].set_color(color)
    ax2.legend(loc = legloc2,labelcolor = color)
    #fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.suptitle(title,fontsize = 12)
    #fig.set_figwidth(8, forward=True)
    fig.subplots_adjust(left = 0.12,bottom = 0.15,right = 0.9,top = 0.9)
    if lineanno == True:
        lineannotate(fig, ax1, plot_data1.to_period('M'), arrow='no', Grid=False,xshift=10)
        lineannotate(fig, ax2, plot_data2.to_period('M'), arrow='no', Grid=False,xshift=10)
    axtitlesave(title, savename, outputpath='E:\\E\\python_w\\data\\\\')
    return(fig, ax1,ax2)
##############################################################
def twin_plot(fig,ax1,plot_data1, plot_data2, ylabel1, ylabel2,loc1,loc2):
#画双y轴的图像，ylabel1, ylabel2分别为左右图标    
    #loc1 = 'upper left'
    #loc2 = 'lower right'
    #fig, ax1 = plt.subplots()
    color = 'tab:red'
    #ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel1, color=color)
    #ax1.plot(t, data1, color=color)
    plot_data1.plot(ax = ax1,color=color,style = ['-','--',':'],linewidth = 3)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(list(plot_data1.columns),loc = loc1,labelcolor = color)
    #x轴刻度
    #ax1.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel(ylabel2, color=color)  # we already handled the x-label with ax1
    #ax2.plot(t, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plot_data2.plot(ax = ax2,color=color, linestyle = (0, (3, 1, 1, 1)),linewidth = 3)
    ax2.legend([plot_data2.columns[0]+'(右轴)'],loc = loc2,labelcolor = color)
    #标注x轴刻度
    #ax2.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
    #ax2.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
    #plt.setp(ax2.get_xticklabels(), rotation=30, ha="right")    
    
    #fig.tight_layout()  # otherwise the right y-label is slightly clipped
    return(fig, ax1,ax2)
##############################################################
def line_bar(fig1,ax1,plotdata1, plotdata2, ylabel1, ylabel2,figsize = (9,6),loc1 = 'upper left',loc2='lower right'):
###画时间序列有问题
#画双y轴的图像，ylabel1, ylabel2分别为左右图标    
    #loc1 = 'upper left'
    #loc2 = 'lower right'
    #plot_data1 = US_deficit.iloc[:,[0,1]].loc['2020':,:]
    #plot_data2 = US_deficit.iloc[:,2].loc['2020':]
    #ylabel1 = '亿美元'; ylabel2 = '亿美元'
    #fig, ax1 = plt.subplots(figsize=figsize)
    color = 'tab:red'
    if len(plotdata1.columns) >=2:
        linecolors = mpl.colormaps['Reds']
        linecolors = linecolors(np.linspace(0.5, 1, len(plotdata1.columns)))
    elif len(plotdata1.columns) ==1:
        linecolors = [color]
    #ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel1, color=color)
    #ax1.plot(t, data1, color=color)
    #plotdata1.plot(ax = ax1,cmap=linecolors,style = ['-','--',':','.'],
    plotdata1.plot(ax = ax1,color=linecolors,
                    linewidth = 3,alpha = 0.8)
    ax1.tick_params(axis='y', labelcolor=color)
    lines = ax1.get_lines()   #线 -1
    linecols = [line.get_color() for line in lines ] #线颜色
    ax1.legend(loc = loc1,labelcolor = linecols)
    #x轴刻度
    #ax1.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    if len(plotdata2.columns) >=2:
        barcolors = mpl.colormaps['Blues']    
        barcolors = barcolors(np.linspace(0.5, 1, len(plotdata2.columns)))
    elif len(plotdata2.columns) ==1:
        barcolors = [color]
    ax2.set_ylabel(ylabel2, color=color)  # we already handled the x-label with ax1
    #ax2.plot(t, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plotdata2.plot.bar(ax = ax2,color=barcolors,alpha = 0.3)
    ax2.legend(loc = loc2)
    #ax2.plot(plotdata2,color = barcolors,alpha = 0.4)
    ax2.legend(loc = loc2,labelcolor = barcolors)
    
    #标注x轴刻度
    #ax2.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
    #ax2.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
    #plt.setp(ax2.get_xticklabels(), rotation=30, ha="right")    
    
    #fig1.tight_layout()  # otherwise the right y-label is slightly clipped
    return(fig1, ax1,ax2)

####################################################
def rnyears(dat,frq,n):
##n年平均增速
    if frq == 'M':
        #dat 为月度数据
        t2_  = (dat/dat.shift(12*n))
        t2 = (np.power(t2_,1/n)-1)*100
    elif frq == 'Q':
        #dat 为季度数据
        t2_  = (dat/dat.shift(4*n))
        t2 = (np.power(t2_,1/n)-1)*100
    return(t2)


################################################
###两年平均增长率
def r2years(dat,frq):
    if frq == 'M':
        #dat 为月度数据
        t2_  = (dat/dat.shift(24))
        t2 = (t2_.apply(np.sqrt)-1)*100
    elif frq == 'Q':
        #dat 为季度数据
        t2_  = (dat/dat.shift(8))
        t2 = (t2_.apply(np.sqrt)-1)*100
    return(t2)
############################################
###各指标累计和单月合并展示
def mlj_pm_plot(df1,start1,title1,ylabel1,legcolsn1, 
                df2,start2,title2,ylabel2,legcolsn2, outputpath, closefig = True):
    for i,item in enumerate(df1.columns):
        plt.figure(figsize = (9,6))
        plt.subplot(211)    ## 累计
        seasplot(df1,start1, df1.columns[i], title1 + df1.columns[i], ylabel1,legcolsn = legcolsn1, newfig = False)
        plt.subplots_adjust(left=0.15, right=0.95,top = 0.92,bottom=0.1)
        plt.xlabel('')
        plt.subplot(212)   ## 单月
        seasplot(df2,start2, df2.columns[i], title2 + df2.columns[i], ylabel2,legcolsn = legcolsn2, newfig = False)
        plt.subplots_adjust(left=0.15, right=0.95,top = 0.92,bottom=0.1)
        plt.savefig(outputpath + str(r'\\') + item.replace(':','_')+ 
                    title1.replace(':','_') +title2.replace(':','_') +'.svg')
        if closefig:
            plt.close('all')
    return()
###各指标累计单独展示
def mlj_pm_plot_wm0(df1,start1,title1,ylabel1,suptitlestr,outputpath, closefig = True):
    savenames = []  #保存的图片文件名称list
    totalcol = np.shape(df1)[1]
    for i,item in enumerate(df1.columns):
        fig,ax = figwmarksource1(nrows=1,ncols=1)
        seasplot1(fig,ax,df1,start1, df1.columns[i], title1 + df1.columns[i], ylabel1)
        ax.set_title(ax.get_title()+ ' |==>> %+.2f%%' %(df1.iloc[-1,i]),
                         color = ax.get_lines()[-1].get_color())         
        ax.axvline(df1[item].dropna().index[-1].month, ls='--', color='gray',linewidth = 1)
        ax.legend(labelcolor='linecolor')
        fig.suptitle(suptitlestr + '（%d - %s)' %(totalcol,i+1))
        savename = item.replace(':','_')+ title1.replace(':','_')  
        savename = savename.replace('%','百分比')
        savename = savename.replace('_','')
        fig.savefig(outputpath + str(r'\\') + savename +'.svg', transparent = True,  bbox_inches='tight')
        fig.savefig(outputpath + str(r'\\') + savename +'.pdf', transparent = True,  bbox_inches='tight')
                
        #plt.savefig(outputpath + str(r'\\') + item.replace(':','_')+ 
        #            title1.replace(':','_') +title2.replace(':','_') +'.svg')
        savenames.append(savename +'.pdf')
        if closefig:
            plt.close('all')
    return(savenames)    
def mlj_pm_plot_wm(df1,start1,title1,ylabel1,
                df2,start2,title2,ylabel2,suptitlestr,outputpath, closefig = True):
    savenames = []  #保存的图片文件名称list
    totalcol = np.shape(df1)[1]
    for i,item in enumerate(df1.columns):
        fig,axs = figwmarksource1(nrows=2,ncols=1,hspace=0.2)
        ## 累计
        seasplot1(fig,axs[0],df1,start1,df1.columns[i], title1 + df1.columns[i] ,ylabel1)
        axs[0].set_title(axs[0].get_title()+ ' |==>> %+.2f<<' %(df1.iloc[:, i].dropna().iloc[-1]),
                         color = axs[0].get_lines()[-1].get_color())        
        axs[0].axvline(df1[item].dropna().index[-1].month, ls='--', color='gray',linewidth = 1)
        axs[0].legend(labelcolor='linecolor', ncols = 3)        
        ## 单月
        seasplot1(fig,axs[1],df2,start2, df2.columns[i], title2 + df2.columns[i], ylabel2)
        axs[1].set_title(axs[1].get_title()+ ' |==>> %+.2f<<' %(df2.iloc[:, i].dropna().iloc[-1]),
                         color = axs[1].get_lines()[-1].get_color())         
        axs[1].axvline(df2.iloc[:,i].dropna().index[-1].month, ls='--', color='gray',linewidth = 1)
        axs[1].get_legend().set_visible(False)
        fig.suptitle(suptitlestr + '（%d - %s)' %(totalcol,i+1))
        item = item.replace('<','小于')
        savename = item.replace(':','_')+ title1.replace(':','_') +title2.replace(':','_') 
        savename = savename.replace('%','百分比')
        savename = savename.replace('_','').replace('/', '或')
        fig.savefig(outputpath + str(r'\\') + savename +'.svg', transparent = True,  bbox_inches='tight')
        fig.savefig(outputpath + str(r'\\') + savename +'.pdf', transparent = True,  bbox_inches='tight')
                
        #plt.savefig(outputpath + str(r'\\') + item.replace(':','_')+ 
        #            title1.replace(':','_') +title2.replace(':','_') +'.svg')
        savenames.append(savename +'.pdf')
        if closefig:
            plt.close('all')
    return(savenames)    
###按财年列示##########################################
# seasplot_F(fig1, ax1,US_deficit,start,column,title,ylabel, endy='2024', startm='10', cumsum = False, detail = True, legcolsn = 1, mask0=True):#####################################
def mlj_pm_plot_wm_F(df1,start1,title1,ylabel1,
                df2,start2,title2,ylabel2,suptitlestr,outputpath, endy, startm='10', closefig = True,cumsum = False, detail = True, legcolsn = 1, mask0=True):
    savenames = []  #保存的图片文件名称list
    totalcol = np.shape(df1)[1]
    for i,item in enumerate(df1.columns):
        fig,axs = figwmarksource1(nrows=2,ncols=1,hspace=0.2)
        ## 累计
        seasplot_F(fig,axs[0],df1,start1,df1.columns[i], title1 + df1.columns[i] ,ylabel1, endy, startm='10', cumsum = False, detail = True, legcolsn = 3, mask0=True)
        axs[0].set_title(axs[0].get_title()+ ' |==>> %+.2f<<' %(df1.iloc[:, i].dropna().iloc[-1]),
                         color = axs[0].get_lines()[-1].get_color())
        if df1[item].dropna().index[-1].month < 10:
            axs[0].axvline(df1[item].dropna().index[-1].month + 12-int(startm), ls='--', color='gray',linewidth = 1)
        if df1[item].dropna().index[-1].month >= 10:
            axs[0].axvline(df1[item].dropna().index[-1].month -int(startm), ls='--', color='gray',linewidth = 1)
        
        axs[0].legend(labelcolor='linecolor', ncols = 3)        
        ## 单月
        seasplot_F(fig,axs[1],df2,start2, df2.columns[i], title2 + df2.columns[i], ylabel2, endy, startm='10', cumsum = False, detail = True, legcolsn = 3, mask0=True)
        axs[1].set_title(axs[1].get_title()+ ' |==>> %+.2f<<' %(df2.iloc[:, i].dropna().iloc[-1]),
                         color = axs[1].get_lines()[-1].get_color())         
        if df1[item].dropna().index[-1].month < 10:
            axs[1].axvline(df2.iloc[:,i].dropna().index[-1].month + 12-int(startm), ls='--', color='gray',linewidth = 1)
        if df1[item].dropna().index[-1].month >= 10:
            axs[1].axvline(df2.iloc[:,i].dropna().index[-1].month -int(startm), ls='--', color='gray',linewidth = 1)
        
        axs[1].get_legend().set_visible(False)
        fig.suptitle(suptitlestr + '（%d - %s)' %(totalcol,i+1))
        item = item.replace('<','小于')
        savename = item.replace(':','_')+ title1.replace(':','_') +title2.replace(':','_') 
        savename = savename.replace('%','百分比')
        savename = savename.replace('_','').replace('/', '或')
        fig.savefig(outputpath + str(r'\\') + savename +'.svg', transparent = True,  bbox_inches='tight')
        fig.savefig(outputpath + str(r'\\') + savename +'.pdf', transparent = True,  bbox_inches='tight')
                
        #plt.savefig(outputpath + str(r'\\') + item.replace(':','_')+ 
        #            title1.replace(':','_') +title2.replace(':','_') +'.svg')
        savenames.append(savename +'.pdf')
        if closefig:
            plt.close('all')
    return(savenames)    

################################################

def ROD_wm(df1,start1,title1,ylabel1,
                df2,start2,title2,ylabel2,df3, suptitlestr,outputpath, closefig = True):
    ####上图：收支增速，下图：收支赤字， 最好用单月数据，以比较每个月的财政扩张力度
    savenames = []  #保存的图片文件名称list
    totalcol = np.shape(df1)[1]    
    for i, item in enumerate(df1):
        fig,axs = figwmarksource1(nrows = 2,source='资料来源：财政部',hspace=0.2,sharex = True)
        plotdata1 = pd.concat([df1.loc[start1:,item], df2.loc[start1:,df2.columns[i]]],axis = 1)
        plotdata1.columns = ['收入增速',  '支出增速']
        plotdata1.plot(ax = axs[0])
        axs[0].set_title(item + title1) ;   axs[0].set_ylabel(ylabel1)
        plotdata2 = df3.loc[start1:,df3.columns[i]]
        plotdata2.plot(ax = axs[1])
        axs[1].set_title(item + title2) ;   axs[1].set_ylabel(ylabel2)
        fig.suptitle(suptitlestr + '（%d - %s)' %(totalcol,i+1))
        lineannotate(fig, axs[0], plotdata1, arrow='yes', Grid=False,xshift=10,enddate=False)
        lineannotate(fig, axs[1], plotdata2, arrow='yes', Grid=False,xshift=10,enddate=False)
        item = item.replace('<','小于')
        savename = item.replace(':','_')+ title1.replace(':','_') +title2.replace(':','_') 
        savename = savename.replace('%','百分比')
        savename = savename.replace('_','').replace('/', '或')
        fig.savefig(outputpath + str(r'\\') + savename +'.svg', transparent = True,  bbox_inches='tight')
        fig.savefig(outputpath + str(r'\\') + savename +'.pdf', transparent = True,  bbox_inches='tight')
                
        #plt.savefig(outputpath + str(r'\\') + item.replace(':','_')+ 
        #            title1.replace(':','_') +title2.replace(':','_') +'.svg')
        if closefig:
            plt.close('all')
        savenames.append(savename +'.pdf')
    return(savenames)    
################################################################################
def ljplusindi(indprolj,unit,titlestr,outputpath, closefig = True):
    con_cols = []   #清除'(DC)' 列
    savenames = []  #保存的图片文件名称list
    for ii,item in enumerate(indprolj.columns):
        if not '(DC)' in(item):
            con_cols.append(item)
    con_indprolj = indprolj.loc[:,con_cols]
    con_unit = unit.loc[:,con_cols]
    totalcol = np.shape(con_indprolj)[1]
    for ii,item in enumerate(con_indprolj.columns):
        if not '(DC)' in(item):
            fig,axs = figwmarksource1(nrows=2,ncols=1,hspace=0.2)
            plotdata = con_indprolj
            #temp1 = (con_indprolj[con_indprolj.index.month ==2]*(31/(24+31)))
            #temp1.index = temp1.index-pd.offsets.MonthEnd(1)
            #plotdata[plotdata.index.month==1] = temp1  ####1月份数据缺失，估算
            #plotdata[plotdata.index.month==2] = con_indprolj[con_indprolj.index.month ==2]*1    ####2月份数据缺失，估算
            plotdata_pct12 = plotdata[item].dropna().pct_change(12)*100
            seasplot1(fig,axs[0],plotdata,'2015',item,item ,con_unit.loc['单位',item])
            axs[0].set_title(axs[0].get_title()+ ' |==>> 累计同比%+.2f%%' %(plotdata_pct12.iloc[-1]),
                             color = axs[0].get_lines()[-1].get_color())
            axs[0].axvline(plotdata[item].dropna().index[-1].month, ls='--', color='gray',linewidth = 1)
            axs[0].legend(labelcolor='linecolor')
        if not '(DC)' in(item):
            plotdata = csm2m(con_indprolj)
            #plotdata[plotdata.index.month==1] = con_indprolj[con_indprolj.index.month ==2]*(31/(24+31))    ####2月份数据缺失，估算
            #plotdata[plotdata.index.month==2] = con_indprolj[con_indprolj.index.month ==2]*(24/(24+31))    ####2月份数据缺失，估算
            plotdata_pct12 = plotdata[item].dropna().pct_change(12)*100
            plotdata_pct1 = plotdata[item].dropna().pct_change(1)*100
            seasplot1(fig,axs[1],plotdata,'2015',item,item.replace('累计','单月'),con_unit.loc['单位',item])
            axs[1].set_title(axs[1].get_title()+ ' |==>> 同比%+.2f%%,环比%+.2f%%'
                             %(plotdata_pct12.iloc[-1],plotdata_pct1.iloc[-1]),
                             color = axs[1].get_lines()[-1].get_color())   ####用2022年线颜色
            axs[1].axvline(plotdata[item].dropna().index[-1].month, ls='--', color='gray',linewidth = 1)
            axs[1].get_legend().set_visible(False)
            
        #plt.subplots_adjust(left=0.15, right=0.95,top = 0.92,bottom=0.1)
        #fig.suptitle('主要工业品产量（%d - %s)' %(totalcol,ii+1))
        fig.suptitle(titlestr + '（%d - %s)' %(totalcol,ii+1))
        savename = titlestr + item.replace(':','')+ '和单月'
        savename = savename.replace('%','百分比')
        fig.savefig(outputpath + str(r'\\') + savename +'.svg', transparent = True,  bbox_inches='tight')
        fig.savefig(outputpath + str(r'\\') + savename +'.pdf', transparent = True,  bbox_inches='tight')
        savenames.append(savename +'.pdf')
        if closefig:
            plt.close('all')
    return(savenames)
###############################################
def twoseas(CPI_pct,CPI, doc, outputpath,  suptitle_='CPI分品类',freq='每月', title0='定基',title1='同比',
             ylabel0 = '百分比', ylabel1='百分比',
             start='2022', doctex = False, figsource = '资料来源：美国', doctexsource = 'CEIC, NFID'):
    ##CPI为包含各行业品类的dataframe,上图为seasplot，下图为seasplot
    totalcol = len(CPI.columns)
    #global doc
    CPI = CPI.loc[start:, :].dropna(axis = 1)
    for ii, item in enumerate(CPI.columns):
        if not '(DC)' in(item) :
            fig1,axs = figwmarksource1(nrows=2,ncols=1,sharex=False, hspace=0.3,x0y0 = (0.75,1.5/20), source=figsource)
            title = item.replace('/', '或')+'(' + freq + ')' + title0
            if isinstance(ylabel0, str):
                ylabel0_ = ylabel0
            elif isinstance(ylabel0, pd.DataFrame):
                ylabel0_ = ylabel0.iloc[0, ii]
            seasplot1(fig1,axs[0],CPI_pct,start,item,title,ylabel0_, legcolsn=4, detail=True)
            axs[0].set_title(title0)
            axs[0].set_xlabel('')
            if isinstance(ylabel1, str):
                ylabel1_ = ylabel1
            elif isinstance(ylabel1, pd.DataFrame):
                ylabel1_ = ylabel1.iloc[0, ii]
            seasplot1(fig1,axs[1],CPI,start,item,title,ylabel1_, legcolsn=4, detail=True)
            axs[1].set_title(title1)
            suptitle = suptitle_ + '('+str(totalcol)+'-'+ str(ii+1)+')-' +  item.replace(':','')
            fig1.suptitle(suptitle)
            item = item.replace('/', '或')
            savename = suptitle
            fig1.savefig(outputpath + savename+ '.svg', transparent = True,  bbox_inches='tight')     #不能用bbox_inches = 'tight'，保存不了
            fig1.savefig(outputpath + savename+ '.pdf', transparent = True,  bbox_inches='tight')
            plt.close()
            if doctex == True:
                doc = frame_image1(doc, suptitle, savename+ r'.pdf', '''''', 
                            source=doctexsource, width = r'0.8\textwidth',height = r'0.8\textheight')
    if doctex == True:
        return(doc)
    elif doctex == False:
        return(fig1, axs)

##############################################################
def seasline(CPI_pct,CPI, doc, outputpath,  suptitle_='CPI分品类',freq='每月', title0='定基',title1='同比',
             ylabel0 = '百分比', ylabel1='百分比',
             start='2022', doctex = False, hspace = 0.3, figsource = '资料来源：美国', doctexsource = 'CEIC, NFID'):
    ##CPI为包含各行业品类的dataframe,上图为seasplot，下图为线图
    totalcol = len(CPI.columns)
    #global doc
    CPI = CPI.loc[start:, :].dropna(axis = 1)
    for ii, item in enumerate(CPI.columns):
        if not '(DC)' in(item) :
            fig1,axs = figwmarksource1(nrows=2,ncols=1,sharex=False, hspace=hspace,x0y0 = (0.75,1.5/20), source=figsource)
            title = item.replace('/', '或')+'(' + freq + ')' + title0
            if isinstance(ylabel1, str):
                ylabel0_ = ylabel0
            elif isinstance(ylabel1, pd.DataFrame):
                ylabel0_ = ylabel0.iloc[0, ii]
            seasplot1(fig1,axs[0],CPI_pct,start,item,title,ylabel0_, legcolsn=4, detail=True)
            line_endpoint(fig1, axs[1], CPI.loc[start:, item].dropna())
            if isinstance(ylabel1, str):
                axs[1].set_ylabel(ylabel1)
            elif isinstance(ylabel1, pd.DataFrame):
                axs[1].set_ylabel(ylabel1.iloc[0, ii])
            axs[1].set_title(title1)
            suptitle = suptitle_ + '('+str(totalcol)+'-'+ str(ii+1)+')'
            fig1.suptitle(suptitle)
            item = item.replace('/', '或')
            savename = suptitle+ item.replace(':','')
            fig1.savefig(outputpath + savename+ '.svg', transparent = True,  bbox_inches='tight')     #不能用bbox_inches = 'tight'，保存不了
            fig1.savefig(outputpath + savename+ '.pdf', transparent = True,  bbox_inches='tight')
            plt.close()
            if doctex == True:
                doc = frame_image1(doc, suptitle, savename+ r'.pdf', '''''', 
                            source=doctexsource, width = r'0.8\textwidth',height = r'0.8\textheight')
    if doctex == True:
        return(doc)
    elif doctex == False:
        return(fig1, axs)

def twolines(CPI, CPI_pct,  doc, outputpath,  datafreq0 = 'M',datafreq1 = 'M', roundn =1, suptitle_='CPI分品类',freq='每月', title0='定基',title1='同比', 
             start='2022', ylabel0='unit', ylabel1 = 'unit', doctex = False,sharex = False,dropna = False, figsource = '资料来源：美国', doctexsource = 'CEIC, NFID'):
    ##CPI为包含各行业品类的dataframe,上图为规模绝对值，下图为百分比线图,
    # ylabel0,ylabel1可以是string, 也可以是unit
    totalcol = len(CPI.columns)
    #global doc
    #CPI = CPI.loc[start:, :].dropna(axis = 0)  对dataframe的各列整齐删除含有NA的行
    #CPI_pct = CPI_pct.loc[start:, :].dropna(axis = 0)
    for ii, item in enumerate(CPI.columns):
        if not '(DC)' in(item) :
            if dropna == True:
                CPI = CPI.dropna()
                CPI_pct = CPI_pct.dropna()            
            fig1,axs = figwmarksource1(nrows=2,ncols=1,sharex=sharex, hspace=0.3,
                                       x0y0 = (0.75,1.5/20), source=figsource)
            title = item.replace('/', '或')+'(' + freq + ')'
            CPI.loc[start:, item].to_period(datafreq0).plot(ax =axs[0], linewidth = 3)
            lineannotate(fig1, axs[0], CPI.loc[start:, item].to_period(datafreq0), roundn = roundn)
            if isinstance(ylabel0, str):
                axs[0].set_ylabel(ylabel0)
            elif isinstance(ylabel0, pd.DataFrame):
                axs[0].set_ylabel(ylabel0.loc[ylabel0.index[0], item])
            axs[0].set_title(title+ title0)
            CPI_pct.loc[start:, item].to_period(datafreq1).plot(ax =axs[1], linewidth = 3)
            lineannotate(fig1, axs[1], CPI_pct.loc[start:, item].to_period(datafreq1), roundn = roundn)
            if isinstance(ylabel1, str):
                axs[1].set_ylabel(ylabel1)
            elif isinstance(ylabel1, pd.DataFrame):   #ylabel1为 读取数据单位unit
                axs[1].set_ylabel(ylabel1.loc[ylabel1.index[0], item])
            axs[1].set_title(title1)
            suptitle = suptitle_ + '('+str(totalcol)+'-'+ str(ii+1)+')'
            fig1.suptitle(suptitle)
            item = item.replace('/', '或')
            savename = suptitle + item.replace(':','')
            fig1.savefig(outputpath + savename+ '.svg', transparent = True,  bbox_inches='tight')     #不能用bbox_inches = 'tight'，保存不了
            fig1.savefig(outputpath + savename+ '.pdf', transparent = True,  bbox_inches='tight')
            if doctex == True:
                plt.close()
                doc = frame_image1(doc, suptitle, savename+ r'.pdf', '''''', 
                            source=doctexsource, width = r'0.8\textwidth',height = r'0.8\textheight')
    if doctex == True:
        return(doc)
    elif doctex == False:
        return(fig1, axs)

def duallines(df1,unit_,df2,ylabel2,legend1, legend2,suptitlestr, outputpath,ylabel1 = 'various', closefig = True):
    ###ylabel1 = 'various'， 表示取不同单位， 如果ylabel1 = '亿美元' 等等，表示取相同单位
    savenames = []  #保存的图片文件名称list
    totalcol = np.shape(df1)[1]
    for i,item in enumerate(df1.columns):
        ##sharex = True,的图，上下的线长度需一致
        df1temp = df1.loc[:,item].dropna(); df2temp = df2.loc[:,item].dropna()
        start = min(df1temp.index[0],df2temp.index[0])
        end = max(df1temp.index[-1],df2temp.index[-1])
        df1plot_i = df1.loc[start:end,item]  ;  df2plot_i = df2.loc[start:end,item] 
        fig1,axs = figwmarksource1(nrows=2, source='资料来源：CEIC',hspace=0.15, figsize=(9,6))
        df1plot_i.plot(alpha = 0.8,ax = axs[0])    ###'1982-1984=100'
        lineannotate(fig1, axs[0], df1plot_i.to_period('M'),enddate = False)
        #axs[0].legend('',loc = 'upper left',framealpha = 0)  ###完全透明，看不见
        axs[0].legend(legend1,loc = 'best')
        #axs[0].get_legend().set_visible(False)
        #suptitlestr = suptitlestr + item
        #axs[0].set_title(suptitlestr + item,fontsize = 12)
        if ylabel1 == 'various':
            ylabel = unit_.iloc[0,i]
        elif ylabel1 != 'various':
            ylabel = ylabel1
        axs[0].set_ylabel(ylabel)
        #fig.set_figwidth(8, forward=True)
        axs[0].set_xlabel('')
        df2plot_i.plot(alpha = 0.8,ax = axs[1])
        lineannotate(fig1, axs[1], df2plot_i.to_period('M'))
        #axs[1].legend([],labelcolor='linecolor',framealpha = 0)
        axs[1].legend(legend2,loc = 'best')
        fig1.suptitle(suptitlestr + item + '（%d - %s)' %(totalcol,i+1))
        axs[1].set_ylabel(ylabel2)
        fig1.subplots_adjust(top = 0.95)
        savename = item.replace(':','_')+ suptitlestr 
        savename = savename.replace('%','百分比')
        savename = savename.replace('_','')
        savename = savename.replace('<','小于')
        savename = savename.replace('>','大于')
        fig1.savefig(outputpath + str(r'\\') +suptitlestr + savename +'.svg', transparent = True,  bbox_inches='tight')
        fig1.savefig(outputpath + str(r'\\') +suptitlestr + savename +'.pdf', transparent = True,  bbox_inches='tight')
        savenames.append(savename +'.pdf')
        if closefig:
            plt.close('all')
    return(savenames)    


def frame_image1(doc, frame_title, image, annotation, 
                source, width = r'0.6\textwidth',height = r'0.6\textheight',*args, **kwargs):
    ##配合\usepackage[Export]{adjustbox},设置box 最大值，使大图自动缩小至需要的尺寸，不会超出范围
    ##\includegraphics[max size={0.6\textwidth}{0.6\textheight}]{CPI分类商品价格变化.pdf}%
    plt.close()
    doc.append(NoEscape(r'\begin{frame}{'+ frame_title +'}'))
    doc.append(NoEscape(annotation))
    doc.append(NoEscape(r'\begin{figure}[htp]'))                    #here, top,  or new page
    doc.append(NoEscape(r'\centering'))
    #doc.append(NoEscape(r'\caption{' + image.rstrip('.pdf')+'}')) 
    doc.append(NoEscape(r'\includegraphics[max size={' + width +'}'+'{'+ height +'}]{'+image+'}'))
    #doc.append(NoEscape(r'\includegraphics[scale=0.6]{image}'))
    doc.append(NoEscape(r'\label{fig:'+ image.rstrip('.pdf')+ '}'))
    doc.append(NoEscape(r'\end{figure}'))
    doc.append(NoEscape(r'\end{frame}'))
    return(doc)



def del_month(plotdata,months):
    ###删除1-2份数据, months = [1,2]
    temp_index = plotdata[plotdata.index.month==months[0]].index 
    plotdata.drop(temp_index,inplace = True)
    temp_index = plotdata[plotdata.index.month==months[1]].index 
    plotdata.drop(temp_index,inplace = True)
    return(plotdata)

def lj12simple(con_indprolj):
    ###假设所有1月份数据缺失
    #补齐累计序列1-2月数据
    temp1 = (con_indprolj[con_indprolj.index.month ==2]*(31/(24+31)))
    temp1.index = temp1.index-pd.offsets.MonthEnd(1)
    con_indprolj[con_indprolj.index.month==1] = temp1  ####1月份数据缺失，估算
    #con_indprolj[con_indprolj.index.month==2] = con_indprolj[con_indprolj.index.month ==2]*1    ####2月份数据缺失，估算
    return(con_indprolj)
####################################################################################
def lj12raw(con_indprolj):
    ###假设部分一月份数据缺失
    ###补齐累计序列1-2月数据
    #con_indprolj = indprolj
    con_indprolj = con_indprolj.resample('ME').last()
    temp1 = (con_indprolj[con_indprolj.index.month ==2]*(31/(24+31)))
    temp1 = temp1.interpolate(method='linear')
    temp1.index = temp1.index-pd.offsets.MonthEnd(1)
    for ii,col in enumerate(con_indprolj.columns):
        raw1 = con_indprolj[con_indprolj.index.month==1].loc[:,[col]]
        for j1 in raw1.index:
            if np.isnan(raw1.loc[j1,col]):
                con_indprolj.loc[j1,col] = temp1.loc[j1,col]
    return(con_indprolj)
def classify(colname = '工业企业:利润总额:累计', indicator1 = '利润总额:累计' , indicator2 = '累计同比:利润总额'):
    #对columnsname 进行分类
    mlj,pct = [], []
    if indicator1 == '':
        if indicator2 not in colname:
            mlj = mlj + [colname]
        elif indicator2 in colname:
            pct = pct + [colname]
    elif indicator1 != '':            
        if indicator1 in colname:
            mlj = mlj + [colname]
        elif indicator2 in colname:
            pct = pct + [colname]
    return(mlj, pct)

def clscols(profitmlj, indicator1 = ':利润总额:累计' , indicator2 = '累计同比:利润总额'):
    mljcol, mljpcol = [], []
    for i, colname in enumerate(profitmlj.columns):
        mljcol_, mljpcol_ = classify(colname, indicator1 , indicator2)
        #dat = pd.concat([dat,dat_],axis = 1)
        mljcol, mljpcol = mljcol + mljcol_, mljpcol +mljpcol_
    return(profitmlj.loc[:, mljcol], profitmlj.loc[:, mljpcol])

def ser2frame(US_deficit,colname='联邦政府收入', starty='2018', endy='2024', startm='10'):
    ###将序列转换为财年的dataframe, 可以选择起始月份
    new_index = pd.date_range(US_deficit.index[0], endy+'-09-30', freq = 'ME')
    US_deficit_ = US_deficit.reindex(new_index)
    #starty = '2000'
    Rev = US_deficit_.loc[starty+'-'+ startm:, [colname]].values
    Rev_matrix = Rev.reshape(math.ceil(len(Rev)/12), 12)
    rowsindex = np.arange(int(starty)+1, int(endy)+1)
    colindex = pd.date_range(starty+'-10-31', periods =12, freq = 'ME').month
    colindex = map(lambda x: str(x), colindex)
    US_deficit_F = pd.DataFrame(data = Rev_matrix, index = rowsindex, columns=colindex)
    US_deficit_F.index.name = '年度'
    US_deficit_F.columns.name = '月度'
    return(US_deficit_F)

def seasplot_F(fig1, ax1,US_deficit,start,column,title,ylabel, endy = '2024', startm='10', cumsum = False, detail = True, legcolsn = 1, mask0=True):
    #deficit_ym = deficit.groupby([deficit.index.year,deficit.index.month]).sum().copy(deep = True)
    #deficit_ym.rename_axis(index = ['年度','月份'],inplace = True)
    US_deficit_F = ser2frame(US_deficit,colname = column, starty = start, endy = endy, startm=startm)
    if cumsum == False:
        deficit_ym = US_deficit_F
    elif cumsum == True:
        deficit_ym = US_deficit_F.cumsum(axis = 1)
    if mask0 == True:  ###将数值0改为Nan
        deficit_ym.mask(deficit_ym==0,np.nan,inplace = True)
    snsdata = deficit_ym.T
    if detail== True:     ####画每年的曲线
        #snsdata.plot(title = title,linewidth = 3)  #比较不同年份，相同月份  图线为实线
        sns.lineplot(ax = ax1,data=snsdata, palette="tab10", linewidth=3)
        ax1.legend(ncols = legcolsn)
        ax1.axvline(US_deficit.loc[:, column].dropna().index[-1].month + 12-int(startm), ls='--', color='gray',linewidth = 1)
    elif detail == 'mean': ####画前些年的均值
        mean = snsdata.iloc[:,0:-1].mean(axis =1)
        mini = snsdata.iloc[:,0:-1].min(axis =1)
        maxi = snsdata.iloc[:,0:-1].max(axis =1)
        ax1.plot(snsdata.index,snsdata.iloc[:,-1],'r')
        ax1.fill_between(mini.index, mini,maxi, color="b", alpha=0.2)
        ax1.plot(mean.index,mean,'b',linewidth = 1)
        ax1.plot(snsdata.index,snsdata.iloc[:,-2],'g')
        #plt.plot(snsdata.index,snsdata.iloc[:,-1])
        #plt.fill_between(mini.index, mini,maxi, color="b", alpha=0.2)
        #plt.plot(mean.index,mean,linewidth = 1)
        #plt.plot(snsdata.index,snsdata.iloc[:,-2])
        ax1.legend([str(snsdata.columns[-1])+'年',
                    str(snsdata.columns[0]) +'-' + str(snsdata.columns[-2])+'年',
                    '均值',
                    str(snsdata.columns[-2])+'年'], ncols = 2)
    ax1.set_ylabel(ylabel); ax1.set_title(title); 
    return(US_deficit_F,(fig1,ax1))
#####################################################
##########地方政府债务发行见顶##
def monthline(Debt, Debt_pct, colname0=['地方政府债务发行:累计:新增:专项','地方政府债务发行:累计:新增:一般'],
              colname1=['地方政府债务发行:累计:新增:专项','地方政府债务发行:累计:新增:一般'],
              month_n=6, title0='月地方政府新增债务发行累计',
              title1='月地方政府新增债务发行累计同比', savename ='月地方政府新增债务发行累计线图' ,
              start0='2012', start1 = '2012', ylabel0 = '亿元',
              ylabel1 = '%', source = '资料来源：中国财政部，国家金融与发展实验室', anno0 = 'line',
              anno1 = 'line', outputpath='E:\\E\\python_w\\data\\'):
    ####每年固定月份的线图
    fig1, ax1 = figwmarksource1(nrows = 2, hspace = 0.3, source = '资料来源：中国财政部，国家金融与发展实验室')
    #Debt_month = Debt.loc[Debt.index.month==6].to_period('M')
    Debt_month = Debt.loc[Debt.index.month==month_n].to_period('M')
    Debt_pct_month = Debt_pct.loc[Debt_pct.index.month==month_n].to_period('M')
    #plotdata1 = Debt_month.loc['2018':,['地方政府债务发行:累计:新增:专项','地方政府债务发行:累计:新增:一般']]
    plotdata0 = Debt_month.loc[start0:,colname0]
    plotdata0 = plotdata0.sort_values(by=plotdata0.index[-1],axis=1, ascending = False)
    plotdata0.plot(ax = ax1[0])
    ax1[0].set_ylabel(ylabel0)
    plotdata1 = Debt_pct_month.loc[start1:,colname1]
    plotdata1 = plotdata1.sort_values(by=plotdata1.index[-1],axis=1, ascending = False)
    plotdata1.plot(ax = ax1[1])
    ax1[1].set_ylabel(ylabel1)
    ax1[0].set_title('各年1-'+str(plotdata0.index.month[-1]) + title0)
    ax1[1].set_title('各年1-'+str(plotdata1.index.month[-1]) + title1)
    ax1[0].axhline(0, color='gray',linestyle = '--', linewidth = 1)
    ax1[1].axhline(0, color='gray',linestyle = '--', linewidth = 1)
    if anno0 == 'line':
        lineannotate(fig1, ax1[0], plotdata0, arrow = 'yes')
    elif anno0 == 'square':
        lineanno3(fig1, ax1[0], plotdata0, arrow = 'yes')    
    if anno1 == 'line':
        lineannotate(fig1, ax1[1], plotdata1, arrow = 'yes')
    elif anno1 == 'square':
        lineanno3(fig1, ax1[1], plotdata1, arrow = 'yes')
    fig1.savefig(outputpath + r'\\'+ savename+ '.svg', transparent = True,  bbox_inches='tight')
    fig1.savefig(outputpath +  r'\\'+ savename+ '.svg', transparent = True,  bbox_inches='tight')
    return(fig1, ax1)
####################################################################################

####################################################################################################
idx = pd.IndexSlice

##输出目录
#outputpath = r'G:\E\python_w\data'
#outputpath = str(r'G:\E\python_w\data')
#outputpath = str(r'E:\E\python_w\data')

###硬盘符号
#source_drive = r"G:"
#source_drive = r"E:"
##########################################
#########################################
############################################################################################
