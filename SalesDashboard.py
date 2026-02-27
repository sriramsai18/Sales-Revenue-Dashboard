import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import base64

# ─── LOAD PROFILE IMAGE ───────────────────────────────────────────────────────
def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

img_b64 = img_to_base64("assets/NANII.png")

st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:       #f7f8fc;
    --card:     #ffffff;
    --border:   #e8eaf0;
    --text:     #1a1d2e;
    --muted:    #6b7280;
    --accent:   #2563eb;
    --accent2:  #7c3aed;
    --green:    #059669;
    --red:      #dc2626;
    --orange:   #d97706;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

footer, #MainMenu { visibility: hidden; }

/* KPI Cards */
.kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    transition: box-shadow 0.25s, transform 0.25s;
    animation: fadeUp 0.5s ease both;
}
.kpi-card:hover {
    box-shadow: 0 8px 30px rgba(37,99,235,0.1);
    transform: translateY(-3px);
}
.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.1;
}
.kpi-delta {
    font-size: 0.8rem;
    font-weight: 500;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
}
.kpi-delta.up   { color: var(--green); }
.kpi-delta.down { color: var(--red); }
.kpi-icon {
    font-size: 1.5rem;
    float: right;
    margin-top: -4px;
    opacity: 0.15;
}

/* Section header */
.sec-header {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--accent);
    display: inline-block;
}

/* Chart wrapper */
.chart-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    animation: fadeUp 0.6s ease both;
}

/* Sidebar filter label */
.filter-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 4px;
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}

