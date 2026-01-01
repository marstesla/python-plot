"""
Plotly Visualization Module for Economic Data
Interactive web-based charts complementing the matplotlib/LaTeX workflow

Author: Based on hjuw_read_plot.py patterns
Purpose: Generate interactive HTML dashboards with Plotly
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from datetime import datetime

# Set default template
pio.templates.default = "plotly_white"


def create_line_chart(data, title, ylabel, xlabel='Date',
                      height=600, width=1000, show_legend=True):
    """
    Create interactive line chart from pandas DataFrame

    Parameters:
    -----------
    data : pd.DataFrame
        Time series data with DatetimeIndex
    title : str
        Chart title
    ylabel : str
        Y-axis label
    xlabel : str
        X-axis label (default: 'Date')
    height : int
        Chart height in pixels
    width : int
        Chart width in pixels
    show_legend : bool
        Whether to show legend

    Returns:
    --------
    plotly.graph_objects.Figure
    """
    fig = go.Figure()

    # Add traces for each column
    for col in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[col],
            name=col,
            mode='lines',
            line=dict(width=2.5),
            hovertemplate='%{y:.2f}<extra></extra>'
        ))

    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family='SimHei, Arial, sans-serif')
        ),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        hovermode='x unified',
        height=height,
        width=width,
        showlegend=show_legend,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        ),
        font=dict(family='SimHei, Arial, sans-serif', size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )

    return fig


def create_dual_axis_chart(data1, data2, title, ylabel1, ylabel2,
                           height=600, width=1000):
    """
    Create chart with dual y-axes (similar to twinx_plot)

    Parameters:
    -----------
    data1 : pd.DataFrame or pd.Series
        Data for left y-axis
    data2 : pd.DataFrame or pd.Series
        Data for right y-axis
    title : str
        Chart title
    ylabel1 : str
        Left y-axis label
    ylabel2 : str
        Right y-axis label

    Returns:
    --------
    plotly.graph_objects.Figure
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces for left axis
    if isinstance(data1, pd.DataFrame):
        for col in data1.columns:
            fig.add_trace(
                go.Scatter(x=data1.index, y=data1[col], name=col,
                          line=dict(width=2.5)),
                secondary_y=False
            )
    else:
        fig.add_trace(
            go.Scatter(x=data1.index, y=data1, name=ylabel1,
                      line=dict(width=2.5)),
            secondary_y=False
        )

    # Add traces for right axis
    if isinstance(data2, pd.DataFrame):
        for col in data2.columns:
            fig.add_trace(
                go.Scatter(x=data2.index, y=data2[col], name=col,
                          line=dict(width=2.5, dash='dash')),
                secondary_y=True
            )
    else:
        fig.add_trace(
            go.Scatter(x=data2.index, y=data2, name=ylabel2,
                      line=dict(width=2.5, dash='dash')),
            secondary_y=True
        )

    # Update layout
    fig.update_xaxes(title_text="Date", showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text=ylabel1, secondary_y=False,
                     showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text=ylabel2, secondary_y=True)

    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family='SimHei, Arial')),
        hovermode='x unified',
        height=height,
        width=width,
        font=dict(family='SimHei, Arial, sans-serif', size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig


def create_heatmap(data, title, height=600, width=1000,
                   colorscale='RdYlGn', annotate=True):
    """
    Create interactive heatmap

    Parameters:
    -----------
    data : pd.DataFrame
        Data for heatmap
    title : str
        Chart title
    height : int
        Chart height
    width : int
        Chart width
    colorscale : str
        Plotly colorscale name
    annotate : bool
        Show values in cells

    Returns:
    --------
    plotly.graph_objects.Figure
    """
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=colorscale,
        text=data.values,
        texttemplate='%{text:.2f}' if annotate else None,
        textfont={"size": 10},
        hoverongaps=False,
        hovertemplate='%{y}<br>%{x}<br>Value: %{z:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family='SimHei, Arial')),
        height=height,
        width=width,
        font=dict(family='SimHei, Arial, sans-serif', size=12)
    )

    return fig


def create_bar_chart(data, title, ylabel, orientation='v',
                     height=600, width=1000, barmode='group'):
    """
    Create interactive bar chart

    Parameters:
    -----------
    data : pd.DataFrame
        Bar chart data
    title : str
        Chart title
    ylabel : str
        Y-axis label
    orientation : str
        'v' for vertical, 'h' for horizontal
    height : int
        Chart height
    width : int
        Chart width
    barmode : str
        'group', 'stack', or 'relative'

    Returns:
    --------
    plotly.graph_objects.Figure
    """
    fig = go.Figure()

    for col in data.columns:
        if orientation == 'v':
            fig.add_trace(go.Bar(
                x=data.index,
                y=data[col],
                name=col,
                hovertemplate='%{y:.2f}<extra></extra>'
            ))
        else:
            fig.add_trace(go.Bar(
                y=data.index,
                x=data[col],
                name=col,
                orientation='h',
                hovertemplate='%{x:.2f}<extra></extra>'
            ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family='SimHei, Arial')),
        yaxis_title=ylabel if orientation == 'v' else None,
        xaxis_title=ylabel if orientation == 'h' else None,
        barmode=barmode,
        height=height,
        width=width,
        font=dict(family='SimHei, Arial, sans-serif', size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )

    return fig


