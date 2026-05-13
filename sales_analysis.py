"""
============================================================
FUTURE INTERNS — Data Science & Analytics Internship
Task 1: Business Sales Performance Analytics
Intern  : Shiv Kumar  |  CIN: FIT/MAY26/DS17882
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ── 1. GENERATE DATASET ──────────────────────────────────────────────────────
# (In a real scenario, replace this block with: df = pd.read_csv('your_data.csv'))

np.random.seed(42)
from datetime import datetime, timedelta

products = {
    'Electronics':    ['Wireless Headphones','Smart Watch','Laptop Stand','USB-C Hub','Bluetooth Speaker'],
    'Clothing':       ['Running Shoes','Denim Jacket','Yoga Pants','Casual T-Shirt','Winter Hoodie'],
    'Home & Kitchen': ['Air Fryer','Coffee Maker','Blender','Knife Set','Cutting Board'],
    'Books':          ['Data Science Guide','Python Programming','Business Strategy','Self Help Book','Finance 101'],
    'Sports':         ['Yoga Mat','Resistance Bands','Protein Shaker','Jump Rope','Gym Gloves'],
}
regions = ['North','South','East','West','Central']
price_map = {
    'Wireless Headphones':89,'Smart Watch':149,'Laptop Stand':45,'USB-C Hub':35,'Bluetooth Speaker':65,
    'Running Shoes':75,'Denim Jacket':60,'Yoga Pants':40,'Casual T-Shirt':20,'Winter Hoodie':55,
    'Air Fryer':99,'Coffee Maker':79,'Blender':55,'Knife Set':45,'Cutting Board':25,
    'Data Science Guide':30,'Python Programming':28,'Business Strategy':22,'Self Help Book':18,'Finance 101':24,
    'Yoga Mat':35,'Resistance Bands':20,'Protein Shaker':15,'Jump Rope':12,'Gym Gloves':18,
}

rows = []
start_date = datetime(2024, 1, 1)
for _ in range(2000):
    category = np.random.choice(list(products.keys()), p=[0.30,0.20,0.25,0.10,0.15])
    product  = np.random.choice(products[category])
    region   = np.random.choice(regions, p=[0.25,0.20,0.20,0.20,0.15])
    date     = start_date + timedelta(days=np.random.randint(0, 365))
    qty      = np.random.randint(1, 6)
    price    = round(price_map[product] * np.random.uniform(0.90, 1.10), 2)
    discount = round(np.random.choice([0,0,0,5,10,15], p=[0.5,0.2,0.1,0.1,0.07,0.03]), 2)
    revenue  = round(price * qty * (1 - discount/100), 2)
    cost     = round(revenue * np.random.uniform(0.45, 0.65), 2)
    profit   = round(revenue - cost, 2)
    rows.append({'Date':date,'Product':product,'Category':category,'Region':region,
                 'Quantity':qty,'Unit_Price':price,'Discount_%':discount,
                 'Revenue':revenue,'Cost':cost,'Profit':profit})

df = pd.DataFrame(rows)
df['Month']   = df['Date'].dt.to_period('M')
df['Quarter'] = df['Date'].dt.quarter.map({1:'Q1',2:'Q2',3:'Q3',4:'Q4'})
df.to_csv('sales_data.csv', index=False)
print("✅ Dataset ready — 2,000 transactions across 5 categories and 5 regions.\n")

# ── 2. DATA CLEANING ─────────────────────────────────────────────────────────
print("── Data Cleaning ──")
print(f"  Null values : {df.isnull().sum().sum()}")
print(f"  Duplicates  : {df.duplicated().sum()}")
print(f"  Date range  : {df['Date'].min().date()} → {df['Date'].max().date()}\n")

# ── 3. KEY METRICS ───────────────────────────────────────────────────────────
total_revenue = df['Revenue'].sum()
total_profit  = df['Profit'].sum()
total_orders  = len(df)
avg_order     = df['Revenue'].mean()
profit_margin = total_profit / total_revenue * 100

print("── Key Business Metrics ──")
print(f"  Total Revenue   : ₹{total_revenue:,.2f}")
print(f"  Total Profit    : ₹{total_profit:,.2f}")
print(f"  Profit Margin   : {profit_margin:.1f}%")
print(f"  Total Orders    : {total_orders:,}")
print(f"  Avg Order Value : ₹{avg_order:.2f}\n")

# ── 4. CATEGORY ANALYSIS ─────────────────────────────────────────────────────
print("── Revenue by Category ──")
cat_stats = df.groupby('Category').agg(
    Revenue=('Revenue','sum'),
    Profit=('Profit','sum'),
    Orders=('Revenue','count')
).assign(Margin=lambda x: (x['Profit']/x['Revenue']*100).round(1))
print(cat_stats.sort_values('Revenue', ascending=False).to_string(), "\n")

# ── 5. TOP PRODUCTS ───────────────────────────────────────────────────────────
print("── Top 10 Products by Revenue ──")
top_products = df.groupby('Product')['Revenue'].sum().nlargest(10)
print(top_products.to_string(), "\n")

# ── 6. REGIONAL ANALYSIS ─────────────────────────────────────────────────────
print("── Regional Performance ──")
regional = df.groupby('Region').agg(
    Revenue=('Revenue','sum'),
    Profit=('Profit','sum'),
    Orders=('Revenue','count')
).assign(Margin=lambda x: (x['Profit']/x['Revenue']*100).round(1))
print(regional.sort_values('Revenue', ascending=False).to_string(), "\n")

# ── 7. MONTHLY TREND ─────────────────────────────────────────────────────────
print("── Monthly Revenue Trend ──")
monthly = df.groupby('Month')['Revenue'].sum()
print(monthly.to_string(), "\n")

# ── 8. DASHBOARD PLOT ────────────────────────────────────────────────────────
BG, CARD = '#0F1117', '#1A1D27'
ACCENT1, ACCENT2, ACCENT3, ACCENT4 = '#4F8EF7', '#F7B731', '#2ECC71', '#E74C3C'
TEXT, SUBTEXT = '#E8EAF0', '#8B90A0'
CAT_COLORS = ['#4F8EF7','#F7B731','#2ECC71','#E74C3C','#9B59B6']

plt.rcParams.update({
    'figure.facecolor':BG,'axes.facecolor':CARD,'text.color':TEXT,
    'axes.labelcolor':TEXT,'xtick.color':SUBTEXT,'ytick.color':SUBTEXT,
    'axes.edgecolor':'#2A2D3A','grid.color':'#2A2D3A',
    'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,
})

fig = plt.figure(figsize=(20, 14), facecolor=BG)
gs  = gridspec.GridSpec(4, 4, figure=fig, hspace=0.55, wspace=0.35,
                         top=0.91, bottom=0.06, left=0.05, right=0.97)

# Title
title_ax = fig.add_axes([0, 0.93, 1, 0.07], facecolor='#141720')
title_ax.axis('off')
title_ax.text(0.5, 0.65, 'BUSINESS SALES PERFORMANCE ANALYTICS',
              ha='center', va='center', fontsize=20, fontweight='bold',
              color=TEXT, transform=title_ax.transAxes)
title_ax.text(0.5, 0.18,
              'Fiscal Year 2024  ·  Future Interns  ·  Data Science & Analytics — Shiv Kumar',
              ha='center', va='center', fontsize=9, color=SUBTEXT,
              transform=title_ax.transAxes)
title_ax.axhline(0, color=ACCENT1, linewidth=2, xmin=0.05, xmax=0.95)

# KPI Cards
kpis = [
    ('Total Revenue',   f"₹{total_revenue/1e6:.2f}M",  ACCENT1),
    ('Total Profit',    f"₹{total_profit/1e3:.1f}K",   ACCENT3),
    ('Orders',          f"{total_orders:,}",             ACCENT2),
    ('Avg Order Value', f"₹{avg_order:.0f}",            '#9B59B6'),
]
for i, (label, val, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(CARD)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    rect = FancyBboxPatch((0.04,0.08),0.92,0.84,boxstyle='round,pad=0.02',
                          linewidth=2,edgecolor=color,facecolor='#1E2130',
                          transform=ax.transAxes,clip_on=False)
    ax.add_patch(rect)
    ax.text(0.5,0.72,label,ha='center',va='center',fontsize=9,color=SUBTEXT,transform=ax.transAxes)
    ax.text(0.5,0.38,val, ha='center',va='center',fontsize=22,fontweight='bold',color=color,transform=ax.transAxes)
    ax.axhline(0.08,color=color,linewidth=3,xmin=0.1,xmax=0.9,alpha=0.5)

# Monthly Trend
ax1 = fig.add_subplot(gs[1, :3])
monthly_df = monthly.reset_index()
monthly_df['Month_dt'] = monthly_df['Month'].dt.to_timestamp()
x = range(len(monthly_df))
months_lbl = [m.strftime('%b') for m in monthly_df['Month_dt']]
ax1.fill_between(x, monthly_df['Revenue'], alpha=0.18, color=ACCENT1)
ax1.plot(x, monthly_df['Revenue'], color=ACCENT1, linewidth=2.5, marker='o',
         markersize=5, markerfacecolor=ACCENT2, markeredgecolor=ACCENT1)
ax1.set_xticks(x); ax1.set_xticklabels(months_lbl, fontsize=8)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v/1000:.0f}K'))
ax1.set_title('Monthly Revenue Trend — 2024', color=TEXT, fontsize=11, pad=10, loc='left')
ax1.grid(axis='y', alpha=0.3)
peak_idx = monthly_df['Revenue'].idxmax()
ax1.annotate(f"Peak: {months_lbl[peak_idx]}",
             xy=(peak_idx, monthly_df['Revenue'].iloc[peak_idx]),
             xytext=(peak_idx+0.5, monthly_df['Revenue'].iloc[peak_idx]*1.03),
             color=ACCENT2, fontsize=8, arrowprops=dict(arrowstyle='->', color=ACCENT2))

# Category Donut
ax2 = fig.add_subplot(gs[1, 3])
cat_rev = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
wedges, texts, autotexts = ax2.pie(cat_rev, autopct='%1.0f%%', startangle=90,
    colors=CAT_COLORS, pctdistance=0.75, wedgeprops=dict(width=0.5,edgecolor=BG,linewidth=2))
for at in autotexts: at.set(color=BG, fontsize=7.5, fontweight='bold')
ax2.set_title('Revenue by Category', color=TEXT, fontsize=11, pad=10, loc='left')
ax2.legend(cat_rev.index, loc='lower center', fontsize=7, ncol=2,
           facecolor=CARD, edgecolor='none', labelcolor=TEXT, bbox_to_anchor=(0.5,-0.22))

# Top 10 Products
ax3 = fig.add_subplot(gs[2, :2])
top_prod = df.groupby('Product')['Revenue'].sum().nlargest(10).sort_values()
colors_bar = [ACCENT1 if i >= 7 else ACCENT1+'66' for i in range(10)]
bars = ax3.barh(top_prod.index, top_prod.values, color=colors_bar, height=0.6)
ax3.set_title('Top 10 Products by Revenue', color=TEXT, fontsize=11, pad=10, loc='left')
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v/1000:.0f}K'))
for bar, val in zip(bars, top_prod.values):
    ax3.text(val+200, bar.get_y()+bar.get_height()/2,
             f'₹{val/1000:.1f}K', va='center', color=TEXT, fontsize=7.5)
ax3.grid(axis='x', alpha=0.3)

# Regional Performance
ax4 = fig.add_subplot(gs[2, 2:])
reg = df.groupby('Region').agg(Revenue=('Revenue','sum'),Profit=('Profit','sum')).reset_index()
reg = reg.sort_values('Revenue', ascending=False)
xi = np.arange(len(reg)); w = 0.38
ax4.bar(xi-w/2, reg['Revenue'], width=w, color=ACCENT1, label='Revenue', alpha=0.9)
ax4.bar(xi+w/2, reg['Profit'],  width=w, color=ACCENT3, label='Profit',  alpha=0.9)
ax4.set_xticks(xi); ax4.set_xticklabels(reg['Region'], fontsize=9)
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v/1000:.0f}K'))
ax4.set_title('Revenue & Profit by Region', color=TEXT, fontsize=11, pad=10, loc='left')
ax4.legend(facecolor=CARD, edgecolor='none', labelcolor=TEXT, fontsize=8)
ax4.grid(axis='y', alpha=0.3)

# Profit Margin by Category
ax5 = fig.add_subplot(gs[3, :2])
cat_margin = df.groupby('Category').apply(
    lambda x: x['Profit'].sum()/x['Revenue'].sum()*100).sort_values(ascending=False)
bar_colors = [ACCENT3 if v >= cat_margin.mean() else ACCENT4+'BB' for v in cat_margin]
ax5.bar(cat_margin.index, cat_margin.values, color=bar_colors, width=0.5)
ax5.axhline(cat_margin.mean(), color=ACCENT2, linestyle='--', linewidth=1.5,
            label=f'Avg {cat_margin.mean():.1f}%')
ax5.set_title('Profit Margin % by Category', color=TEXT, fontsize=11, pad=10, loc='left')
ax5.set_ylabel('Margin %', color=SUBTEXT, fontsize=8)
ax5.legend(facecolor=CARD, edgecolor='none', labelcolor=TEXT, fontsize=8)
ax5.grid(axis='y', alpha=0.3)
for i, (cat, val) in enumerate(cat_margin.items()):
    ax5.text(i, val+0.3, f'{val:.1f}%', ha='center', color=TEXT, fontsize=8.5, fontweight='bold')

# Quarterly Revenue by Category
ax6 = fig.add_subplot(gs[3, 2:])
qtr = df.groupby(['Quarter','Category'])['Revenue'].sum().unstack()
qtr.plot(kind='bar', ax=ax6, color=CAT_COLORS, width=0.65, edgecolor=BG)
ax6.set_title('Quarterly Revenue by Category', color=TEXT, fontsize=11, pad=10, loc='left')
ax6.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v/1000:.0f}K'))
ax6.set_xlabel(''); ax6.tick_params(axis='x', rotation=0)
ax6.legend(fontsize=7, facecolor=CARD, edgecolor='none', labelcolor=TEXT,
           loc='upper right', ncol=2)
ax6.grid(axis='y', alpha=0.3)

plt.savefig('sales_dashboard.png', dpi=160, bbox_inches='tight', facecolor=BG)
print("✅ Dashboard saved as sales_dashboard.png")
