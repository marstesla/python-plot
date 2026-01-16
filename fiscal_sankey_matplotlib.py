"""
US Fiscal Year 2026 Sankey Diagram - Matplotlib Version
Closer match to original Treasury visualization style

This version uses matplotlib for static output matching the original design
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.sankey import Sankey
import numpy as np

# Set font and style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

# =========================
# Data (in billions)
# =========================

receipts = [
    ('Individual Income Taxes', 606),
    ('Social Insurance & Retirement', 409),
    ('Customs Duties', 90),
    ('Corporation Income Taxes', 82),
    ('Excise Taxes', 22),
    ('Estate and Gift Taxes', 8),
    ('Miscellaneous', 8)
]

outlays = [
    ('Social Security', 402),
    ('Net Interest', 270),
    ('National Defense', 267),
    ('Health', 261),
    ('Medicare', 254),
    ('Income Security', 166),
    ('Veterans\' Benefits & Services', 114),
    ('Education', 39),
    ('Transportation', 33),
    ('Other', 21)
]

total_receipts = sum(v for _, v in receipts)  # 1,225
total_outlays = sum(v for _, v in outlays)    # 1,827
deficit = total_outlays - total_receipts       # 602

# =========================
# Create Figure
# =========================

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[], title='')

# Colors matching the original
color_receipts = '#66C2A5'  # Green
color_outlays = '#2C7BB6'   # Teal
color_deficit = '#FC8D62'   # Orange

# =========================
# Build Sankey Diagram
# =========================

# Prepare flows for Sankey
# Receipts (positive inflows)
flows_in = [v for _, v in receipts]
labels_in = [f'{name}\n${v}B' for name, v in receipts]

# Deficit (additional inflow)
flows_in.append(deficit)
labels_in.append(f'Deficit\n${deficit}B')

# Outlays (negative outflows)
flows_out = [-v for _, v in outlays]
labels_out = [f'{name}\n${v}B' for name, v in outlays]

# Combine all flows
all_flows = flows_in + flows_out
all_labels = labels_in + labels_out

# Orientations (0=right, 1=up, -1=down, 2=left)
orientations_in = [0] * len(flows_in)
orientations_out = [0] * len(flows_out)
all_orientations = orientations_in + orientations_out

# Create Sankey
sankey = Sankey(
    ax=ax,
    scale=0.01,
    offset=0.3,
    head_angle=120,
    format='%.0f',
    unit=' B'
)

# Add the main diagram
sankey.add(
    flows=all_flows,
    labels=all_labels,
    orientations=all_orientations,
    pathlengths=[0.25] * len(all_flows),
    trunklength=2.0,
    facecolor=color_receipts,
    edgecolor='none',
    alpha=0.7
)

diagrams = sankey.finish()

# =========================
# Customize appearance
# =========================

# Color code the flows
for i, patch in enumerate(diagrams[0].patches):
    if i < len(receipts):  # Receipt flows
        patch.set_facecolor(color_receipts)
        patch.set_alpha(0.6)
    elif i == len(receipts):  # Deficit flow
        patch.set_facecolor(color_deficit)
        patch.set_alpha(0.8)
    else:  # Outlay flows
        patch.set_facecolor(color_outlays)
        patch.set_alpha(0.6)

# =========================
# Add title and annotations
# =========================

fig.suptitle(
    'Figure 2. Cumulative Receipts, Outlays, and Surplus/Deficit through Fiscal Year 2026',
    fontsize=16,
    fontweight='bold',
    y=0.98
)

plt.text(
    0.5, 0.94,
    'October + November + December 2025 Totals',
    ha='center',
    fontsize=12,
    style='italic',
    transform=fig.transFigure
)

# Add section labels
plt.text(
    0.15, 0.88,
    'Receipts by Source:',
    ha='center',
    fontsize=13,
    fontweight='bold',
    transform=fig.transFigure
)

plt.text(
    0.85, 0.88,
    'Outlays by Function:',
    ha='center',
    fontsize=13,
    fontweight='bold',
    transform=fig.transFigure
)

# Add central info box
box_text = (
    f'Total Receipts\n${total_receipts:,} Billion\n\n'
    f'Total Outlays\n${total_outlays:,} Billion'
)

bbox_props = dict(
    boxstyle='round,pad=0.8',
    facecolor='white',
    edgecolor='black',
    linewidth=2
)

plt.text(
    0.5, 0.75,
    box_text,
    ha='center',
    va='center',
    fontsize=11,
    bbox=bbox_props,
    transform=fig.transFigure
)

# Add deficit box
deficit_bbox = dict(
    boxstyle='round,pad=0.5',
    facecolor=color_deficit,
    edgecolor='darkred',
    linewidth=2
)

plt.text(
    0.5, 0.6,
    f'Deficit\n${deficit:,} Billion',
    ha='center',
    va='center',
    fontsize=11,
    fontweight='bold',
    color='darkred',
    bbox=deficit_bbox,
    transform=fig.transFigure
)

# =========================
# Add legend
# =========================

legend_elements = [
    mpatches.Patch(facecolor=color_receipts, alpha=0.6, label='Receipts'),
    mpatches.Patch(facecolor=color_outlays, alpha=0.6, label='Outlays'),
    mpatches.Patch(facecolor=color_deficit, alpha=0.8, label='Deficit')
]

ax.legend(
    handles=legend_elements,
    loc='lower right',
    fontsize=10,
    frameon=True
)

plt.tight_layout(rect=[0, 0, 1, 0.96])

# =========================
# Save outputs
# =========================

# Save as SVG
plt.savefig('fiscal_sankey_matplotlib.svg', format='svg', dpi=300, bbox_inches='tight')
print("Saved: fiscal_sankey_matplotlib.svg")

# Save as PDF
plt.savefig('fiscal_sankey_matplotlib.pdf', format='pdf', dpi=300, bbox_inches='tight')
print("Saved: fiscal_sankey_matplotlib.pdf")

# Save as PNG (high resolution)
plt.savefig('fiscal_sankey_matplotlib.png', format='png', dpi=300, bbox_inches='tight')
print("Saved: fiscal_sankey_matplotlib.png")

plt.show()

# =========================
# Print summary
# =========================

print("\n" + "="*60)
print("Fiscal Year 2026 Summary (Oct-Dec 2025)")
print("="*60)
print(f"\n{'RECEIPTS':<40} ${total_receipts:>8,} Billion")
print("-"*60)
for name, value in receipts:
    print(f"  {name:<38} ${value:>8,} Billion")

print(f"\n{'OUTLAYS':<40} ${total_outlays:>8,} Billion")
print("-"*60)
for name, value in outlays:
    print(f"  {name:<38} ${value:>8,} Billion")

print("\n" + "="*60)
print(f"{'DEFICIT':<40} ${deficit:>8,} Billion")
print("="*60)
