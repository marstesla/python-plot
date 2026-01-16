# Fiscal Sankey Diagram Generator

## Overview

Two Python scripts to recreate US Treasury-style fiscal flow diagrams showing receipts, outlays, and deficit/surplus using Sankey diagrams.

## 📊 What It Creates

A visualization showing:
- **Left side**: Revenue sources (receipts by category)
- **Right side**: Spending categories (outlays by function)
- **Center**: Flow showing how money moves from receipts to outlays
- **Deficit/Surplus**: Visual representation of budget gap

Based on **FY 2026** data (October-December 2025 cumulative totals):
- Total Receipts: **$1,225 Billion**
- Total Outlays: **$1,827 Billion**
- **Deficit: $602 Billion**

## 🎨 Two Versions Available

### 1. `fiscal_sankey.py` - Interactive Plotly Version

**Best for**: Interactive exploration, web sharing, presentations

**Features**:
- Interactive hover tooltips showing exact values
- Zoom and pan capabilities
- Professional color scheme
- Exports to HTML, SVG, and PDF

**Output files**:
- `fiscal_sankey_fy2026.html` - Interactive web version
- `fiscal_sankey_fy2026.svg` - Vector graphic
- `fiscal_sankey_fy2026.pdf` - Print-ready PDF

### 2. `fiscal_sankey_matplotlib.py` - Static Matplotlib Version

**Best for**: Print publications, reports, static images

**Features**:
- Clean, publication-quality output
- Closer match to original Treasury style
- Customizable fonts and colors
- Multiple export formats

**Output files**:
- `fiscal_sankey_matplotlib.svg` - Vector graphic
- `fiscal_sankey_matplotlib.pdf` - Print-ready PDF
- `fiscal_sankey_matplotlib.png` - High-res raster (300 DPI)

## 🚀 Quick Start

### Installation

```bash
# For Plotly version
pip install plotly pandas numpy

# For matplotlib version
pip install matplotlib numpy

# For image export (SVG/PDF)
pip install kaleido
```

### Run the Scripts

```bash
# Interactive Plotly version
python fiscal_sankey.py

# Static matplotlib version
python fiscal_sankey_matplotlib.py
```

## 📋 Data Structure

### Receipts by Source (in billions)

| Category | Amount |
|----------|--------|
| Individual Income Taxes | $606 |
| Social Insurance & Retirement | $409 |
| Customs Duties | $90 |
| Corporation Income Taxes | $82 |
| Excise Taxes | $22 |
| Estate and Gift Taxes | $8 |
| Miscellaneous | $8 |
| **Total** | **$1,225** |

### Outlays by Function (in billions)

| Category | Amount |
|----------|--------|
| Social Security | $402 |
| Net Interest | $270 |
| National Defense | $267 |
| Health | $261 |
| Medicare | $254 |
| Income Security | $166 |
| Veterans' Benefits & Services | $114 |
| Education | $39 |
| Transportation | $33 |
| Other | $21 |
| **Total** | **$1,827** |

## 🎨 Color Scheme

Matching the original Treasury visualization:

- **Receipts**: `#66C2A5` (Green) - Money coming in
- **Outlays**: `#2C7BB6` (Teal/Blue) - Money going out
- **Deficit**: `#FC8D62` (Orange/Red) - Budget shortfall

## 🔧 Customization

### Update Data

Edit the dictionaries in either script:

```python
# Receipts
receipts = {
    'Individual Income Taxes': 606,
    'Social Insurance & Retirement': 409,
    # ... add or modify categories
}

# Outlays
outlays = {
    'Social Security': 402,
    'Net Interest': 270,
    # ... add or modify categories
}
```

### Change Colors

```python
# Plotly version (fiscal_sankey.py)
colors.append('rgba(102, 194, 165, 0.6)')  # Change RGBA values

# Matplotlib version (fiscal_sankey_matplotlib.py)
color_receipts = '#66C2A5'  # Change hex color
color_outlays = '#2C7BB6'
color_deficit = '#FC8D62'
```

### Adjust Layout

```python
# Plotly version
fig.update_layout(
    height=700,  # Change height
    width=1200,  # Change width
)

# Matplotlib version
fig = plt.figure(figsize=(14, 10))  # Change figure size
```

## 📊 Output Examples

### Plotly Version
- Opens in browser automatically
- Hover over flows to see exact amounts
- Click and drag to explore
- Download as PNG using camera icon

### Matplotlib Version
- High-resolution static images
- Perfect for embedding in reports
- Print-ready quality (300 DPI)

## 🔍 Use Cases

1. **Budget Analysis**: Visualize government revenue vs spending
2. **Policy Presentations**: Show fiscal impact clearly
3. **Economic Reports**: Include in economic analysis documents
4. **Educational Materials**: Teach government finance concepts
5. **Media Graphics**: Create charts for news articles
6. **Research Papers**: Publication-quality fiscal diagrams

## 📈 Integration with Existing Codebase

These scripts integrate well with your existing tools:

```python
from plotly_viz import create_dashboard_html

# Generate fiscal Sankey
# ... (run fiscal_sankey.py code)

# Add to existing dashboard
figures = {
    'Budget Flow': fig_sankey,
    'CPI Trends': fig_cpi,
    'Economic Indicators': fig_indicators
}

create_dashboard_html(figures, 'Economic Analysis Dashboard')
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'plotly'"
**Solution**: `pip install plotly`

### Issue: "Cannot save to PDF/SVG"
**Solution**: `pip install kaleido`

### Issue: Charts look compressed
**Solution**: Increase figure size in layout settings

### Issue: Text overlapping
**Solution**: Adjust `pad` parameter in Sankey node settings

## 📚 Dependencies

### Plotly Version
```
plotly>=5.18.0
pandas>=2.0.0
numpy>=1.24.0
kaleido>=0.2.1  # Optional, for image export
```

### Matplotlib Version
```
matplotlib>=3.7.0
numpy>=1.24.0
```

## 🎓 Understanding Sankey Diagrams

**What is a Sankey diagram?**
A flow diagram where arrow width is proportional to flow quantity. Perfect for showing:
- Budget flows (receipts → outlays)
- Energy flows
- Material flows
- Any resource allocation

**Why use Sankey for fiscal data?**
- ✅ Shows proportions visually
- ✅ Clear flow from sources to uses
- ✅ Easy to spot largest categories
- ✅ Deficit/surplus immediately visible

## 📝 Data Sources

Original data from:
- US Department of Treasury
- Monthly Treasury Statement
- Fiscal Year 2026 (October-December 2025 cumulative)

**Note**: Update the data in the scripts to reflect current fiscal periods.

## 🔄 Future Enhancements

Possible additions:
- [ ] Load data from CSV/Excel files
- [ ] Multi-year comparison
- [ ] Animated fiscal changes over time
- [ ] Breakdown by department
- [ ] State-level fiscal flows
- [ ] Integration with real-time Treasury API

## 💡 Tips

1. **For web sharing**: Use Plotly version, share HTML file
2. **For print**: Use matplotlib version, export as PDF
3. **For presentations**: Use Plotly version, embed in slides
4. **For reports**: Use matplotlib PNG at 300 DPI
5. **Quick preview**: Run Plotly version, opens in browser

## 📧 Support

For questions or improvements:
- Check CLAUDE.md for codebase documentation
- Review PLOTLY_README.md for visualization tips
- Email: hjuw2005@126.com

---

**Created**: 2026-01-15
**Version**: 1.0
**Author**: Based on US Treasury fiscal visualizations

Happy visualizing! 📊💰
