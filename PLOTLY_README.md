# Plotly Interactive Dashboard Guide

## 📊 Overview

This guide explains how to create interactive web-based dashboards using Plotly, complementing the existing matplotlib/LaTeX Beamer workflow.

**What's New:**
- ✅ Interactive charts with zoom, pan, and hover tooltips
- ✅ Web-based dashboards (no PDF compilation needed)
- ✅ Mobile-responsive design
- ✅ Easy sharing via HTML files
- ✅ Integrates with existing `hjuw_read_plot.py` data reading functions

## 🚀 Quick Start

### 1. Install Plotly

```bash
pip install plotly pandas numpy
```

### 2. Run the Example

```bash
python example_plotly_dashboard.py
```

This will generate:
- `us_inflation_dashboard.html` - Full multi-chart dashboard
- `simple_inflation_chart.html` - Single chart example

### 3. Open in Browser

Simply double-click the HTML files or open them in any web browser.

## 📁 File Structure

```
python-plot/
├── plotly_viz.py                    # Plotly visualization module
├── example_plotly_dashboard.py      # Example dashboard generator
├── template_dashboard.html          # HTML template
└── PLOTLY_README.md                 # This file
```

## 🎯 Key Features

### Interactive Charts

All charts support:
- **Hover tooltips** - See exact values on hover
- **Zoom** - Click and drag to zoom into data
- **Pan** - Shift+drag to move around
- **Legend toggle** - Click legend items to hide/show series
- **Export** - Download as PNG image (camera icon)
- **Auto-resize** - Responsive to window size

### Available Chart Types

| Function | Description | Use Case |
|----------|-------------|----------|
| `create_line_chart()` | Multi-line time series | CPI, PPI trends |
| `create_dual_axis_chart()` | Two y-axes | Compare CPI vs M2 |
| `create_bar_chart()` | Bar charts | Trade data, comparisons |
| `create_area_chart()` | Stacked area | Component breakdown |
| `create_heatmap()` | Color-coded matrix | Monthly variations |

## 💡 Usage Examples

### Example 1: Basic Line Chart

```python
from plotly_viz import create_line_chart, save_html
import pandas as pd

# Your data (from xwread or other sources)
data = pd.DataFrame({
    'CPI': [2.1, 2.3, 2.5, 2.7],
    'PPI': [1.8, 2.0, 2.2, 2.4]
}, index=pd.date_range('2024-01', periods=4, freq='ME'))

# Create chart
fig = create_line_chart(
    data,
    title='通货膨胀率',
    ylabel='百分比 (%)'
)

# Save as HTML
save_html(fig, 'inflation_chart', outputpath='./')
```

### Example 2: Dual-Axis Chart

```python
from plotly_viz import create_dual_axis_chart

# Compare two different metrics
fig = create_dual_axis_chart(
    cpi_data,          # Left axis
    m2_data,           # Right axis
    title='CPI与M2对比',
    ylabel1='CPI (%)',
    ylabel2='M2 (%)'
)

save_html(fig, 'dual_axis_chart')
```

### Example 3: Complete Dashboard

```python
from plotly_viz import create_dashboard_html

# Dictionary of charts
figures = {
    '消费物价指数': fig_cpi,
    '生产者价格指数': fig_ppi,
    'CPI与M2对比': fig_dual
}

# Create multi-chart dashboard
create_dashboard_html(
    figures,
    title='经济监测报告',
    outputpath='./',
    filename='dashboard'
)
```

## 🔧 Integration with Existing Workflow

### Using with `xwread()` Function

```python
from hjuw_read_plot import xwread, clean_df
from plotly_viz import create_line_chart, create_dashboard_html

# 1. Read data (existing workflow)
filename = r"E:\D\www\macromodels\IECASS\CEIC_macrodata_US.xlsx"
US_CPI, unit = xwread(filename, 'CPIUSA', start='A1', droprowsN=3)

# 2. Clean data
US_CPI = clean_df(US_CPI, Old1='：经季节性调整后', New1='：SA')

# 3. Calculate YoY change
US_CPI_pct = US_CPI.pct_change(12, fill_method=None) * 100

# 4. Create Plotly chart (NEW!)
fig = create_line_chart(
    US_CPI_pct.loc['2022':],
    title='美国CPI同比',
    ylabel='百分比'
)

# 5. Save as interactive HTML
save_html(fig, 'us_cpi_interactive')
```

### Parallel Workflow: Both PDF and Web

You can generate both LaTeX/PDF reports AND web dashboards:

```python
# For PDF report (existing workflow)
fig_mpl, ax = fig1_lines(plotdata, title, ylabel, savename, outputpath)
doc = frame_image1(doc, title, savename + '.pdf', '', source)

# For web dashboard (new workflow)
fig_plotly = create_line_chart(plotdata, title, ylabel)
save_html(fig_plotly, savename + '_interactive')
```

## 🎨 Customization

### Modify Chart Appearance

```python
fig = create_line_chart(data, title, ylabel)

# Update layout
fig.update_layout(
    height=800,
    width=1200,
    template='plotly_dark',  # Dark theme
    font=dict(size=14)
)

# Update line styles
fig.update_traces(
    line=dict(width=4, dash='dot')
)
```

### Add Watermark

```python
from plotly_viz import add_watermark

fig = create_line_chart(data, title, ylabel)
fig = add_watermark(fig, text='SALMON', opacity=0.1)
```

### Custom Colors

```python
fig = create_line_chart(data, title, ylabel)

# Set specific colors
colors = ['#667eea', '#e74c3c', '#27ae60']
for i, trace in enumerate(fig.data):
    trace.line.color = colors[i % len(colors)]
```