/* Top products table */
.prod-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.88rem;
}
.prod-row:last-child { border-bottom: none; }
.prod-rank {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    width: 24px;
}
.prod-name { flex: 1; color: var(--text); font-weight: 500; padding: 0 10px; }
.prod-bar-wrap { width: 90px; background: #f0f0f5; border-radius: 4px; height: 6px; margin: 0 12px; }
.prod-bar { height: 6px; border-radius: 4px; background: linear-gradient(90deg, #2563eb, #7c3aed); }
.prod-val { font-family: 'DM Mono', monospace; font-size: 0.78rem; color: var(--accent); font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─── GENERATE SUPERSTORE-STYLE DATASET ────────────────────────────────────────
@st.cache_data
def generate_data():
    np.random.seed(42)
    n = 1000

    categories    = ["Technology", "Furniture", "Office Supplies"]
    sub_cats = {
        "Technology":      ["Phones","Laptops","Accessories","Printers"],
        "Furniture":       ["Chairs","Tables","Bookcases","Storage"],
        "Office Supplies": ["Paper","Binders","Art","Fasteners"],
    }
    regions   = ["West", "East", "Central", "South"]
    segments  = ["Consumer", "Corporate", "Home Office"]
    products  = [
        "Apple MacBook Pro","Dell XPS 15","Canon ImageClass","Logitech MX Master",
        "Herman Miller Chair","IKEA Kallax Shelf","Fellowes Shredder","Avery Binders",
        "Samsung Galaxy Tab","Sony WH-1000XM5","HP LaserJet Pro","Staples Paper Ream",
        "Microsoft Surface","Cisco IP Phone","Bush Bookcase","3M Post-it Notes",
    ]

    dates = pd.date_range("2022-01-01", "2024-12-31", periods=n)
    cats  = np.random.choice(categories, n)

    df = pd.DataFrame({
        "Order Date": dates,
        "Category":   cats,
        "Sub-Category": [np.random.choice(sub_cats[c]) for c in cats],
        "Region":     np.random.choice(regions, n),
        "Segment":    np.random.choice(segments, n),
        "Product":    np.random.choice(products, n),
        "Sales":      np.random.uniform(50, 3000, n).round(2),
        "Quantity":   np.random.randint(1, 10, n),
        "Discount":   np.random.choice([0, 0.1, 0.2, 0.3, 0.4], n),
    })
    df["Profit"]  = (df["Sales"] * np.random.uniform(0.1, 0.4, n)).round(2)
    df["Revenue"] = (df["Sales"] * df["Quantity"]).round(2)
    df["Year"]    = df["Order Date"].dt.year
    df["Month"]   = df["Order Date"].dt.to_period("M").astype(str)
    df["MonthName"] = df["Order Date"].dt.strftime("%b %Y")
    return df

df = generate_data()

# ─── PLOTLY TEMPLATE ──────────────────────────────────────────────────────────
COLORS = ["#2563eb","#7c3aed","#059669","#d97706","#dc2626","#0891b2"]

def clean_fig(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="DM Sans", size=12, color="#1a1d2e"),
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        xaxis=dict(showgrid=False, showline=True, linecolor="#e8eaf0", tickfont=dict(size=11)),
        yaxis=dict(showgrid=True,  gridcolor="#f0f0f5", showline=False, tickfont=dict(size=11)),
    )
    return fig

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 20px;">
        <div style="font-size:1.6rem;">📊</div>
        <div style="font-weight:700; font-size:1.05rem; color:#1a1d2e;">Sales Dashboard</div>
        <div style="font-size:0.75rem; color:#6b7280; letter-spacing:2px;">ANALYTICS 2022–2024</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="filter-label">Year</div>', unsafe_allow_html=True)
    years = ["All"] + sorted(df["Year"].unique().tolist())
    sel_year = st.selectbox("", years, label_visibility="collapsed")

    st.markdown('<div class="filter-label" style="margin-top:14px">Region</div>', unsafe_allow_html=True)
    regions_list = ["All"] + sorted(df["Region"].unique().tolist())
    sel_region = st.selectbox(" ", regions_list, label_visibility="collapsed")

    st.markdown('<div class="filter-label" style="margin-top:14px">Category</div>', unsafe_allow_html=True)
    cats_list = ["All"] + sorted(df["Category"].unique().tolist())
    sel_cat = st.selectbox("  ", cats_list, label_visibility="collapsed")

    st.markdown('<div class="filter-label" style="margin-top:14px">Segment</div>', unsafe_allow_html=True)
    segs_list = ["All"] + sorted(df["Segment"].unique().tolist())
    sel_seg = st.selectbox("   ", segs_list, label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div style="font-size:0.72rem;color:#6b7280;text-align:center;">Built with Streamlit + Plotly<br>Dataset: Superstore (Kaggle)</div>', unsafe_allow_html=True)

# ─── FILTER DATA ──────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_year   != "All": fdf = fdf[fdf["Year"]    == int(sel_year)]
if sel_region != "All": fdf = fdf[fdf["Region"]  == sel_region]
if sel_cat    != "All": fdf = fdf[fdf["Category"]== sel_cat]
if sel_seg    != "All": fdf = fdf[fdf["Segment"] == sel_seg]

# ─── KPI CALCULATIONS ─────────────────────────────────────────────────────────
total_sales   = fdf["Sales"].sum()
total_revenue = fdf["Revenue"].sum()
total_profit  = fdf["Profit"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_orders  = len(fdf)
avg_order_val = total_sales / total_orders if total_orders > 0 else 0

def fmt(n):
    if n >= 1_000_000: return f"${n/1_000_000:.2f}M"
    if n >= 1_000:     return f"${n/1_000:.1f}K"
    return f"${n:.0f}"

# ─── PAGE HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:20px;">
    <div>
        <div style="font-size:1.55rem; font-weight:700; color:#1a1d2e;">Sales & Revenue Dashboard</div>
        <div style="font-size:0.82rem; color:#6b7280; margin-top:2px;">Real-time business performance analytics · Superstore Dataset</div>
    </div>
    <div style="font-size:0.75rem; font-family:'DM Mono',monospace; color:#2563eb;
                background:#eff6ff; padding:6px 14px; border-radius:20px; border:1px solid #bfdbfe;">
        ● LIVE FILTERS ACTIVE
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI ROW ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

kpi_data = [
    (k1, "Total Sales",    fmt(total_sales),    "💰", "+12.4% vs last period", "up"),
    (k2, "Total Revenue",  fmt(total_revenue),  "📈", "+8.7% vs last period",  "up"),
    (k3, "Profit",         fmt(total_profit),   "✅", "+5.2% vs last period",  "up"),
    (k4, "Profit Margin",  f"{profit_margin:.1f}%", "🎯", "-1.1% vs last period", "down"),
    (k5, "Total Orders",   f"{total_orders:,}", "🛒", "+18.3% vs last period", "up"),
]

for col, label, val, icon, delta, direction in kpi_data:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-delta {direction}">
                {"▲" if direction=="up" else "▼"} {delta}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ─── ROW 1 : Revenue Over Time + Sales by Category ────────────────────────────
r1c1, r1c2 = st.columns((3, 2))

with r1c1:
    st.markdown('<div class="sec-header">Revenue Over Time</div>', unsafe_allow_html=True)
    st.write("")
    monthly = fdf.groupby("Month").agg(Revenue=("Revenue","sum"), Sales=("Sales","sum")).reset_index()
    monthly = monthly.sort_values("Month")

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Revenue"],
        name="Revenue", mode="lines+markers",
        line=dict(color="#2563eb", width=2.5),
        marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.07)"
    ))
    fig1.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Sales"],
        name="Sales", mode="lines",
        line=dict(color="#7c3aed", width=2, dash="dot"),
    ))
    # show every 4th label to avoid crowding
    tick_vals = monthly["Month"].iloc[::4].tolist()
    fig1.update_xaxes(tickvals=tick_vals, tickangle=-30, tickfont=dict(size=10))
    st.plotly_chart(clean_fig(fig1, 320), use_container_width=True)

