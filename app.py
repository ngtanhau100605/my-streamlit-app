import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BDS TPHCM · Dự đoán giá căn hộ",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0d1117;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * {
    color: #e6edf3 !important;
}

/* ── Main text ── */
h1, h2, h3, h4, p, label, div {
    color: #e6edf3;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 16px;
    transition: border-color 0.2s;
}
[data-testid="metric-container"]:hover {
    border-color: #388bfd;
}
[data-testid="stMetricValue"] {
    color: #58a6ff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1.6rem !important;
}
[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricDelta"] {
    font-size: 0.85rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white !important;
    border: none;
    border-radius: 8px;
    font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.6rem 2rem;
    width: 100%;
    transition: opacity 0.2s, transform 0.1s;
}
.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

/* ── Inputs ── */
.stSelectbox > div > div,
.stSlider > div,
.stNumberInput > div > div > input {
    background: #21262d !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
    border-radius: 8px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #21262d;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8b949e !important;
    border-radius: 8px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #21262d !important;
    color: #58a6ff !important;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    border: 1px solid #374151;
    border-radius: 16px;
    padding: 28px 32px;
    margin-top: 16px;
}
.price-main {
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    color: #58a6ff;
    line-height: 1.1;
}
.price-range {
    font-size: 0.95rem;
    color: #8b949e;
    margin-top: 4px;
}
.market-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.88rem;
    font-weight: 600;
    margin-top: 12px;
}
.badge-high   { background: #2d1b1b; color: #f87171; border: 1px solid #7f1d1d; }
.badge-low    { background: #1a2e1a; color: #4ade80; border: 1px solid #14532d; }
.badge-normal { background: #1c2333; color: #93c5fd; border: 1px solid #1e40af; }

/* ── Section headers ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #58a6ff;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border-bottom: 1px solid #21262d;
    padding-bottom: 8px;
    margin-bottom: 16px;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(56,139,253,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: #e6edf3;
    margin: 0;
}
.hero-title span {
    color: #58a6ff;
}
.hero-sub {
    color: #8b949e;
    font-size: 0.95rem;
    margin-top: 8px;
}
.hero-stats {
    display: flex;
    gap: 32px;
    margin-top: 20px;
}
.hero-stat-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #58a6ff;
}
.hero-stat-lbl {
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Divider ── */
hr { border-color: #21262d !important; }

/* ── Plotly backgrounds ── */
.js-plotly-plot { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
DISTRICT_MAP = {
    53:'Quận 1',  54:'Quận 2',  55:'Quận 3',  56:'Quận 4',
    57:'Quận 5',  58:'Quận 6',  59:'Quận 7',  60:'Quận 8',
    61:'Quận 9',  62:'Quận 10', 63:'Quận 11', 64:'Quận 12',
    65:'Bình Thạnh', 66:'Tân Bình', 67:'Tân Phú', 68:'Phú Nhuận',
    69:'Gò Vấp',  70:'Bình Tân', 71:'Thủ Đức', 72:'Bình Chánh',
    73:'Hóc Môn', 74:'Cần Giờ', 75:'Nhà Bè',  76:'Củ Chi',
}
DISTRICT_NAME_TO_ID = {v: k for k, v in DISTRICT_MAP.items()}

DIST_STATS_FALLBACK = {
    'Quận 1':     {'median':13.4e9,'mean':18.4e9,'std':12e9,'count':454},
    'Quận 2':     {'median':8.8e9, 'mean':12.9e9,'std':9e9, 'count':3635},
    'Quận 3':     {'median':6.5e9, 'mean':8.9e9, 'std':5e9, 'count':101},
    'Quận 4':     {'median':6.9e9, 'mean':7.0e9, 'std':3e9, 'count':460},
    'Quận 5':     {'median':4.6e9, 'mean':7.9e9, 'std':6e9, 'count':212},
    'Quận 6':     {'median':4.5e9, 'mean':4.5e9, 'std':2e9, 'count':407},
    'Quận 7':     {'median':6.55e9,'mean':7.9e9, 'std':5e9, 'count':3157},
    'Quận 8':     {'median':3.45e9,'mean':3.7e9, 'std':2e9, 'count':827},
    'Quận 9':     {'median':3.8e9, 'mean':4.2e9, 'std':2.5e9,'count':2411},
    'Quận 10':    {'median':7.2e9, 'mean':7.7e9, 'std':3e9, 'count':387},
    'Quận 11':    {'median':3.99e9,'mean':5.3e9, 'std':4e9, 'count':223},
    'Quận 12':    {'median':2.95e9,'mean':3.0e9, 'std':1.5e9,'count':256},
    'Bình Thạnh': {'median':3.45e9,'mean':3.5e9, 'std':2e9, 'count':616},
    'Tân Bình':   {'median':8.3e9, 'mean':10.3e9,'std':7e9, 'count':803},
    'Tân Phú':    {'median':3.19e9,'mean':3.8e9, 'std':2e9, 'count':207},
    'Phú Nhuận':  {'median':6.8e9, 'mean':6.8e9, 'std':3e9, 'count':399},
    'Gò Vấp':     {'median':4.4e9, 'mean':4.9e9, 'std':2.5e9,'count':422},
    'Bình Tân':   {'median':4.75e9,'mean':6.2e9, 'std':4e9, 'count':1024},
    'Thủ Đức':    {'median':3.65e9,'mean':4.7e9, 'std':3e9, 'count':668},
    'Bình Chánh': {'median':3.5e9, 'mean':3.6e9, 'std':1.5e9,'count':878},
    'Hóc Môn':    {'median':2.5e9, 'mean':2.9e9, 'std':1e9, 'count':35},
    'Nhà Bè':     {'median':1.15e9,'mean':1.18e9,'std':0.5e9,'count':19},
    'Củ Chi':     {'median':4.8e9, 'mean':4.9e9, 'std':2e9, 'count':823},
}


# ─────────────────────────────────────────────
# DATA & MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    paths = [
        'bds_data_clean_v2.csv',
        '/content/drive/MyDrive/bds_data_clean_v2.csv',
    ]
    for p in paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    # Generate synthetic summary from fallback stats
    rows = []
    for dname, s in DIST_STATS_FALLBACK.items():
        for _ in range(min(int(s['count']), 200)):
            price = max(5e8, np.random.normal(s['mean'], s['std']))
            rows.append({'district_name': dname, 'price_vnd': price,
                         'area_m2': np.random.uniform(40, 150),
                         'bedroom': np.random.choice([1,2,3,4]),
                         'price_per_m2': price / np.random.uniform(40,150)})
    return pd.DataFrame(rows)

@st.cache_resource
def load_models():
    # ── Ưu tiên 1: models.pkl gộp ──────────────
    single_paths = ['models.pkl', 'house_price_models/models.pkl']
    for p in single_paths:
        if os.path.exists(p):
            with open(p, 'rb') as f:
                obj = pickle.load(f)
            best_xgb = obj['best_xgb']
            best_lgb = obj['best_lgb']
            best_cat = obj.get('best_cat', obj.get('cat_m'))
            feats    = obj['FEATURES']
            # Convert df_stats dict 
            raw = obj['df_stats']
            dstats = pd.DataFrame(raw)
            dstats.index.name = 'districtId'
            dstats = dstats.rename(columns={
                'median': 'dist_median',
                'mean':   'dist_mean',
                'std':    'dist_std',
                'count':  'dist_count',
            })
            return best_xgb, best_lgb, best_cat, None, dstats, feats

    # ── Ưu tiên 2: các file .pkl riêng lẻ ───────
    model_dirs = ['house_price_models', '/content/drive/MyDrive/house_price_models']
    for d in model_dirs:
        xgb_path = os.path.join(d, 'best_xgb.pkl')
        if os.path.exists(xgb_path):
            with open(os.path.join(d,'best_xgb.pkl'),'rb') as f: best_xgb = pickle.load(f)
            with open(os.path.join(d,'best_lgb.pkl'),'rb') as f: best_lgb = pickle.load(f)
            with open(os.path.join(d,'cat_m.pkl'),'rb') as f:    cat_m    = pickle.load(f)
            meta_path = os.path.join(d,'meta_model.pkl')
            meta = pickle.load(open(meta_path,'rb')) if os.path.exists(meta_path) else None
            with open(os.path.join(d,'dist_stats.pkl'),'rb') as f: dstats = pickle.load(f)
            with open(os.path.join(d,'features.json'),'r') as f:   feats  = json.load(f)
            return best_xgb, best_lgb, cat_m, meta, dstats, feats
    return None

def predict_price(area_m2, bedroom, toilet, district_name,
                  has_furniture=0, is_corner=0, has_view=0,
                  is_vinhomes=0, is_masteri=0,
                  models=None, dist_stats=None, features=None):

    dist_id = DISTRICT_NAME_TO_ID.get(district_name, 61)
    fb = DIST_STATS_FALLBACK.get(district_name, {'median':5e9,'mean':6e9,'std':2e9,'count':50})

    if dist_stats is not None and dist_id in dist_stats.index:
        d_median = float(dist_stats.loc[dist_id,'dist_median'])
        d_mean   = float(dist_stats.loc[dist_id,'dist_mean'])
        d_std    = float(dist_stats.loc[dist_id,'dist_std'])
        d_count  = float(dist_stats.loc[dist_id,'dist_count'])
    else:
        d_median = fb['median']; d_mean = fb['mean']
        d_std    = fb['std'];    d_count = fb['count']

    if models is None:
        # Fallback heuristic
        base = d_median
        area_factor = (area_m2 / 70) ** 0.85
        bed_factor  = 1 + (bedroom - 2) * 0.08
        bonus = 1 + has_furniture*0.04 + is_corner*0.05 + has_view*0.08
        brand = 1 + is_vinhomes*0.15 + is_masteri*0.12
        price = base * area_factor * bed_factor * bonus * brand
        noise_std = d_std * 0.10
    else:
        best_xgb, best_lgb, cat_m, meta_model, _, feats = models
        FEATURES = feats

        sample = pd.DataFrame([{f: 0 for f in FEATURES}])
        sample['area_m2']       = area_m2
        sample['area_log']      = np.log1p(area_m2)
        sample['bedroom']       = bedroom
        sample['toilet']        = toilet
        sample['area_per_room'] = area_m2 / max(bedroom, 1)
        sample['area_x_bed']    = area_m2 * bedroom
        sample['bed_x_toilet']  = bedroom * toilet
        sample['districtId']    = dist_id
        sample['dist_median']   = d_median
        sample['dist_mean']     = d_mean
        sample['dist_std']      = d_std
        sample['dist_count']    = d_count
        sample['ward_median']   = d_median
        sample['ward_count']    = 50
        sample['verified']      = 1
        sample['days_posted']   = 1
        sample['is_new_post']   = 1
        sample['has_furniture'] = has_furniture
        sample['is_corner']     = is_corner
        sample['has_view']      = has_view
        sample['is_vinhomes']   = is_vinhomes
        sample['is_masteri']    = is_masteri

        for col in FEATURES:
            if col not in sample.columns:
                sample[col] = 0

        p_xgb = best_xgb.predict(sample[FEATURES])
        p_lgb = best_lgb.predict(sample[FEATURES])
        p_cat = cat_m.predict(sample[FEATURES])
        if meta_model is not None:
            meta_in = np.column_stack([p_xgb, p_lgb, p_cat])
            price = np.expm1(meta_model.predict(meta_in))[0]
        else:
            price = np.expm1(0.4*p_xgb + 0.4*p_lgb + 0.2*p_cat)[0]
        noise_std = d_std * 0.10

    diff_pct = (price - d_median) / d_median * 100
    if diff_pct > 5:
        market_label = f"Cao hơn thị trường ~{diff_pct:.1f}%"
        badge_class  = "badge-high"
        badge_icon   = "⬆️"
        verdict      = "Giá cao — cân nhắc kỹ trước khi mua"
        verdict_color = "#f87171"
    elif diff_pct < -5:
        market_label = f"Thấp hơn thị trường ~{abs(diff_pct):.1f}%"
        badge_class  = "badge-low"
        badge_icon   = "⬇️"
        verdict      = "Giá tốt — cơ hội đáng xem xét"
        verdict_color = "#4ade80"
    else:
        market_label = f"Ngang bằng thị trường ({diff_pct:+.1f}%)"
        badge_class  = "badge-normal"
        badge_icon   = "↔️"
        verdict      = "Giá hợp lý với thị trường"
        verdict_color = "#93c5fd"

    return {
        'price': price,
        'lo': max(0, price - noise_std),
        'hi': price + noise_std,
        'price_m2': price / area_m2,
        'd_median': d_median,
        'diff_pct': diff_pct,
        'market_label': market_label,
        'badge_class': badge_class,
        'badge_icon': badge_icon,
        'verdict': verdict,
        'verdict_color': verdict_color,
    }


# ─────────────────────────────────────────────
# LOAD RESOURCES
# ─────────────────────────────────────────────
df   = load_data()
mdls = load_models()
if mdls:
    models_tuple = mdls
    dist_stats   = mdls[4]
    features     = mdls[5]
    MODEL_LOADED = True
else:
    models_tuple = None
    dist_stats   = None
    features     = None
    MODEL_LOADED = False


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 24px;'>
        <div style='font-size:2.2rem'>🏙️</div>
        <div style='font-size:1.1rem; font-weight:700; color:#e6edf3;'>BDS TPHCM</div>
        <div style='font-size:0.75rem; color:#8b949e; margin-top:4px;'>AI Price Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📍 Thông tin căn hộ</div>', unsafe_allow_html=True)

    district = st.selectbox("Quận / Huyện", sorted(DISTRICT_NAME_TO_ID.keys()))
    area     = st.slider("Diện tích (m²)", 20, 300, 70, step=5)
    bedroom  = st.selectbox("Số phòng ngủ", [1, 2, 3, 4, 5], index=1)
    toilet   = st.selectbox("Số WC", [1, 2, 3, 4], index=1)

    st.markdown('<div class="section-header" style="margin-top:20px;">✨ Đặc điểm</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        has_furniture = st.checkbox("Nội thất", value=True)
        is_corner     = st.checkbox("Căn góc")
    with col2:
        has_view      = st.checkbox("View đẹp")
        is_vinhomes   = st.checkbox("Vinhomes")

    is_masteri = st.checkbox("Masteri")

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔍 Dự đoán giá", use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.75rem; color:#8b949e; text-align:center;'>
        {'✅ Model đã load' if MODEL_LOADED else '⚠️ Dùng heuristic (chưa có .pkl)'}
        <br>Dataset: {len(df):,} căn hộ
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-title">Dự đoán giá <span>căn hộ TPHCM</span></p>
    <p class="hero-sub">Powered by XGBoost · LightGBM · CatBoost Stacking Ensemble</p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-val">18,424</div>
            <div class="hero-stat-lbl">Căn hộ</div>
        </div>
        <div>
            <div class="hero-stat-val">23</div>
            <div class="hero-stat-lbl">Quận / Huyện</div>
        </div>
        <div>
            <div class="hero-stat-val">3</div>
            <div class="hero-stat-lbl">Models AI</div>
        </div>
        <div>
            <div class="hero-stat-val">30+</div>
            <div class="hero-stat-lbl">Features</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔮 Dự đoán giá", "📊 Phân tích thị trường", "🔄 So sánh căn hộ"])


# ══════════════════════════════════════════════
# TAB 1 — DỰ ĐOÁN GIÁ
# ══════════════════════════════════════════════
with tab1:
    if predict_btn or True:  # Show on load with default values
        result = predict_price(
            area_m2=area, bedroom=bedroom, toilet=toilet,
            district_name=district,
            has_furniture=int(has_furniture),
            is_corner=int(is_corner),
            has_view=int(has_view),
            is_vinhomes=int(is_vinhomes),
            is_masteri=int(is_masteri),
            models=models_tuple,
            dist_stats=dist_stats,
            features=features,
        )

        # ── Result card ──
        st.markdown(f"""
        <div class="result-card">
            <div style='font-size:0.8rem; color:#8b949e; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;'>
                Giá ước tính · {district} · {area}m² · {bedroom}PN
            </div>
            <div class="price-main">{result['price']/1e9:.2f} tỷ đồng</div>
            <div class="price-range">
                Khoảng: {result['lo']/1e9:.2f} – {result['hi']/1e9:.2f} tỷ &nbsp;·&nbsp;
                {result['price_m2']/1e6:.1f} triệu/m²
            </div>
            <div class="market-badge {result['badge_class']}">
                {result['badge_icon']} {result['market_label']}
            </div>
            <div style='margin-top:14px; font-size:0.9rem; color:{result["verdict_color"]}; font-weight:600;'>
                → {result['verdict']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Metrics row ──
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💰 Giá dự đoán", f"{result['price']/1e9:.2f} tỷ")
        c2.metric("📐 Giá/m²", f"{result['price_m2']/1e6:.1f} triệu")
        c3.metric("🏙️ Median quận", f"{result['d_median']/1e9:.2f} tỷ")
        c4.metric("📈 So thị trường", f"{result['diff_pct']:+.1f}%",
                  delta=f"{result['diff_pct']:+.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Price breakdown gauge ──
        col_a, col_b = st.columns([1, 1])

        with col_a:
            st.markdown('<div class="section-header">📊 Vị trí giá trong thị trường</div>', unsafe_allow_html=True)
            fb    = DIST_STATS_FALLBACK.get(district, {'median':5e9,'mean':6e9,'std':2e9,'count':50})
            med   = result['d_median']
            price = result['price']
            low   = max(med * 0.4, 3e8)
            high  = med * 2.5

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=price/1e9,
                number={'suffix': " tỷ", 'font': {'size': 28, 'color': '#58a6ff', 'family': 'Space Mono'}},
                gauge={
                    'axis': {'range': [low/1e9, high/1e9],
                             'tickcolor': '#8b949e', 'tickfont': {'color': '#8b949e', 'size': 11}},
                    'bar': {'color': '#388bfd', 'thickness': 0.25},
                    'bgcolor': '#161b22',
                    'bordercolor': '#21262d',
                    'steps': [
                        {'range': [low/1e9, med*0.8/1e9],   'color': '#1a3a2a'},
                        {'range': [med*0.8/1e9, med*1.2/1e9],'color': '#1c2333'},
                        {'range': [med*1.2/1e9, high/1e9],   'color': '#3a1a1a'},
                    ],
                    'threshold': {
                        'line': {'color': '#f0b429', 'width': 3},
                        'thickness': 0.8,
                        'value': med/1e9,
                    },
                },
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#8b949e',
                margin=dict(t=20, b=10, l=30, r=30),
                height=220,
                annotations=[dict(
                    x=0.5, y=-0.08, xref='paper', yref='paper',
                    text=f"<span style='color:#f0b429'>━</span> Median quận: {med/1e9:.1f} tỷ",
                    showarrow=False, font=dict(size=11, color='#8b949e')
                )]
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-header">🔑 Yếu tố tác động</div>', unsafe_allow_html=True)
            factors = {
                'Diện tích': min(area / 150, 1.0),
                'Vị trí quận': min(result['d_median'] / 15e9, 1.0),
                'Số phòng ngủ': bedroom / 5,
                'Nội thất': 0.6 if has_furniture else 0.1,
                'Căn góc': 0.7 if is_corner else 0.1,
                'View': 0.75 if has_view else 0.1,
                'Thương hiệu': 0.9 if (is_vinhomes or is_masteri) else 0.2,
            }
            fig_bar = go.Figure(go.Bar(
                x=list(factors.values()),
                y=list(factors.keys()),
                orientation='h',
                marker=dict(
                    color=[f'rgba(56,139,253,{v*0.9+0.1})' for v in factors.values()],
                    line=dict(color='rgba(0,0,0,0)')
                ),
                text=[f'{v*100:.0f}%' for v in factors.values()],
                textposition='outside',
                textfont=dict(color='#8b949e', size=11),
            ))
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, range=[0, 1.3]),
                yaxis=dict(tickfont=dict(color='#e6edf3', size=12)),
                margin=dict(t=10, b=10, l=10, r=60),
                height=250,
            )
            st.plotly_chart(fig_bar, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 2 — PHÂN TÍCH THỊ TRƯỜNG
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">🗺️ Giá median theo quận</div>', unsafe_allow_html=True)

    dist_summary = pd.DataFrame([
        {'district': k, 'median_ty': v['median']/1e9, 'mean_ty': v['mean']/1e9, 'count': v['count']}
        for k, v in DIST_STATS_FALLBACK.items()
    ]).sort_values('median_ty', ascending=True)

    fig_dist = go.Figure()
    colors_bar = ['#388bfd' if d == district else '#21262d' for d in dist_summary['district']]
    fig_dist.add_trace(go.Bar(
        y=dist_summary['district'],
        x=dist_summary['median_ty'],
        orientation='h',
        marker_color=colors_bar,
        marker_line_color='rgba(0,0,0,0)',
        text=[f'{v:.1f} tỷ' for v in dist_summary['median_ty']],
        textposition='outside',
        textfont=dict(color='#8b949e', size=10),
        hovertemplate='<b>%{y}</b><br>Median: %{x:.2f} tỷ<extra></extra>',
    ))
    fig_dist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#21262d', tickfont=dict(color='#8b949e'),
                   title=dict(text='Tỷ đồng', font=dict(color='#8b949e'))),
        yaxis=dict(tickfont=dict(color='#e6edf3', size=11)),
        margin=dict(t=10, b=10, l=10, r=80),
        height=520,
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    # ── District heatmap + scatter ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">📦 Phân phối giá top 8 quận</div>', unsafe_allow_html=True)
        top8 = dist_summary.sort_values('count', ascending=False).head(8)['district'].tolist()
        if 'district_name' in df.columns and 'price_vnd' in df.columns:
            df_top = df[df['district_name'].isin(top8)].copy()
            df_top['price_ty'] = df_top['price_vnd'] / 1e9
            fig_box = px.box(
                df_top, x='district_name', y='price_ty',
                color='district_name',
                color_discrete_sequence=px.colors.sequential.Blues_r,
            )
        else:
            # Synthetic
            rows = []
            for d in top8:
                s = DIST_STATS_FALLBACK[d]
                prices = np.random.normal(s['mean']/1e9, s['std']/1e9, 300)
                prices = prices[(prices > 0.5) & (prices < 50)]
                for p in prices:
                    rows.append({'district_name': d, 'price_ty': p})
            df_syn = pd.DataFrame(rows)
            fig_box = px.box(df_syn, x='district_name', y='price_ty',
                             color='district_name',
                             color_discrete_sequence=px.colors.sequential.Blues_r)

        fig_box.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(tickangle=-35, tickfont=dict(color='#8b949e', size=10),
                       title=None, gridcolor='#21262d'),
            yaxis=dict(tickfont=dict(color='#8b949e'), title='Giá (tỷ)',
                       gridcolor='#21262d', range=[0, 30]),
            margin=dict(t=10, b=80, l=50, r=10),
            height=350,
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">💡 Số lượng listing theo quận</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=dist_summary['district'],
            values=dist_summary['count'],
            hole=0.55,
            marker=dict(
                colors=px.colors.sequential.Blues_r * 2,
                line=dict(color='#0d1117', width=2)
            ),
            textfont=dict(color='#e6edf3', size=10),
            hovertemplate='<b>%{label}</b><br>%{value:,} listings<br>%{percent}<extra></extra>',
        ))
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color='#8b949e', size=9), bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=10, b=10, l=10, r=10),
            height=350,
            annotations=[dict(text='18,424<br><span style="font-size:10px">căn hộ</span>',
                              x=0.5, y=0.5, font_size=16, font_color='#58a6ff',
                              showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Price vs area scatter ──
    st.markdown('<div class="section-header">🔵 Diện tích vs Giá (toàn bộ thị trường)</div>', unsafe_allow_html=True)
    if 'area_m2' in df.columns and 'price_vnd' in df.columns:
        df_scatter = df[df['price_vnd'] < 30e9].copy()
        df_scatter['price_ty'] = df_scatter['price_vnd'] / 1e9
        fig_sc = px.scatter(
            df_scatter.sample(min(3000, len(df_scatter))),
            x='area_m2', y='price_ty',
            color='district_name' if 'district_name' in df.columns else None,
            opacity=0.5, size_max=5,
            hover_data=['district_name'] if 'district_name' in df.columns else None,
            labels={'area_m2': 'Diện tích (m²)', 'price_ty': 'Giá (tỷ)'},
        )
    else:
        rows = []
        for dname, s in DIST_STATS_FALLBACK.items():
            for _ in range(100):
                area_s = np.random.uniform(30, 200)
                price_s = max(0.5, np.random.normal(s['mean'] * (area_s/80)**0.7, s['std']*0.5)) / 1e9
                rows.append({'area_m2': area_s, 'price_ty': price_s, 'district_name': dname})
        df_sc2 = pd.DataFrame(rows)
        fig_sc = px.scatter(df_sc2, x='area_m2', y='price_ty', color='district_name',
                            opacity=0.5, labels={'area_m2': 'Diện tích (m²)', 'price_ty': 'Giá (tỷ)'})

    # Highlight current input
    fig_sc.add_trace(go.Scatter(
        x=[area], y=[result['price']/1e9 if 'result' in dir() else 5],
        mode='markers',
        marker=dict(size=14, color='#f0b429', symbol='star', line=dict(color='white', width=2)),
        name='Căn hộ của bạn',
        hovertemplate=f'<b>Căn hộ của bạn</b><br>Diện tích: {area}m²<br>Giá: {result["price"]/1e9:.2f} tỷ<extra></extra>'
        if 'result' in dir() else '<b>Căn hộ của bạn</b><extra></extra>'
    ))
    fig_sc.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#21262d', tickfont=dict(color='#8b949e')),
        yaxis=dict(gridcolor='#21262d', tickfont=dict(color='#8b949e')),
        legend=dict(font=dict(color='#8b949e', size=9), bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=10, b=40, l=50, r=10),
        height=380,
    )
    st.plotly_chart(fig_sc, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 — SO SÁNH CĂN HỘ
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">🔄 So sánh 3 căn hộ cùng lúc</div>', unsafe_allow_html=True)
    st.caption("Nhập thông số 3 căn hộ để so sánh giá và đặc điểm side-by-side")

    cols = st.columns(3)
    apartments = []
    labels = ["🏠 Căn A", "🏢 Căn B", "🏗️ Căn C"]

    for i, (col, label) in enumerate(zip(cols, labels)):
        with col:
            st.markdown(f"**{label}**")
            d_i   = st.selectbox("Quận",        sorted(DISTRICT_NAME_TO_ID.keys()), key=f'd{i}',
                                 index=i % len(DISTRICT_NAME_TO_ID))
            a_i   = st.number_input("Diện tích (m²)", 20, 500, [65, 85, 100][i], key=f'a{i}')
            b_i   = st.selectbox("Phòng ngủ",   [1,2,3,4,5], index=min(i+1,4), key=f'b{i}')
            t_i   = st.selectbox("WC",          [1,2,3,4],   index=min(i,3),   key=f't{i}')
            fur_i = st.checkbox("Nội thất",  key=f'f{i}', value=True)
            cor_i = st.checkbox("Căn góc",   key=f'c{i}')
            apartments.append({'label': label, 'district': d_i, 'area': a_i,
                                'bedroom': b_i, 'toilet': t_i,
                                'has_furniture': int(fur_i), 'is_corner': int(cor_i)})

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ So sánh ngay", use_container_width=True):
        results = []
        for apt in apartments:
            r = predict_price(
                area_m2=apt['area'], bedroom=apt['bedroom'], toilet=apt['toilet'],
                district_name=apt['district'],
                has_furniture=apt['has_furniture'], is_corner=apt['is_corner'],
                models=models_tuple, dist_stats=dist_stats, features=features,
            )
            r['label']    = apt['label']
            r['district'] = apt['district']
            r['area']     = apt['area']
            r['bedroom']  = apt['bedroom']
            results.append(r)

        # ── Comparison metrics ──
        m_cols = st.columns(3)
        for rc, res in zip(m_cols, results):
            with rc:
                st.metric(res['label'], f"{res['price']/1e9:.2f} tỷ",
                          delta=f"{res['diff_pct']:+.1f}% vs quận")
                st.markdown(f"""
                <div style='font-size:0.8rem; color:#8b949e; line-height:1.8;'>
                    📍 {res['district']}<br>
                    📐 {res['area']}m² · {res['bedroom']}PN<br>
                    💵 {res['price_m2']/1e6:.1f} triệu/m²<br>
                    <span style='color:{res["verdict_color"]}'>{res['badge_icon']} {res['verdict']}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Bar chart comparison ──
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Bar(
            name='Giá dự đoán',
            x=[r['label'] for r in results],
            y=[r['price']/1e9 for r in results],
            marker_color=['#388bfd','#f0b429','#4ade80'],
            text=[f"{r['price']/1e9:.2f} tỷ" for r in results],
            textposition='outside',
            textfont=dict(color='#e6edf3', size=13),
            error_y=dict(
                type='data',
                array=[(r['hi']-r['price'])/1e9 for r in results],
                arrayminus=[(r['price']-r['lo'])/1e9 for r in results],
                color='#8b949e', thickness=2, width=8,
            ),
        ))
        fig_cmp.add_trace(go.Bar(
            name='Median quận',
            x=[r['label'] for r in results],
            y=[r['d_median']/1e9 for r in results],
            marker_color='rgba(139,148,158,0.3)',
            marker_line_color='rgba(139,148,158,0.6)',
            marker_line_width=1,
            text=[f"median: {r['d_median']/1e9:.1f}" for r in results],
            textposition='outside',
            textfont=dict(color='#8b949e', size=10),
        ))
        fig_cmp.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            barmode='group',
            xaxis=dict(tickfont=dict(color='#e6edf3', size=14)),
            yaxis=dict(gridcolor='#21262d', tickfont=dict(color='#8b949e'),
                       title='Tỷ đồng'),
            legend=dict(font=dict(color='#8b949e'), bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=30, b=30, l=50, r=30),
            height=380,
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        # ── Giá/m² comparison ──
        fig_m2 = go.Figure(go.Bar(
            x=[r['label'] for r in results],
            y=[r['price_m2']/1e6 for r in results],
            marker_color=['#388bfd','#f0b429','#4ade80'],
            text=[f"{r['price_m2']/1e6:.1f} tr/m²" for r in results],
            textposition='outside',
            textfont=dict(color='#e6edf3', size=12),
        ))
        fig_m2.update_layout(
            title=dict(text='Giá trên m²', font=dict(color='#e6edf3', size=13)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#e6edf3')),
            yaxis=dict(gridcolor='#21262d', tickfont=dict(color='#8b949e'),
                       title='Triệu/m²'),
            margin=dict(t=40, b=30, l=50, r=30),
            height=280,
        )
        st.plotly_chart(fig_m2, use_container_width=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#8b949e; font-size:0.8rem; padding:12px 0 24px;'>
    🏙️ <strong style='color:#58a6ff'>BDS TPHCM Price Intelligence</strong> &nbsp;·&nbsp;
    XGBoost + LightGBM + CatBoost Stacking &nbsp;·&nbsp;
    
</div>
""", unsafe_allow_html=True)
