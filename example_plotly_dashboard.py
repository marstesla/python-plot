"""
Example: Creating Interactive Plotly Dashboard for US Economic Data
Demonstrates integration with existing hjuw_read_plot.py data reading functions

使用示例：创建美国经济数据交互式仪表板
"""

import sys
import pandas as pd
import numpy as np
from plotly_viz import *

# If hjuw_read_plot.py functions are available, import them
# Otherwise, use sample data
try:
    from hjuw_read_plot import xwread, clean_df
    USE_REAL_DATA = False  # Set to True when Excel files are available
except ImportError:
    USE_REAL_DATA = False
    print("Note: hjuw_read_plot not available, using sample data")


def generate_sample_data():
    """Generate sample economic data for demonstration"""
    # Create date range
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='ME')

    # Sample CPI data (similar to US CPI structure)
    cpi_data = pd.DataFrame({
        '居民消费价格指数': 100 + np.cumsum(np.random.randn(len(dates)) * 0.3),
        '食品和饮料': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
        '能源': 100 + np.cumsum(np.random.randn(len(dates)) * 2),
        '住房': 100 + np.cumsum(np.random.randn(len(dates)) * 0.2),
        '核心CPI': 100 + np.cumsum(np.random.randn(len(dates)) * 0.25)
    }, index=dates)

    # Calculate YoY percentage change
    cpi_pct = cpi_data.pct_change(12) * 100

    # Sample PPI data
    ppi_data = pd.DataFrame({
        '生产者价格指数': 100 + np.cumsum(np.random.randn(len(dates)) * 0.4),
        '最终需求': 100 + np.cumsum(np.random.randn(len(dates)) * 0.35),
        '制造业': 100 + np.cumsum(np.random.randn(len(dates)) * 0.3),
        '服务业': 100 + np.cumsum(np.random.randn(len(dates)) * 0.2)
    }, index=dates)

    ppi_pct = ppi_data.pct_change(12) * 100

    # Sample M2 data
    m2_data = pd.DataFrame({
        'M2货币供应': 15000 + np.cumsum(np.random.randn(len(dates)) * 100),
        'M1货币供应': 5000 + np.cumsum(np.random.randn(len(dates)) * 50)
    }, index=dates)

    m2_pct = m2_data.pct_change(12) * 100

    # Sample trade data
    trade_data = pd.DataFrame({
        '出口': 200 + np.random.randn(len(dates)) * 20,
        '进口': 250 + np.random.randn(len(dates)) * 25,
        '贸易差额': -50 + np.random.randn(len(dates)) * 15
    }, index=dates)

    return {
        'cpi_data': cpi_data,
        'cpi_pct': cpi_pct.dropna(),
        'ppi_data': ppi_data,
        'ppi_pct': ppi_pct.dropna(),
        'm2_data': m2_data,
        'm2_pct': m2_pct.dropna(),
        'trade_data': trade_data
    }


def load_real_data(source_drive='E:'):
    """
    Load real data using xwread functions
    Requires Excel files to be available
    """
    data = {}

    try:
        # US CPI data
        filename = source_drive + r"\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
        sheetname = 'CPIUSA'
        US_CPI, unit = xwread(filename, sheetname, start='A1', droprowsN=3)
        US_CPI = clean_df(US_CPI, newcolname_0='no change',
                         Old1='：经季节性调整后', New1='：SA')
        US_CPI_pct = US_CPI.pct_change(12, fill_method=None) * 100

        data['cpi_data'] = US_CPI
        data['cpi_pct'] = US_CPI_pct.dropna()

        # US PPI data
        sheetname = 'PPI最终需求中间需求商品分类行业分类'
        US_PPI, unit = xwread(filename, sheetname, start='A1', droprowsN=3, freq='M')
        US_PPI_pct = US_PPI.pct_change(12, fill_method=None) * 100

        data['ppi_data'] = US_PPI
        data['ppi_pct'] = US_PPI_pct.dropna()

        print("Real data loaded successfully!")
    except Exception as e:
        print(f"Error loading real data: {e}")
        print("Falling back to sample data...")
        return generate_sample_data()

    return data