def create_area_chart(data, title, ylabel, height=600, width=1000):
    """
    Create stacked area chart

    Parameters:
    -----------
    data : pd.DataFrame
        Time series data
    title : str
        Chart title
    ylabel : str
        Y-axis label

    Returns:
    --------
    plotly.graph_objects.Figure
    """
    fig = go.Figure()

    for col in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[col],
            name=col,
            mode='lines',
            stackgroup='one',
            fillcolor='tonexty',
            line=dict(width=0.5),
            hovertemplate='%{y:.2f}<extra></extra>'
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family='SimHei, Arial')),
        yaxis_title=ylabel,
        hovermode='x unified',
        height=height,
        width=width,
        font=dict(family='SimHei, Arial, sans-serif', size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig


def save_html(fig, filename, outputpath='./'):
    """
    Save Plotly figure as standalone HTML file

    Parameters:
    -----------
    fig : plotly.graph_objects.Figure
        Figure to save
    filename : str
        Output filename (without .html extension)
    outputpath : str
        Output directory path
    """
    filepath = f"{outputpath}/{filename}.html"
    fig.write_html(filepath, include_plotlyjs='cdn')
    print(f"Saved: {filepath}")
    return filepath


def create_dashboard_html(figures_dict, title, outputpath='./',
                          filename='dashboard'):
    """
    Create multi-chart dashboard HTML page

    Parameters:
    -----------
    figures_dict : dict
        Dictionary of {section_title: figure} pairs
    title : str
        Dashboard title
    outputpath : str
        Output directory
    filename : str
        Output filename (without .html)

    Returns:
    --------
    str : filepath
    """
    html_parts = [f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'SimHei', 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .chart-section {{
            margin-bottom: 50px;
            background: #f8f9fa;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}

        .chart-section h2 {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-size: 1.8em;
        }}

        .chart-container {{
            background: white;
            border-radius: 5px;
            padding: 15px;
        }}

        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}

        .timestamp {{
            color: #95a5a6;
            font-size: 0.85em;
            margin-top: 10px;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            header h1 {{
                font-size: 1.8em;
            }}

            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p>经济数据交互式可视化分析</p>
            <p class="timestamp">更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>

        <div class="content">
"""]

    # Add each figure to the dashboard
    for section_title, fig in figures_dict.items():
        div_id = section_title.replace(' ', '_').replace('/', '_')
        html_parts.append(f"""
            <div class="chart-section">
                <h2>{section_title}</h2>
                <div class="chart-container">
                    <div id="{div_id}"></div>
                </div>
            </div>
""")

    html_parts.append("""
        </div>

        <footer>
            <p><strong>资料来源:</strong> CEIC, BEA, BLS, 国家金融与发展实验室</p>
            <p><strong>作者:</strong> 汪红驹 | <strong>邮箱:</strong> hjuw2005@126.com</p>
            <p style="margin-top: 10px; opacity: 0.8;">本报告基于公开数据，仅代表作者个人观点，不构成投资建议。</p>
        </footer>
    </div>

    <script>
""")

    # Add JavaScript to render each figure
    for section_title, fig in figures_dict.items():
        div_id = section_title.replace(' ', '_').replace('/', '_')
        fig_json = fig.to_json()
        html_parts.append(f"""
        var fig_{div_id} = {fig_json};
        Plotly.newPlot('{div_id}', fig_{div_id}.data, fig_{div_id}.layout, {{responsive: true}});
""")

    html_parts.append("""
    </script>
</body>
</html>
""")

    filepath = f"{outputpath}/{filename}.html"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(''.join(html_parts))

    print(f"Dashboard saved: {filepath}")
    return filepath


def add_watermark(fig, text='SALMON', opacity=0.1):
    """
    Add watermark to Plotly figure

    Parameters:
    -----------
    fig : plotly.graph_objects.Figure
        Figure to add watermark to
    text : str
        Watermark text
    opacity : float
        Watermark opacity (0-1)

    Returns:
    --------
    plotly.graph_objects.Figure
    """
    fig.add_annotation(
        text=text,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=80, color="gray", family='Arial Black'),
        opacity=opacity,
        textangle=-30
    )
    return fig


if __name__ == "__main__":
    # Example usage
    print("Plotly visualization module loaded successfully!")
    print("Use functions like create_line_chart(), create_dual_axis_chart(), etc.")
    print("See examples in example_plotly_dashboard.py")
