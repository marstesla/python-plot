"""
US Fiscal Year 2026 Sankey Diagram
Cumulative Receipts, Outlays, and Surplus/Deficit
October + November + December 2025 Totals

Author: Based on Treasury data visualization
Purpose: Recreate fiscal flow Sankey diagram
"""

import plotly.graph_objects as go
import plotly.io as pio

# =========================
# Data from FY 2026 (Oct-Dec 2025)
# =========================

# Receipts by Source (in billions)
receipts = {
    'Individual Income Taxes': 606,
    'Social Insurance & Retirement': 409,
    'Customs Duties': 90,
    'Corporation Income Taxes': 82,
    'Excise Taxes': 22,
    'Estate and Gift Taxes': 8,
    'Miscellaneous': 8
}

# Outlays by Function (in billions)
outlays = {
    'Social Security': 402,
    'Net Interest': 270,
    'National Defense': 267,
    'Health': 261,
    'Medicare': 254,
    'Income Security': 166,
    'Veterans\' Benefits & Services': 114,
    'Education': 39,
    'Transportation': 33,
    'Other': 21
}

total_receipts = sum(receipts.values())  # 1,225
total_outlays = sum(outlays.values())     # 1,827
deficit = total_outlays - total_receipts  # 602

print(f"Total Receipts: ${total_receipts:,} Billion")
print(f"Total Outlays: ${total_outlays:,} Billion")
print(f"Deficit: ${deficit:,} Billion")

# =========================
# Build Sankey Diagram
# =========================

# Node labels (all sources and destinations)
labels = (
    list(receipts.keys()) +           # Receipt sources
    ['Total Receipts'] +              # Central node
    ['Deficit'] +                     # Deficit node
    list(outlays.keys())              # Outlay destinations
)

# Create node indices
receipt_indices = list(range(len(receipts)))
total_receipts_idx = len(receipts)
deficit_idx = len(receipts) + 1
outlay_start_idx = len(receipts) + 2
outlay_indices = list(range(outlay_start_idx, outlay_start_idx + len(outlays)))

# Build flows (source, target, value)
sources = []
targets = []
values = []
colors = []

# Flow from receipts to Total Receipts (GREEN)
for i, (name, value) in enumerate(receipts.items()):
    sources.append(receipt_indices[i])
    targets.append(total_receipts_idx)
    values.append(value)
    colors.append('rgba(102, 194, 165, 0.6)')  # Green

# Flow from Total Receipts to Outlays (TEAL/BLUE)
for i, (name, value) in enumerate(outlays.items()):
    sources.append(total_receipts_idx)
    targets.append(outlay_indices[i])
    values.append(value)
    colors.append('rgba(44, 123, 182, 0.6)')  # Teal

# Flow for Deficit (ORANGE/RED)
# Deficit flows from a virtual source to outlays
sources.append(deficit_idx)
targets.append(total_receipts_idx)
values.append(deficit)
colors.append('rgba(252, 141, 98, 0.8)')  # Orange/red for deficit

# Node colors
node_colors = (
    ['rgba(102, 194, 165, 0.8)'] * len(receipts) +  # Green for receipts
    ['rgba(200, 200, 200, 0.8)'] +                   # Gray for total receipts
    ['rgba(252, 141, 98, 0.9)'] +                    # Orange for deficit
    ['rgba(44, 123, 182, 0.8)'] * len(outlays)       # Teal for outlays
)

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="white", width=2),
        label=labels,
        color=node_colors,
        customdata=[f"${v}B" if i < len(receipts) else
                    f"${list(outlays.values())[i - outlay_start_idx]}B" if i >= outlay_start_idx else
                    f"${deficit}B" if i == deficit_idx else f"${total_receipts}B"
                    for i in range(len(labels))],
        hovertemplate='%{label}<br>$%{customdata}<extra></extra>'
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=colors,
        hovertemplate='%{source.label} → %{target.label}<br>$%{value}B<extra></extra>'
    )
)])

# Update layout
fig.update_layout(
    title={
        'text': (
            '<b>Figure 2. Cumulative Receipts, Outlays, and Surplus/Deficit through Fiscal Year 2026</b><br>'
            '<i>October + November + December 2025 Totals</i>'
        ),
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18, 'family': 'Arial, sans-serif'}
    },
    font=dict(size=12, family='Arial, sans-serif'),
    height=700,
    width=1200,
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        # Total Receipts annotation
        dict(
            x=0.25,
            y=1.05,
            xref='paper',
            yref='paper',
            text='<b>Receipts by Source:</b>',
            showarrow=False,
            font=dict(size=14, family='Arial')
        ),
        # Total Outlays annotation
        dict(
            x=0.75,
            y=1.05,
            xref='paper',
            yref='paper',
            text='<b>Outlays by Function:</b>',
            showarrow=False,
            font=dict(size=14, family='Arial')
        ),
        # Center box with totals
        dict(
            x=0.5,
            y=0.95,
            xref='paper',
            yref='paper',
            text=(
                f'<b>Total Receipts</b><br>${total_receipts:,} Billion<br><br>'
                f'<b>Total Outlays</b><br>${total_outlays:,} Billion<br><br>'
                f'<b style="color: #fc8d62;">Deficit<br>${deficit:,} Billion</b>'
            ),
            showarrow=False,
            font=dict(size=12, family='Arial'),
            bgcolor='white',
            bordercolor='black',
            borderwidth=2,
            borderpad=10
        )
    ]
)

# =========================
# Save as HTML (interactive)
# =========================
fig.write_html('fiscal_sankey_fy2026.html')
print("Saved: fiscal_sankey_fy2026.html")

# =========================
# Save as SVG
# =========================
try:
    fig.write_image('fiscal_sankey_fy2026.svg', format='svg')
    print("Saved: fiscal_sankey_fy2026.svg")
except Exception as e:
    print(f"SVG save failed (need kaleido): {e}")
    print("Install with: pip install kaleido")

# =========================
# Save as PDF
# =========================
try:
    fig.write_image('fiscal_sankey_fy2026.pdf', format='pdf')
    print("Saved: fiscal_sankey_fy2026.pdf")
except Exception as e:
    print(f"PDF save failed (need kaleido): {e}")
    print("Install with: pip install kaleido")

# =========================
# Display (optional)
# =========================
fig.show()

print("\n" + "="*60)
print("Fiscal Flow Summary:")
print("="*60)
print(f"\nReceipts: ${total_receipts:,} Billion")
for name, value in receipts.items():
    print(f"  - {name}: ${value} Billion")

print(f"\nOutlays: ${total_outlays:,} Billion")
for name, value in outlays.items():
    print(f"  - {name}: ${value} Billion")

print(f"\n{'Deficit'}: ${deficit:,} Billion")
print("="*60)