def create_us_inflation_dashboard(outputpath='./'):
    """
    Create comprehensive US inflation dashboard

    Parameters:
    -----------
    outputpath : str
        Output directory for HTML file
    """
    print("Generating US Economic Dashboard...")

    # Load data
    if USE_REAL_DATA:
        data = load_real_data()
    else:
        data = generate_sample_data()

    # Create dictionary to hold all figures
    figures = {}

    # 1. CPI Year-over-Year Change
    print("Creating CPI charts...")
    cpi_recent = data['cpi_pct'].loc['2022':]
    fig_cpi = create_line_chart(
        cpi_recent,
        title='美国消费物价指数（与上年同比）',
        ylabel='百分比 (%)',
        height=500
    )
    fig_cpi = add_watermark(fig_cpi, 'SALMON')
    figures['1. 消费物价指数（CPI）同比变化'] = fig_cpi

    # 2. CPI Index Levels
    cpi_level = data['cpi_data'].loc['2020':]
    fig_cpi_level = create_line_chart(
        cpi_level,
        title='美国消费物价指数水平',
        ylabel='指数 (2020=100)',
        height=500
    )
    figures['2. 消费物价指数水平'] = fig_cpi_level

    # 3. PPI Year-over-Year Change
    print("Creating PPI charts...")
    ppi_recent = data['ppi_pct'].loc['2022':]
    fig_ppi = create_line_chart(
        ppi_recent,
        title='美国生产者价格指数（与上年同比）',
        ylabel='百分比 (%)',
        height=500
    )
    fig_ppi = add_watermark(fig_ppi, 'SALMON')
    figures['3. 生产者价格指数（PPI）同比变化'] = fig_ppi

    # 4. Dual axis: CPI vs M2
    print("Creating dual-axis charts...")
    if 'm2_pct' in data and 'cpi_pct' in data:
        recent_date = '2020'
        m2_recent = data['m2_pct'].loc[recent_date:]
        cpi_core = data['cpi_pct'].loc[recent_date:, ['核心CPI']] if '核心CPI' in data['cpi_pct'].columns else data['cpi_pct'].iloc[:, [0]].loc[recent_date:]

        fig_dual = create_dual_axis_chart(
            cpi_core,
            m2_recent.iloc[:, [0]],
            title='美国CPI与M2货币供应同比对比',
            ylabel1='CPI同比 (%)',
            ylabel2='M2同比 (%)',
            height=500
        )
        figures['4. CPI与M2货币供应对比'] = fig_dual

    # 5. Trade Balance Bar Chart
    print("Creating trade charts...")
    if 'trade_data' in data:
        trade_recent = data['trade_data'].loc['2023':]
        fig_trade = create_bar_chart(
            trade_recent,
            title='美国贸易数据',
            ylabel='十亿美元',
            height=500,
            barmode='group'
        )
        figures['5. 贸易收支'] = fig_trade

    # 6. Inflation Components Heatmap
    print("Creating heatmap...")
    if len(data['cpi_pct']) > 12:
        # Create monthly heatmap for recent year
        heatmap_data = data['cpi_pct'].tail(12).T
        heatmap_data.columns = heatmap_data.columns.strftime('%Y-%m')

        fig_heatmap = create_heatmap(
            heatmap_data,
            title='CPI分项月度同比变化热力图',
            height=400,
            colorscale='RdYlGn_r',
            annotate=True
        )
        figures['6. CPI分项热力图'] = fig_heatmap

    # 7. Stacked Area Chart for CPI Components
    print("Creating area chart...")
    # Select a few key components
    cols_to_plot = data['cpi_data'].columns[:4]  # First 4 columns
    area_data = data['cpi_data'].loc['2022':, cols_to_plot]

    fig_area = create_area_chart(
        area_data,
        title='CPI分项指数堆叠面积图',
        ylabel='指数',
        height=500
    )
    figures['7. CPI分项堆叠面积图'] = fig_area

    # Generate dashboard HTML
    print("Generating dashboard HTML file...")
    output_file = create_dashboard_html(
        figures,
        title='美国经济监测报告 - 通货膨胀分析',
        outputpath=outputpath,
        filename='us_inflation_dashboard'
    )

    print(f"\n{'='*60}")
    print(f"Dashboard created successfully!")
    print(f"File: {output_file}")
    print(f"{'='*60}")
    print(f"\nTotal charts generated: {len(figures)}")
    print("\nTo view:")
    print(f"  Open {output_file} in your web browser")
    print("\nFeatures:")
    print("  ✓ Interactive hover tooltips")
    print("  ✓ Zoom and pan capabilities")
    print("  ✓ Legend toggle (click to hide/show series)")
    print("  ✓ Responsive design (mobile-friendly)")
    print("  ✓ Export as PNG (camera icon)")
    print(f"{'='*60}\n")

    return output_file


def create_simple_example():
    """Create a simple single-chart example"""
    print("Creating simple example...")

    # Generate sample data
    dates = pd.date_range('2020-01', '2024-12', freq='ME')
    data = pd.DataFrame({
        'CPI': 100 + np.cumsum(np.random.randn(len(dates)) * 0.3),
        'PPI': 100 + np.cumsum(np.random.randn(len(dates)) * 0.4),
        '核心CPI': 100 + np.cumsum(np.random.randn(len(dates)) * 0.25)
    }, index=dates)

    data_pct = data.pct_change(12) * 100

    # Create chart
    fig = create_line_chart(
        data_pct.dropna(),
        title='美国通货膨胀率（同比）',
        ylabel='百分比 (%)'
    )

    # Add watermark
    fig = add_watermark(fig)

    # Save as standalone HTML
    save_html(fig, 'simple_inflation_chart', outputpath='./')

    print("Simple example created: simple_inflation_chart.html")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Plotly Interactive Dashboard Generator")
    print("美国经济数据交互式仪表板生成器")
    print("="*60 + "\n")

    # Create the full dashboard
    create_us_inflation_dashboard(outputpath='.')

    # Also create a simple example
    print("\n" + "-"*60 + "\n")
    create_simple_example()

    print("\n✓ All dashboards generated successfully!")
    print("\nNext steps:")
    print("1. Open the HTML files in your browser")
    print("2. Interact with the charts (hover, zoom, pan)")
    print("3. Customize plotly_viz.py for your needs")
    print("4. Integrate with your existing data reading workflow")
