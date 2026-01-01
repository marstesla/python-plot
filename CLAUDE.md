# CLAUDE.md - AI Assistant Guide for python-plot Repository

## Project Overview

This repository is a Python-based data visualization and report generation system for economic and financial analysis. It automates the workflow of:
1. Reading data from Excel files (.xlsx)
2. Processing and analyzing economic/financial data
3. Creating publication-quality plots using matplotlib
4. Generating LaTeX Beamer presentations
5. Outputting professional PDF reports via XeLaTeX

**Primary Use Case**: Creating macroeconomic monitoring reports (e.g., US inflation, employment, trade data) with automated data processing, visualization, and professional presentation generation.

## Repository Structure

```
python-plot/
├── README.md                              # Project description
├── hjuw_read_plot.py                      # Core utility library (2403 lines)
├── macrobeamertex.py                      # LaTeX Beamer template functions
├── beamer美国经济监测通货膨胀_tex.py       # Example: US inflation report
└── beamer_USeconomy_inflation.pdf         # Example output PDF
```

## Key Files and Their Purposes

### 1. hjuw_read_plot.py (Core Utility Library)
**Size**: 2403 lines
**Purpose**: Comprehensive data reading, processing, and visualization utilities

**Key Functions** (50+ functions, most important listed):
- **Data Reading**:
  - `xwread()` - Read Excel files with CEIC/Wind data format handling
  - `xwread_wind()` - Read Wind financial data
  - `xwread_ceic()` - Read CEIC economic data
  - `pdxl_ceic()` - Pandas Excel reader for CEIC format

- **Data Processing**:
  - `clean_df()` - Clean dataframe column names with regex replacement
  - `csm2m()` - Convert cumulative sum to monthly values
  - `m2csm()` - Convert monthly to cumulative sum
  - `contrib()` - Calculate contribution analysis
  - `sortdf_last()` - Sort dataframe by last row values

- **Plotting Functions**:
  - `fig1_lines()` - Standard multi-line plot with annotations
  - `fig2_lines()` - Two-panel line plots (different y-axes)
  - `figwmarksource1()` - Create figure with watermark and source
  - `lineannotate()` - Annotate line endpoints with values
  - `seasplot()` - Seasonal pattern visualization
  - `bargraph_123()` - Bar chart comparisons
  - `heatmap()` - Heatmap visualization with annotations
  - `treemap()` - Treemap for hierarchical data
  - `twinx_plot()` - Dual y-axis plots

- **Specialized Utilities**:
  - `NBERdate_plot()` - Add NBER recession shading to plots
  - `svg2pdf()` - Convert SVG images to PDF
  - `export_Emf()` - Export plots to EMF format

**Dependencies**:
```python
pandas, numpy, matplotlib, seaborn
xlwings  # Excel interaction
WindPy   # Wind financial data API
pylatex  # LaTeX generation
statsmodels  # Statistical analysis
colorama  # Terminal colors
```

### 2. macrobeamertex.py (LaTeX Beamer Generator)
**Purpose**: Functions for creating LaTeX Beamer presentations using pylatex

**Key Functions**:
- `beamer()` - Initialize Beamer document with Chinese support, themes, and styling
- `frame_plot()` - Add plot to a Beamer frame
- `frame_image1()` - Add image to frame with size constraints
- `lastpart()` - Add disclaimer/contact section
- `lastpartsalmon()` - Customized disclaimer section

**Features**:
- Chinese language support (`ctex` package)
- Custom themes (AnnArbor, seahorse color scheme)
- Watermark support ("SALMON" or "NIFD")
- Automatic table of contents generation
- Navigation symbols disabled
- Figure numbering enabled
- Adjustbox for automatic image sizing

### 3. beamer美国经济监测通货膨胀_tex.py (Example Report Script)
**Purpose**: Complete example of generating US inflation monitoring report

**Data Sources**:
- US CPI (Consumer Price Index) - various categories
- US PPI (Producer Price Index) - by industry/commodity
- PCE Price Index (Personal Consumption Expenditure)
- Import/Export Price Indices
- Agricultural Price Indices
- M1/M2 Money Supply

**Workflow**:
1. Read data from Excel files (`CEIC_macrodata_US.xlsx`)
2. Process and clean data (column name cleaning, frequency conversion)
3. Calculate year-over-year percentage changes
4. Generate multiple visualizations
5. Add plots to LaTeX Beamer presentation
6. Generate .tex file for compilation with XeLaTeX

## Development Workflows

### Standard Data Analysis Workflow

