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

##############with matplotlib ################################
import numpy as np
import os, glob
from pylatex import Document, Section, Subsection, Tabular, Command
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex import PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Itemize, Hyperref, Package
from pylatex.utils import italic, bold, NoEscape, escape_latex
import os
import pandas as pd
import matplotlib
#matplotlib.use('Agg')  # Not to use X server. For TravisCI.   ####这一行使画图不显示
import matplotlib.pyplot as plt  # noqa


# import 汪红驹编写的读写、绘图函数， 存放于C:\Python39\Lib\site-packages\hjuw_read_plot.py
import sys
#sys.path.append(source_drive + '\\E\\python_w\\')   #添加系统搜索路径

#from hjuw_read_plot.py import *
from hjuw_read_plot import *
##关闭interactive mode
plt.ioff()
####################################################################################
def beamer(fname, title = '全球宏观经济监测报告系列', subtitle = '美国劳动市场'):
    #geometry_options = {"right": "2cm", "left": "2cm"}
    #geometry_options = {"tmargin": "1cm", "lmargin": "1cm", "margin": "1cm"}
    #doc = Document(fname,documentclass='article', geometry_options=geometry_options)
    #doc = Document(fname,documentclass='beamer', geometry_options=geometry_options)
    doc = Document(fname,documentclass='beamer')
    doc.packages.append(Package("enumerate"))
    doc.packages.append(Package("multirow"))
    doc.packages.append(Package("ctex"))
    doc.packages.append(Package("tikz"))
    doc.packages.append(Package("graphicx"))
    doc.packages.append(Package("adjustbox",options='Export'))    ##\usepackage[Export]{adjustbox}
    doc.packages.append(Package("bbding"))                 # % 一些特殊符号
    doc.packages.append(Package("ctex"))
    doc.packages.append(Package("pdfpages"))               # includegraphics  pdf  才能准确
    #doc.packages.append(Package("svg"))
    #doc.packages.append(Package("svg-extract"))  #-被编译成{-} 出错  ###\usepackage{svg-extract}
    #doc.append(NoEscape(r'\usepackage{svg-extract}'))   ##也会出错
    doc.packages.append(Package("relsize"))
    doc.packages.append(Package("caption"))       #图表标题
    doc.packages.append(Package("subcaption"))
    doc.append(NoEscape(r'\setbeamertemplate{caption}[numbered]')) #% set captions with numbers,beamer caption without d number by default
    doc.packages.append(Package("url"))
    doc.packages.append(Package("cite"))                    # 支持引用
    doc.append(NoEscape(r'\renewcommand{\UrlFont}{\small\tt}'))
    doc.packages.append(Package("hyperref"))
    #doc.packages.append(Package("xwatermark",options = 'printwatermark'))
    #doc.append(NoEscape(r'\newwatermark[allpages,fontfamily=bch,color=cyan!5,angle=60,scale=7,xpos=-40,ypos=25]{CMEM}'))
    #doc.append(NoEscape(r'\hypersetup{backref,  breaklinks=true, pdftex,raiselinks=false}'))  #已经设定
    #doc.append(NoEscape(r'\graphicspath{{E:/E/python_w/data/image_pdf/}}'))    #pdf image path
    doc.append(NoEscape(r'\graphicspath{{E:/E/python_w/data/}}'))    #pdf image path
    #doc.append(NoEscape(r'\svgpath{{svg/}{E:/E/python_w/data/}}'))
    #doc.append(NoEscape(r'\svgsetup{clean=true}'))
    doc.append(NoEscape(r'\setbeamertemplate{navigation symbols}{} %不显示导航栏符号'))
    #doc.append(NoEscape(r'\setbeamertemplate{footline}[frame number]  %只显示页码'))
    #doc.preamble.append(Command('usetheme', 'boxes'))   #类似  default
    #doc.append(NoEscape(r'\newcommand{\plotstandard}[1]{\centerline{\includegraphics[height=4in]{#1}}}'))  ##新定义插入4in height 图片，\plotstandard{myFile.pdf}
    ###选择主题，不选，白板
    #doc.preamble.append(Command('usetheme', 'Boadilla'))
    #doc.preamble.append(Command('usetheme', 'Madrid'))
    #doc.preamble.append(Command('usetheme', 'Berlin'))
    #doc.preamble.append(Command('usetheme', 'CambridgeUS'))
    doc.preamble.append(Command('usetheme', 'AnnArbor'))
    #doc.preamble.append(Command('usetheme', 'Pittsburgh'))
    #doc.preamble.append(Command('usecolortheme', 'whale'))          #蓝色
    doc.preamble.append(Command('usecolortheme', 'seahorse'))        #灰色
    #doc.preamble.append(Command('usecolortheme', 'wolverine'))      #黄色
    #doc.preamble.append(Command('usecolortheme', 'crane'))
    #doc.preamble.append(Command("newcommand{plotstandard}[1]{\centerline{\includegraphics[height=4in]{#1}}}"))  ##
    #% Title page details:
    #doc.preamble.append(Command('title', '全球宏观经济监测报告系列'))
    #doc.preamble.append(Command('subtitle', '中国货币监测'))
    doc.append(NoEscape(r'\title{' + title + '}'))
    doc.append(NoEscape(r'\subtitle{' + subtitle + '}'))
    doc.preamble.append(Command('author', '汪红驹'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    #doc.preamble.append(Command('institute', '中国社科院国家金融与发展实验室'))
    ####加logo，位置由theme决定，一般在右下角
    #doc.append(NoEscape(r'\logo{\large \LaTeX{}}'))
    #doc.append(NoEscape(r'\logo{\large NIFD'))
    #doc.append(NoEscape(r'\logo{\includegraphics[width=3cm]{.//国家金融发展实验室模板///实验室logo.png}}'))
    ####加logo在右上角
    #% Load TikZ
    #doc.append(NoEscape(r'''
    #    \logo{ 
    #    \begin{tikzpicture}[overlay,remember picture]
    #    \node[left=0.2cm] at (current page.30){    %   ###中心出发，东北30度方向，右上角
    #        \includegraphics[width=3cm]{.//国家金融发展实验室模板///实验室logo.png}
    #    };
    #    \end{tikzpicture}
    #    }%
    #'''))
    
    #% global background must be put in the preamble
    ###背景图用下一语句
    #doc.append(NoEscape(r'\setbeamertemplate{background canvas}{\includegraphics[width=\paperwidth, height=\paperheight]{.//国家金融发展实验室模板///实验室水印模板宽图.png}}'))    
    #doc.append(NoEscape(r'\setbeamertemplate{background canvas}{\includegraphics[width=\paperwidth, height=\paperheight]{.//国家金融发展实验室模板///实验室背景.png}}'))    
    
    #doc.packages.append(Package("background"))      #水印，不能显示
    #doc.append(NoEscape(r'\backgroundsetup{contents=NFID,color=blue!20,scale=5,opacity=0.2}'))
    #doc.packages.append(Package("xwatermark",options='printwatermark'))
    #doc.append(NoEscape(r'\newwatermark[allpages,fontfamily=bch,color=cyan!5,angle=60,scale=7,xpos=-40,ypos=25]{CMEM}'))
    doc.packages.append(Package("draftwatermark"))
    #doc.append(NoEscape(r'\SetWatermarkText{NIFD}'))
    doc.append(NoEscape(r'\SetWatermarkText{SALMON}'))
    doc.append(NoEscape(r'\SetWatermarkLightness{0.9}'))
    doc.append(NoEscape(r'\SetWatermarkScale{0.6}'))
    
    doc.append(NoEscape(r'\setbeamercolor{background canvas}{bg=}'))  ###%transparent canvas         
    #doc.preamble.append(Command('setbeamertemplate', options= 'navigation symbols',arguments=''))
    #doc.preamble.append(Command('setbeamertemplate', options = 'footline',arguments='frame number'))
    doc.append(NoEscape(r'\kaishu'))   
    # Background image (local and global options)
    #  % global background must be put in the preamble
    #doc.append(NoEscape(r'\setbeamertemplate{background}'
    #                    r'{\includegraphics[width=\paperwidth,height=\paperheight]{background.jpg}}'))
    ####emf图片做背景不行
    #doc.append(NoEscape(r'\setbeamertemplate{background}'
    #                    r'{\includegraphics[width=\paperwidth,height=\paperheight]{financelogo.emf}}'))
    
         
    #doc.append(NoEscape(r'\maketitle'))
    doc.append(NoEscape(r'''
    \AtBeginSubsection[]
    {%                                         
      \begin{frame}<beamer>{目录}%
        \tableofcontents[currentsection,currentsubsection]
      \end{frame}%
    }%
    % If you wish to uncover everything in a step-wise fashion, uncomment
    % the following command:
    %\beamerdefaultoverlayspecification{<+->}%
    \begin{frame}{}%     #加背景水印
       \titlepage
    \end{frame}%
    
    % Remove logo from the next slides
    %\logo{}

    \begin{frame}{目录}%
        \tableofcontents
        % You might wish to add the option [pausesections]
    \end{frame}%
    '''))
        
    #doc.append(NoEscape(r'\begin{frame}{介绍}'))
    #doc.append('Introduction.')
    #doc.append(NoEscape(r'\end{frame}'))

    return(doc)

def frame_plot(doc, frame_title, annotation,
                source, width =  r'0.7\textwidth', *args, **kwargs):
    doc.append(NoEscape(r'\begin{frame}{' +frame_title + '}'))
    doc.append(NoEscape(annotation))
    with doc.create(Figure(position='htbp')) as plot:
        plot.add_plot(width=NoEscape(width),*args, **kwargs)
        plot.add_caption(f'资料来源： {source}')
        #doc.append(NoEscape(r'\flushleft\footnotesize'    ####这是一页的脚注
        #                    r'{资料来源: ' + source +'}'))
        
    doc.append(NoEscape(r'\end{frame}'))
    return(doc)
def frame_image(doc, frame_title, image, annotation, 
                source, height = r'4in',*args, **kwargs):
    doc.append(NoEscape(r'\begin{frame}{'+ frame_title +'}'))
    doc.append(NoEscape(annotation))
    with doc.create(Figure(position='htbp')) as graph:
        graph.add_image(image, width=NoEscape(width),*args, **kwargs)
        #graph.add_image(image, width=NoEscape(width),*args, **kwargs)
        #graph.add_caption(f'资料来源： {source}')
        #doc.append(NoEscape(r'\flushleft\footnotesize'    ####这是一页的脚注
        #                    r'{资料来源: ' + source +'}'))
                
    doc.append(NoEscape(r'\end{frame}'))
    return(doc)

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

    

def frame_image2(doc, frame_title, image, annotation,  source):
    doc.append(NoEscape(r'''
    \begin{frame}{全球疫情}
    \begin{figure}[htp]                    % here, top, or new page
        \centering
            %\caption{全球疫情}
            #\includegraphics[max size={0.6\textwidth}{0.6\textheight}]{CPI分类商品价格变化.pdf}%
            \includegraphics[scale=0.6]{全球疫情.pdf}
        %   \label{fig:CEICOMP05}
            \flushleft\footnotesize{资料来源: 中国社科院国家金融与发展实验室}
    \end{figure}
    6月份以来，全球疫情新增人数已大幅下降
    \end{frame}
    '''))
    return(doc)


def lastpart(doc, outputname = 'beamer_USeconomy' ):
    
    ####结束页，不要用section，否则显示在目录
    with doc.create(Section('免责声明')):
        doc.append(NoEscape(r'''
        \begin{frame}{机构免责声明}%
        \begin{block}{国家金融与发展实验室}%
        国家金融实验室是国家智库
        
        \end{block}%
        \begin{block}{免责声明}%
        本报告基于公开数据，欢迎联系作者，完善报告。仅代表作者个人观点，不代表机构观点。本报告不构成投资建议。
        \end{block}%
        \begin{block}{报告联系人}%
        汪红驹，hjuw2005@126.com, 13241948068
        \end{block}%
        \end{frame}%'''))

def lastpartsalmon(doc, outputname = 'beamer_USeconomy' ):
    
    ####结束页，不要用section，否则显示在目录
    with doc.create(Section('免责声明')):
        doc.append(NoEscape(r'''
        \begin{frame}{机构免责声明}%
        \begin{block}{Salmon}%
        Salmon 
        
        \end{block}%
        \begin{block}{免责声明}%
        本报告基于公开数据，欢迎联系作者，完善报告。仅代表作者个人观点，不代表机构观点。本报告不构成投资建议。
        \end{block}%
        \begin{block}{报告联系人}%
        汪红驹，hjuw2005@126.com, 13241948068
        \end{block}%
        \end{frame}%'''))
        
    ###############################################
    
    ######################################################
    #############output pdf###############
    #outputname = 'beamer_USeconomy'   #
    #doc.generate_pdf(outputname,compiler='XeLaTeX', clean_tex=False)
    doc.generate_tex(outputname)  ##生成.tex 文件, 位于E:\E\python_w
    #用MIKtex 打开，用  xelatex+MakeIndex + BibTex 运行两次，生成目录和引用
    '''
    ###os.system 运行后得不到 pdf文件
    filePath = outputname + '.pdf'
    try:
        os.unlink(filePath)                  ###先删除原有文件
        #os.remove(filepath)
    except:
        print("Error while deleting file ", filePath)
    os.system(f'xeltx0.bat {outputname}.tex') ####
    '''
    ####手动打开Miktex， 打开  beamer_industry.tex , 用  xelatex+MakeIndex + BibTex