## 📱 Responsive Design

All dashboards are mobile-friendly:
- Charts automatically resize
- Touch-friendly controls
- Optimized layout for small screens

Test on mobile by opening the HTML file on your phone.

## 🌐 Deployment Options

### Option 1: Local Files
- Share HTML files directly
- No server needed
- Works offline (with CDN internet required for first load)

### Option 2: Web Server
```bash
# Simple Python server
python -m http.server 8000

# Access at http://localhost:8000
```

### Option 3: GitHub Pages
1. Push HTML files to GitHub repository
2. Enable GitHub Pages in repository settings
3. Share public URL

### Option 4: Cloud Hosting
- Upload to AWS S3, Google Cloud Storage, etc.
- Set up static website hosting
- Share public URL

## 🆚 Plotly vs Matplotlib

| Feature | Matplotlib (Current) | Plotly (New) |
|---------|---------------------|--------------|
| Output | PDF (via LaTeX) | HTML |
| Interactivity | Static | Interactive |
| File size | Small | Larger |
| Quality | Publication-grade | Web-optimized |
| Chinese support | Excellent | Good |
| Sharing | Email PDF | Share link |
| Mobile | Fixed size | Responsive |
| Best for | Formal reports | Online dashboards |

**Recommendation:** Use both!
- PDF reports for formal presentations
- HTML dashboards for interactive exploration

## 🔍 Advanced Features

### 1. Add Annotations

```python
fig.add_annotation(
    x='2024-06-01',
    y=3.5,
    text='重要事件',
    showarrow=True,
    arrowhead=2
)
```

### 2. Add Shapes (Recession Shading)

```python
fig.add_vrect(
    x0='2020-03-01',
    x1='2020-06-01',
    fillcolor='gray',
    opacity=0.2,
    annotation_text='经济衰退'
)
```

### 3. Subplots

```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('CPI', 'PPI', 'M2', '贸易')
)

fig.add_trace(go.Scatter(x=dates, y=cpi), row=1, col=1)
fig.add_trace(go.Scatter(x=dates, y=ppi), row=1, col=2)
# ... add more traces
```

### 4. Custom Hover Templates

```python
fig.update_traces(
    hovertemplate='<b>日期:</b> %{x}<br>' +
                  '<b>数值:</b> %{y:.2f}%<br>' +
                  '<extra></extra>'
)
```

## 🐛 Troubleshooting

### Issue: Chinese characters not displaying

**Solution:** Add font specification in layout
```python
fig.update_layout(
    font=dict(family='SimHei, Microsoft YaHei, Arial')
)
```

### Issue: Charts too large/small

**Solution:** Adjust height and width parameters
```python
fig = create_line_chart(data, title, ylabel, height=600, width=1000)
```

### Issue: HTML file won't open

**Solution:**
- Check file permissions
- Try different browser
- Ensure Plotly CDN is accessible (internet required)

### Issue: Performance slow with large datasets

**Solution:** Downsample data or use Plotly's scattergl for WebGL rendering
```python
go.Scattergl()  # Instead of go.Scatter()
```

## 📚 Additional Resources

### Official Documentation
- Plotly Python: https://plotly.com/python/
- Graph reference: https://plotly.com/python/reference/

### Templates
- `template_dashboard.html` - Standalone HTML template
- `example_plotly_dashboard.py` - Complete example

### Color Schemes
```python
# Built-in Plotly templates
templates = [
    'plotly', 'plotly_white', 'plotly_dark',
    'ggplot2', 'seaborn', 'simple_white'
]

fig.update_layout(template='plotly_dark')
```

## 🤝 Best Practices

1. **Always add titles and labels** - Make charts self-explanatory
2. **Include source attribution** - Add data source in footer
3. **Use consistent colors** - Match your branding/style
4. **Test on multiple devices** - Check desktop, tablet, mobile
5. **Optimize file size** - Don't include unnecessary data
6. **Add watermarks** - Protect your work
7. **Version your dashboards** - Include timestamp/version

## 📝 Example Workflow

Complete workflow from Excel to Web Dashboard:

```python
# 1. Import modules
from hjuw_read_plot import xwread, clean_df
from plotly_viz import *

# 2. Read and process data
data, unit = xwread('data.xlsx', 'Sheet1', start='A1', droprowsN=3)
data = clean_df(data, Old1='prefix:', New1='')
data_pct = data.pct_change(12, fill_method=None) * 100

# 3. Create charts
fig1 = create_line_chart(data_pct, 'CPI同比', '百分比')
fig2 = create_bar_chart(data.tail(12), '最近12个月', '指数')
fig3 = create_heatmap(data.corr(), '相关性矩阵')

# 4. Build dashboard
figures = {
    '趋势分析': fig1,
    '近期数据': fig2,
    '相关性': fig3
}

create_dashboard_html(figures, '经济分析报告', filename='report')

# 5. Open in browser and share!
```

## 🎓 Learning Path

1. **Start simple**: Run `example_plotly_dashboard.py`
2. **Modify template**: Edit `template_dashboard.html`
3. **Create custom chart**: Use `create_line_chart()` with your data
4. **Build dashboard**: Combine multiple charts
5. **Customize styling**: Adjust colors, fonts, layout
6. **Deploy**: Share via web server or cloud

## 💬 Support

For questions or issues:
- Email: hjuw2005@126.com
- Check CLAUDE.md for codebase documentation
- Refer to Plotly official docs

---

**Created**: 2026-01-01
**Version**: 1.0
**Author**: Based on python-plot codebase by 汪红驹

Happy visualizing! 📊✨