```python
# 1. Read data
data, unit = xwread(filename, sheetname, start='A1', droprowsN=3)

# 2. Clean column names
data = clean_df(data, newcolname_0='no change',
                Old1='unwanted_prefix:', New1='')

# 3. Calculate changes
data_pct = data.pct_change(12, fill_method=None) * 100  # YoY %

# 4. Create visualization
fig, ax = fig1_lines(plotdata, title, ylabel, savename, outputpath,
                     lgncols=2, figsize=(9, 6),
                     source='资料来源：BEA,国家金融与发展实验室')

# 5. Add to Beamer presentation
doc = frame_image1(doc, title, savename + '.pdf', '',
                   source, width=r'0.8\textwidth', height=r'0.8\textheight')
```

### Creating a New Report

```python
# 1. Import libraries
from macrobeamertex import *
import sys
sys.path.append(r'E:\E\python_w\')
from hjuw_read_plot import *
plt.ioff()  # Turn off interactive mode

# 2. Initialize Beamer document
doc = beamer(fname, title='Report Title', subtitle='Subtitle')

# 3. Add sections
section = Section('Section Name')
doc.append(section)

# 4. Process data and add frames
# ... (data processing code)
doc = frame_image1(doc, frame_title, image_file, annotation, source)

# 5. Add disclaimer
lastpartsalmon(doc, outputname='output_filename')

# 6. Generate TEX file (manual PDF compilation required)
```

### Manual PDF Compilation
After generating .tex file:
1. Open in MiKTeX
2. Run: XeLaTeX + MakeIndex + BibTeX (twice for TOC and references)
3. Output: PDF file

## Code Conventions

### File Naming
- Python scripts: `descriptive_name.py` or Chinese names (UTF-8 supported)
- Image files for LaTeX: **Never use underscore `_`** in filenames
  - Reason: LaTeX treats `_` as subscript command, causing errors
  - Use camelCase or hyphens instead

### Data Processing Patterns

1. **Reading Excel Data**:
   ```python
   data, unit = xwread(filename, sheetname, start='A1', droprowsN=3, freq='M')
   ```
   - Always returns data and unit columns separately
   - `droprowsN` removes header rows
   - `freq='M'` for monthly, 'Q' for quarterly

2. **Column Name Cleaning**:
   ```python
   data = clean_df(data, newcolname_0='no change',
                   Old1='prefix:', New1='')
   ```
   - Use regex patterns to clean column names
   - `newcolname_0='no change'` keeps first column name

3. **Time Series Analysis**:
   ```python
   # Year-over-year change
   data_pct = data.pct_change(12, fill_method=None) * 100

   # Month-over-month
   data_pct1 = data.pct_change(1, fill_method=None) * 100
   ```

4. **Handling Missing Data**:
   ```python
   # Forward interpolation
   data.interpolate(method='linear', axis=0,
                   limit=None, limit_direction='forward', inplace=True)
   ```

### LaTeX/Beamer Conventions

1. **Line Endings**: Add `%` after lines ending with `{` or `}` to prevent vbox overfull warnings

2. **Image Insertion**:
   ```python
   # Use adjustbox for automatic sizing
   doc.append(NoEscape(r'\includegraphics[max size={0.6\textwidth}{0.6\textheight}]{image.pdf}'))
   ```

3. **Chinese Section Labels**: Modified `pylatex/section.py` line 27→28 to prevent duplicate `\label{sec:}` for Chinese sections

### Matplotlib Configuration

```python
# Must set for Chinese characters
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['savefig.dpi'] = 600
mpl.rcParams['lines.linewidth'] = 3

# Turn off interactive mode for batch processing
plt.ioff()
plt.close()  # Close figures to free memory
```

## Important Dependencies and Setup

### Required Packages
```bash
pip install pandas numpy matplotlib seaborn
pip install xlwings openpyxl
pip install pylatex
pip install statsmodels scipy
pip install colorama
pip install WindPy  # For Wind financial data
```

### External Software
- **MiKTeX**: Required for LaTeX compilation
- **XeLaTeX**: For Chinese character support
- **Microsoft Excel**: For xlwings functionality

### Data Sources
- **CEIC**: Economic data database
- **Wind**: Financial data API (中国)
- **BEA**: US Bureau of Economic Analysis
- **BLS**: US Bureau of Labor Statistics