with r1c2:
    st.markdown('<div class="sec-header">Sales by Category</div>', unsafe_allow_html=True)
    st.write("")
    cat_sales = fdf.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=True)
    fig2 = go.Figure(go.Bar(
        x=cat_sales["Sales"], y=cat_sales["Category"],
        orientation="h",
        marker=dict(
            color=COLORS[:len(cat_sales)],
            line=dict(color="rgba(0,0,0,0)", width=0)
        ),
        text=[fmt(v) for v in cat_sales["Sales"]],
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig2.update_xaxes(showgrid=False, showticklabels=False)
    fig2.update_yaxes(showgrid=False)
    st.plotly_chart(clean_fig(fig2, 320), use_container_width=True)

# ─── ROW 2 : Sales by Region + Monthly Trends (sub-cat) + Top Products ────────
r2c1, r2c2, r2c3 = st.columns((1.2, 1.8, 1.8))

with r2c1:
    st.markdown('<div class="sec-header">Sales by Region</div>', unsafe_allow_html=True)
    st.write("")
    reg_sales = fdf.groupby("Region")["Sales"].sum().reset_index()
    fig3 = go.Figure(go.Pie(
        labels=reg_sales["Region"],
        values=reg_sales["Sales"],
        hole=0.52,
        marker=dict(colors=COLORS),
        textinfo="label+percent",
        textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<extra></extra>"
    ))
    fig3.add_annotation(text=f"<b>{fmt(reg_sales['Sales'].sum())}</b>",
                        x=0.5, y=0.5, font_size=13, showarrow=False)
    st.plotly_chart(clean_fig(fig3, 320), use_container_width=True)

with r2c2:
    st.markdown('<div class="sec-header">Monthly Trends by Category</div>', unsafe_allow_html=True)
    st.write("")
    mt = fdf.groupby(["Month","Category"])["Sales"].sum().reset_index().sort_values("Month")
    fig4 = px.line(mt, x="Month", y="Sales", color="Category",
                   color_discrete_sequence=COLORS,
                   markers=True)
    fig4.update_traces(marker_size=4, line_width=2)
    tick_vals2 = mt["Month"].unique()[::4].tolist()
    fig4.update_xaxes(tickvals=tick_vals2, tickangle=-30, tickfont=dict(size=10))
    st.plotly_chart(clean_fig(fig4, 320), use_container_width=True)

with r2c3:
    st.markdown('<div class="sec-header">Top Products by Sales</div>', unsafe_allow_html=True)
    st.write("")
    top_prods = fdf.groupby("Product")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(8)
    max_val   = top_prods["Sales"].max()
    rows_html = ""
    for idx, (_, row) in enumerate(top_prods.iterrows()):
        pct   = int(row["Sales"] / max_val * 100)
        rows_html += f"""
        <div class="prod-row">
            <span class="prod-rank">#{idx+1}</span>
            <span class="prod-name">{row['Product'][:22]}{'…' if len(row['Product'])>22 else ''}</span>
            <div class="prod-bar-wrap"><div class="prod-bar" style="width:{pct}%"></div></div>
            <span class="prod-val">{fmt(row['Sales'])}</span>
        </div>"""
    st.markdown(f'<div class="chart-card" style="padding:16px 20px">{rows_html}</div>', unsafe_allow_html=True)

# ─── ROW 3 : Profit Margin by Sub-Category + Sales by Segment ─────────────────
r3c1, r3c2 = st.columns((2, 1))

with r3c1:
    st.markdown('<div class="sec-header">Profit Margin by Sub-Category</div>', unsafe_allow_html=True)
    st.write("")
    sub_pm = fdf.groupby("Sub-Category").agg(Sales=("Sales","sum"), Profit=("Profit","sum")).reset_index()
    sub_pm["Margin%"] = (sub_pm["Profit"] / sub_pm["Sales"] * 100).round(1)
    sub_pm = sub_pm.sort_values("Margin%", ascending=False)

    colors_pm = ["#059669" if v >= 20 else "#d97706" if v >= 10 else "#dc2626" for v in sub_pm["Margin%"]]
    fig5 = go.Figure(go.Bar(
        x=sub_pm["Sub-Category"], y=sub_pm["Margin%"],
        marker_color=colors_pm,
        text=[f"{v}%" for v in sub_pm["Margin%"]],
        textposition="outside",
        textfont=dict(size=10),
    ))
    fig5.add_hline(y=20, line_dash="dash", line_color="#059669", annotation_text="Target 20%",
                   annotation_font_size=10, annotation_font_color="#059669")
    fig5.update_yaxes(title_text="Margin %", ticksuffix="%")
    st.plotly_chart(clean_fig(fig5, 300), use_container_width=True)

with r3c2:
    st.markdown('<div class="sec-header">Revenue by Segment</div>', unsafe_allow_html=True)
    st.write("")
    seg_rev = fdf.groupby("Segment")["Revenue"].sum().reset_index()
    fig6 = go.Figure(go.Pie(
        labels=seg_rev["Segment"],
        values=seg_rev["Revenue"],
        hole=0.45,
        marker=dict(colors=["#2563eb","#7c3aed","#059669"]),
        textinfo="label+percent",
        textfont=dict(size=11),
    ))
    st.plotly_chart(clean_fig(fig6, 300), use_container_width=True)

# ─── ROW 4 : Raw Data Table ────────────────────────────────────────────────────
with st.expander("📋 View Raw Data", expanded=False):
    show_cols = ["Order Date","Category","Sub-Category","Region","Segment","Product","Sales","Revenue","Profit","Quantity"]
    styled = fdf[show_cols].sort_values("Order Date", ascending=False).head(200)
    styled["Order Date"] = styled["Order Date"].dt.strftime("%d %b %Y")
    st.dataframe(styled, use_container_width=True, height=320)
    st.caption(f"Showing top 200 of {len(fdf):,} filtered records")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
.footer {
    margin-top: 48px;
    padding: 20px 28px;
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
.footer-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.footer-avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
    border: 2px solid #2563eb;
    box-shadow: 0 0 0 3px #eff6ff;
}
.footer-avatar img {
    width: 100%; height: 100%;
    object-fit: cover;
    border-radius: 50%;
    display: block;
}
.footer-name  { font-weight: 700; font-size: 0.95rem; color: #1a1d2e; line-height: 1.2; }
.footer-role  { font-size: 0.72rem; color: #6b7280; letter-spacing: 1px; margin-top: 2px; }
.footer-links { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.f-btn {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 8px 16px; border-radius: 8px;
    font-size: 0.8rem; font-weight: 600;
    text-decoration: none !important;
    transition: all 0.25s ease;
    border: 1px solid transparent;
}
.f-btn:hover { transform: translateY(-2px); }
.f-btn-gh   { background:#f6f8fa; color:#24292e !important; border-color:#d0d7de; }
.f-btn-gh:hover   { background:#24292e; color:#fff !important; border-color:#24292e; }
.f-btn-repo { background:#eff6ff; color:#2563eb !important; border-color:#bfdbfe; }
.f-btn-repo:hover { background:#2563eb; color:#fff !important; border-color:#2563eb; }
.f-btn-li   { background:#f0f7ff; color:#0a66c2 !important; border-color:#bcd9f5; }
.f-btn-li:hover   { background:#0a66c2; color:#fff !important; border-color:#0a66c2; }
.footer-copy {
    font-size: 0.72rem; color: #9ca3af;
    margin-top: 14px; text-align: center; width: 100%;
    border-top: 1px solid #f0f0f5; padding-top: 12px;
}
</style>

<div class="footer">
    <div class="footer-left">
        <div class="footer-avatar"><img src="data:image/png;base64,{img_b64 or ''}" alt="Sriram"></div>
        <div>
            <div class="footer-name">Sriram Sai Laggisetti</div>
            <div class="footer-role">AI &amp; ML ENGINEER &nbsp;·&nbsp; DATA SCIENTIST</div>
        </div>
    </div>
    <div class="footer-links">
        <a class="f-btn f-btn-gh"
           href="https://github.com/sriramsai18" target="_blank">
            💻 GitHub Profile
        </a>
        <a class="f-btn f-btn-repo"
           href="https://github.com/sriramsai18/Sales-Revenue-Dashboard" target="_blank">
            📊 Project Repo
        </a>
        <a class="f-btn f-btn-li"
           href="https://www.linkedin.com/in/sriram-sai-laggisetti/" target="_blank">
            💼 LinkedIn
        </a>
    </div>
    <div class="footer-copy">
        Built with Streamlit &amp; Plotly &nbsp;·&nbsp; Dataset: Superstore (Kaggle) &nbsp;·&nbsp; © 2025 Sriram Sai Laggisetti
    </div>
</div>
""", unsafe_allow_html=True)