### Critical File Paths
- Data files typically in: `E:\D\www\macromodels\IECASS\`
- Output path: `E:\E\python_w\data\`
- Image path for LaTeX: `E:/E/python_w/data/`
- Python packages: `C:\Python310\Lib\site-packages\`

**Note**: These paths are Windows-specific and hardcoded. May need adjustment for different environments.

## AI Assistant Guidelines

### When Modifying Code

1. **Preserve Chinese Characters**: This codebase extensively uses Chinese for:
   - Column names (e.g., '居民消费价格指数')
   - Plot titles and labels
   - Report section names
   - Do NOT translate or remove these

2. **File Path Handling**:
   - Be aware of Windows-style paths (`E:\`, `C:\`)
   - Distinguish between LaTeX paths (forward slashes) and Python paths (backslashes)
   - Use raw strings `r"path"` for Windows paths

3. **Data Processing**:
   - Always check data frequency (M=monthly, Q=quarterly, D=daily)
   - Verify time series index after resampling
   - Handle NaN values explicitly (don't assume dropna)

4. **Plot Generation**:
   - Close plots with `plt.close()` after saving to prevent memory issues
   - Use `plt.ioff()` at start of scripts for batch processing
   - Include source attribution in all plots

5. **LaTeX Generation**:
   - Escape special LaTeX characters in dynamic content
   - Use `NoEscape()` for raw LaTeX commands
   - Test image filenames for underscores before using

### Common Debugging Patterns

1. **Excel Reading Issues**:
   - Check `droprowsN` matches actual header rows
   - Verify `start` cell reference (e.g., 'A1', 'A2')
   - Ensure Excel file is closed before reading with xlwings

2. **LaTeX Compilation Errors**:
   - Check for `_` in image filenames → rename files
   - Verify Chinese package (`ctex`) is installed
   - Ensure image files exist in specified paths

3. **Plot Display Issues**:
   - Chinese characters not showing → check `mpl.rcParams['font.sans-serif']`
   - Negative signs as boxes → set `axes.unicode_minus = False`
   - Plots not appearing → check interactive mode with `mpl.is_interactive()`

### Adding New Features

When adding new economic indicators:
1. Follow existing data reading patterns
2. Create corresponding plotting functions
3. Add to appropriate Beamer section
4. Document data source and frequency
5. Include both level and percentage change plots
6. Add source attribution

When creating new plots:
1. Use existing plotting functions as templates
2. Include watermark and source
3. Save as PDF for LaTeX inclusion
4. Close figure after saving
5. Return figure and axis objects for flexibility

## Performance Considerations

1. **Large Data Files**: `hjuw_read_plot.py` is 2403 lines
   - When reading, use line limits if not modifying
   - Search for specific functions using grep

2. **Memory Management**:
   - Close matplotlib figures: `plt.close()`
   - Use `plt.ioff()` to prevent display overhead
   - Process data in chunks for very large datasets

3. **Batch Processing**:
   - Multiple reports can be generated in sequence
   - Turn off interactive mode
   - Generate all .tex files first, then batch compile PDFs

## Testing Approach

### Data Integrity Tests
- Verify data read correctly: check shape, dtypes
- Confirm time index is DatetimeIndex
- Validate calculations (spot check percentage changes)

### Visualization Tests
- Generate sample plots to verify formatting
- Check Chinese character rendering
- Confirm legends and labels are readable

### LaTeX Generation Tests
- Generate .tex file and inspect manually
- Compile to PDF to catch LaTeX errors
- Verify images are included correctly

## Version History (from git log)

```
4e19326 Add additional instructions to README
e72ec27 Add project features to README
5d3364d Add beamer_USeconomy_inflation.pdf
0c9adb8 Add beamer美国经济监测通货膨胀_tex.py
672c87e Add macrobeamertex.py
c865e18 Add hjuw_read_plot.py
```

## Contact and Attribution

- **Author**: 汪红驹 (Wang Hongju)
- **Email**: hjuw2005@126.com
- **Institution**: 中国社科院国家金融与发展实验室 (NIFD - National Institution for Finance & Development)
- **Watermark**: Recent work uses "SALMON" watermark

## Quick Reference

### Most Commonly Used Functions

```python
# Data reading
xwread(filename, sheetname, start='A1', droprowsN=3)

# Data cleaning
clean_df(df, Old1='prefix:', New1='')

# Basic line plot
fig1_lines(data, title, ylabel, savename, outputpath)

# Beamer document
doc = beamer(fname, title='Title', subtitle='Subtitle')
doc = frame_image1(doc, title, image_file, annotation, source)
lastpartsalmon(doc, outputname='filename')
```

### File Extensions
- `.py` - Python scripts
- `.xlsx` - Excel data files
- `.pdf` - Output reports and images for LaTeX
- `.tex` - Generated LaTeX source
- `.svg` - Vector graphics (converted to PDF for LaTeX)

---

**Last Updated**: 2026-01-01
**For Claude Code Assistants**: This guide provides context for understanding and modifying the python-plot codebase. Always preserve Chinese language content and respect existing data processing patterns.
