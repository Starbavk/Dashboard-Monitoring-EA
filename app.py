import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from utils.data_loader import load_excel, get_summary
from utils.charts import chart_overall, chart_donut, chart_per_kantor
from utils.export import export_excel, export_pdf
from utils import data_store

LOGO_DIR = Path(__file__).parent
logo_djpb = base64.b64encode((LOGO_DIR / "logo_djpb.png").read_bytes()).decode()
logo_intress = base64.b64encode((LOGO_DIR / "logo_intress.png").read_bytes()).decode()

st.set_page_config(page_title="Dashboard Monitoring Aktivasi Employee Advocacy", page_icon="📊", layout="wide")

# ── Color Palette ───────────────────────────────────────
SIDEBAR_BG = "#1B2A4A"
SIDEBAR_TEXT = "#CBD5E1"
SIDEBAR_ACTIVE = "#3B82F6"
MAIN_BG = "#F0F4F8"
DARK = "#1E293B"
GRAY = "#64748B"
BLUE = "#3B82F6"
GREEN = "#059669"
RED = "#DC2626"
GOLD = "#D97706"
WHITE = "#FFFFFF"
BORDER = "#E2E8F0"

# ── CSS ─────────────────────────────────────────────────
st.markdown(f"""
<style>
    /* Force light color scheme globally */
    :root, html, body {{ color-scheme: light !important; }}

    /* Global */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
    [data-testid="stBottomBlockContainer"] {{
        background: {MAIN_BG} !important;
        color-scheme: light !important;
    }}
    .block-container {{
        padding: 1.5rem 2rem !important; max-width: 100% !important;
    }}
    [data-testid="stHeader"] {{ display: none !important; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {SIDEBAR_BG} !important;
        min-width: 260px !important; max-width: 260px !important;
    }}
    section[data-testid="stSidebar"] > div:first-child {{
        background: {SIDEBAR_BG} !important;
        padding-top: 1.5rem !important;
    }}
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown span, [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2, [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stCaption {{
        color: {SIDEBAR_TEXT} !important;
    }}
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-baseweb="radio"] {{
        color: {WHITE} !important;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.1) !important;
    }}
    [data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        color: {SIDEBAR_TEXT} !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(255,255,255,0.1) !important;
        border-color: {SIDEBAR_ACTIVE} !important;
        color: {WHITE} !important;
    }}
    [data-testid="stSidebar"] .stTextInput input {{
        background: rgba(255,255,255,0.08) !important;
        color: {WHITE} !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 6px !important;
    }}
    [data-testid="stSidebar"] .stFileUploader,
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px dashed rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
    }}
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {{
        color: {SIDEBAR_TEXT} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {{
        background: rgba(255,255,255,0.1) !important;
        color: {WHITE} !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }}
    [data-testid="stSidebar"] .stCheckbox label span {{
        color: {SIDEBAR_TEXT} !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background: rgba(255,255,255,0.08) !important;
        border-color: rgba(255,255,255,0.2) !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="tag"] {{
        background: rgba(59,130,246,0.2) !important;
        color: {WHITE} !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="tag"] span {{ color: {WHITE} !important; }}

    /* Main content widgets */
    [data-baseweb="select"] > div, [data-baseweb="input"] > div,
    [data-baseweb="base-input"], .stTextInput input,
    .stSelectbox div[data-baseweb="select"] > div {{
        background: {WHITE} !important; color: {DARK} !important;
        border-color: {BORDER} !important; border-radius: 8px !important;
    }}
    [data-baseweb="tag"] {{ background: #EFF6FF !important; color: {BLUE} !important; border-radius: 4px !important; }}
    [data-baseweb="tag"] span {{ color: {BLUE} !important; }}
    [data-baseweb="popover"] li, [data-baseweb="menu"] li {{
        background: {WHITE} !important; color: {DARK} !important;
    }}
    [data-baseweb="popover"] ul, [data-baseweb="menu"] ul {{ background: {WHITE} !important; }}

    /* Cards */
    .overview-cards {{
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    .ov-card {{
        background: {WHITE}; border-radius: 12px; padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid {BORDER};
        display: flex; align-items: center; gap: 1rem;
    }}
    .ov-card .icon {{
        width: 48px; height: 48px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; font-weight: 700; color: {WHITE};
        flex-shrink: 0;
    }}
    .ov-card .icon.blue {{ background: #2563EB; }}
    .ov-card .icon.green {{ background: {GREEN}; }}
    .ov-card .icon.red {{ background: {RED}; }}
    .ov-card .info .label {{ font-size: 0.8rem; color: {GRAY}; margin-bottom: 4px; font-weight: 500; }}
    .ov-card .info .value {{ font-size: 1.6rem; font-weight: 700; color: {DARK}; line-height: 1.2; }}
    .ov-card .info .sub {{ font-size: 0.75rem; color: {GRAY}; margin-top: 4px; }}

    /* Chart containers */
    .chart-container {{
        background: {WHITE}; border-radius: 12px; padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid {BORDER};
        margin-bottom: 1rem;
    }}
    .chart-title {{
        font-size: 0.9rem; font-weight: 600; color: {DARK}; margin-bottom: 0.5rem;
    }}

    /* Table section */
    .table-section {{
        background: {WHITE}; border-radius: 12px; padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid {BORDER};
        margin-bottom: 1rem;
    }}

    /* Force dataframe light mode */
    div[data-testid="stDataFrame"] {{ background: {WHITE} !important; }}
    div[data-testid="stDataFrame"] > div {{ background: {WHITE} !important; }}
    div[data-testid="stDataFrame"] iframe {{
        background: {WHITE} !important;
        color-scheme: light !important;
    }}
    .stDataFrame, .stDataFrame > div, .stDataFrame div {{
        background: {WHITE} !important;
        color-scheme: light !important;
    }}

    /* Force ALL labels in main area to dark */
    .stApp label, .stApp .stSelectbox label, .stApp .stTextInput label,
    .stApp .stMultiSelect label, .stApp .stRadio label,
    .stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stWidgetLabel"] p {{
        color: {DARK} !important;
    }}

    /* Force placeholder text visible */
    .stApp .stTextInput input::placeholder {{
        color: #94A3B8 !important; opacity: 1 !important;
    }}
    .stApp .stTextInput input {{ color: {DARK} !important; }}

    /* Force selectbox text dark */
    .stApp .stSelectbox [data-baseweb="select"] span,
    .stApp .stSelectbox [data-baseweb="select"] div {{
        color: {DARK} !important;
    }}

    /* Caption text in main area */
    .stApp .stCaption, .stApp .stMarkdown p, .stApp .stMarkdown span {{
        color: {DARK} !important;
    }}

    /* Override: sidebar text must stay light (higher specificity) */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown span {{
        color: {SIDEBAR_TEXT} !important;
    }}

    /* Welcome bar */
    .welcome-bar {{
        background: {WHITE}; border-radius: 12px; padding: 1rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid {BORDER};
        margin-bottom: 1.5rem;
        display: flex; align-items: center; justify-content: space-between;
    }}
    .welcome-bar .left h2 {{
        font-size: 1.1rem; font-weight: 600; color: {DARK}; margin: 0;
    }}
    .welcome-bar .left .edisi {{
        font-size: 0.85rem; color: {GRAY}; margin: 0.2rem 0 0 0;
    }}
    .welcome-bar .right {{
        display: flex; align-items: center; gap: 10px;
    }}
    .welcome-bar .right img {{ height: 40px; width: auto; object-fit: contain; }}
    .welcome-bar .right img.logo-kiri {{ height: 55px; }}
    .welcome-bar .right img.logo-kanan {{ height: 24px; }}

    /* Download buttons */
    .stDownloadButton button {{
        background: {WHITE} !important; color: {DARK} !important;
        border: 1px solid {BORDER} !important; border-radius: 8px !important;
        font-size: 0.85rem !important;
    }}
    .stDownloadButton button:hover {{
        border-color: {BLUE} !important; color: {BLUE} !important;
        background: #F8FAFC !important;
    }}

    /* Sidebar brand */
    .sidebar-brand {{
        text-align: center; padding: 0.5rem 1rem 1.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1rem;
    }}
    .sidebar-brand img {{ height: 50px; margin-bottom: 0.5rem; }}
    .sidebar-brand .title {{ font-size: 0.8rem; color: {SIDEBAR_TEXT}; font-weight: 500; }}
    .sidebar-brand .subtitle {{ font-size: 0.65rem; color: rgba(255,255,255,0.5); }}

    /* Empty state */
    .empty-state {{
        text-align: center; padding: 5rem 2rem;
        background: {WHITE}; border-radius: 12px;
        border: 1px solid {BORDER};
    }}
    .empty-state .icon {{ font-size: 3.5rem; margin-bottom: 1rem; }}
    .empty-state h3 {{ color: {DARK}; font-weight: 500; margin-bottom: 0.5rem; }}
    .empty-state p {{ color: {GRAY}; font-size: 0.9rem; }}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(f"""
    <div class="sidebar-brand">
        <img src="data:image/png;base64,{logo_djpb}" alt="DJPb">
        <div class="title">Dashboard Monitoring EA</div>
        <div class="subtitle">Kanwil DJPb Prov. Jawa Barat</div>
    </div>
    """, unsafe_allow_html=True)

    # Filter (only show if data loaded)
    if "data" in st.session_state and st.session_state["data"] is not None:
        st.markdown(f"<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.5px;color:rgba(255,255,255,0.5);margin-bottom:0.3rem;font-weight:600'>Filter Unit</p>", unsafe_allow_html=True)
        st.checkbox("Pilih Semua", value=True, key="sa")
        es3_list = sorted(st.session_state["data"]["Eselon 3"].dropna().unique())
        if st.session_state.get("sa", True):
            st.multiselect("Unit", es3_list, default=es3_list, key="es3_dummy", disabled=True, label_visibility="collapsed")
        else:
            st.multiselect("Unit", es3_list, key="es3", label_visibility="collapsed")
        st.divider()

    # Role & Auth
    st.markdown(f"<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.5px;color:rgba(255,255,255,0.5);margin-bottom:0.3rem;font-weight:600'>Mode</p>", unsafe_allow_html=True)
    st.radio("Mode", ["Admin", "User"], index=1, key="role", label_visibility="collapsed")

    if st.session_state["role"] == "Admin":
        if not st.session_state.get("admin_auth", False):
            st.markdown(f"<p style='font-size:0.75rem;color:{SIDEBAR_TEXT};margin-top:0.5rem'>Login Admin</p>", unsafe_allow_html=True)
            user = st.text_input("Username", key="login_user", label_visibility="collapsed", placeholder="Username")
            pwd = st.text_input("Password", type="password", key="login_pwd", label_visibility="collapsed", placeholder="Password")
            if st.button("Login", use_container_width=True):
                if user == "admin" and pwd == "djpb89":
                    st.session_state["admin_auth"] = True
                    st.rerun()
                else:
                    st.error("Username atau password salah")
            uploaded_file = None
        else:
            st.markdown(f"<p style='font-size:0.75rem;color:{SIDEBAR_TEXT};margin-top:0.5rem'>Upload Data</p>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("File Excel", type=["xlsx"], label_visibility="collapsed")

            if uploaded_file is not None and st.button("Reset Data", use_container_width=True):
                for k in ["data", "uploaded_name"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()

            if "data" in st.session_state and st.session_state["data"] is not None:
                df_s = st.session_state["data"]
                st.caption(f"{len(df_s)} pegawai · {df_s['Eselon 3'].nunique()} unit")
            else:
                st.caption("Upload file Excel (.xlsx) dari Dashboard Aktivasi")

            st.divider()
            if st.button("Logout", use_container_width=True):
                del st.session_state["admin_auth"]
                st.rerun()
    else:
        uploaded_file = None
        if data_store.exists():
            st.caption("Mode User — view only")
        else:
            st.caption("Menunggu admin upload data")

# ── Load data ──────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state["data"] = None

if st.session_state["role"] == "Admin" and uploaded_file is not None and st.session_state.get("uploaded_name") != uploaded_file.name:
    try:
        uploaded_file.seek(0)
        df = load_excel(uploaded_file)
        st.session_state["data"] = df
        st.session_state["uploaded_name"] = uploaded_file.name
        data_store.save(df)
        st.rerun()
    except Exception as e:
        st.error(f"Gagal memuat: {e}")

if st.session_state["data"] is None and data_store.exists():
    st.session_state["data"] = data_store.load()
    st.rerun()

df = st.session_state["data"]

# ── Header / Welcome Bar ───────────────────────────────
st.markdown(f"""
<div class="welcome-bar">
    <div class="left">
        <h2>Dashboard Monitoring Aktivasi Employee Advocacy</h2>
        <p class="edisi">Kanwil DJPb Provinsi Jawa Barat</p>
    </div>
    <div class="right">
        <img class="logo-kiri" src="data:image/png;base64,{logo_djpb}" alt="DJPb">
        <img class="logo-kanan" src="data:image/png;base64,{logo_intress}" alt="InTress">
    </div>
</div>
""", unsafe_allow_html=True)

# ── Edisi EA ────────────────────────────────────────────
edisi_sekarang = data_store.load_edisi()
if st.session_state.get("role") == "Admin" and st.session_state.get("admin_auth", False):
    col_edisi = st.columns([0.4, 0.6])
    with col_edisi[0]:
        baru = st.text_input("Edisi EA", value=edisi_sekarang, key="edisi", placeholder="Contoh: EA-06-APBN KiTa Juni 2026")
        if baru != edisi_sekarang:
            data_store.save_edisi(baru)
            st.rerun()
else:
    if edisi_sekarang:
        st.markdown(f"<div style='font-size:0.9rem;color:{GRAY};margin-bottom:1rem'><strong>Edisi EA:</strong> {edisi_sekarang}</div>", unsafe_allow_html=True)

# ── Empty state ─────────────────────────────────────────
if df is None:
    if st.session_state["role"] == "Admin" and not st.session_state.get("admin_auth", False):
        msg = "Login sebagai Admin untuk upload data"
    elif st.session_state["role"] == "Admin":
        msg = "Upload file Excel di sidebar untuk memulai"
    else:
        msg = "Admin belum mengupload data. Silakan tunggu."
    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">📊</div>
        <h3>{msg}</h3>
        <p>File export dari Dashboard Aktivasi (.xlsx)</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Apply filters ───────────────────────────────────────
es3_list = sorted(df["Eselon 3"].dropna().unique())

if st.session_state.get("sa", True):
    selected_units = st.session_state.get("es3_dummy", es3_list)
else:
    selected_units = st.session_state.get("es3", es3_list)

d_filter = df[df["Eselon 3"].isin(selected_units)] if selected_units else df
sum_f = get_summary(d_filter)

# ── Overview Cards (3 cards) ────────────────────────────
icon_users = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
icon_check = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
icon_x = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'

pct_aktif = f"{sum_f['aktif']/sum_f['total']*100:.1f}%" if sum_f['total'] else "0%"
pct_belum = f"{sum_f['belum']/sum_f['total']*100:.1f}%" if sum_f['total'] else "0%"

st.markdown(f"""
<div class="overview-cards">
    <div class="ov-card">
        <div class="icon blue">{icon_users}</div>
        <div class="info">
            <div class="label">Total Pegawai</div>
            <div class="value">{sum_f['total']}</div>
            <div class="sub">{d_filter['Eselon 3'].nunique()} unit eselon III</div>
        </div>
    </div>
    <div class="ov-card">
        <div class="icon green">{icon_check}</div>
        <div class="info">
            <div class="label">Sudah Aktivasi</div>
            <div class="value">{sum_f['aktif']}</div>
            <div class="sub">{pct_aktif} dari total</div>
        </div>
    </div>
    <div class="ov-card">
        <div class="icon red">{icon_x}</div>
        <div class="info">
            <div class="label">Belum Aktivasi</div>
            <div class="value">{sum_f['belum']}</div>
            <div class="sub">{pct_belum} dari total</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Charts ──────────────────────────────────────────────
CHART_CONFIG = {
    "modeBarButtonsToRemove": [
        "zoom2d", "pan2d", "select2d", "lasso2d",
        "zoomIn2d", "zoomOut2d", "toImage",
        "toggleSpikelines", "hoverClosestCartesian",
        "hoverCompareCartesian", "sendDataToCloud",
    ],
    "displaylogo": False,
}

col_ch_a, col_ch_b = st.columns(2)
with col_ch_a:
    st.markdown('<div class="chart-container"><div class="chart-title">Status Aktivasi Keseluruhan</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_overall(d_filter), use_container_width=True, key="ch_bar", config=CHART_CONFIG)
    st.markdown('</div>', unsafe_allow_html=True)
with col_ch_b:
    st.markdown('<div class="chart-container"><div class="chart-title">Komposisi Aktivasi</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_donut(d_filter), use_container_width=True, key="ch_donut", config=CHART_CONFIG)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-container"><div class="chart-title">Aktivasi per Eselon III</div>', unsafe_allow_html=True)
st.plotly_chart(chart_per_kantor(d_filter), use_container_width=True, key="ch_per_es3", config=CHART_CONFIG)
st.markdown('</div>', unsafe_allow_html=True)

# ── Table ───────────────────────────────────────────────
st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:1.5rem 0;">', unsafe_allow_html=True)
cf1, cf2, cf3 = st.columns([1, 1, 0.6])
with cf1:
    f_st = st.selectbox("Status", ["Semua", "Sudah Aktivasi", "Belum Aktivasi"], key="st_flt")
with cf2:
    f_nm = st.text_input("Cari Nama", placeholder="Ketik nama...", key="nm_flt")
with cf3:
    st.markdown(f"""<div style="margin-top:1.5rem;padding:0.5rem 1rem;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;display:flex;align-items:baseline;justify-content:center;gap:6px;">
        <span style="font-size:1.3rem;font-weight:700;color:#1D4ED8;">{len(d_filter)}</span>
        <span style="font-size:0.8rem;color:#3B82F6;font-weight:500;">pegawai</span>
    </div>""", unsafe_allow_html=True)

d_all = d_filter.copy()
if f_st == "Sudah Aktivasi":
    d_all = d_all[d_all["Pegawai V"] == "Sudah"]
elif f_st == "Belum Aktivasi":
    d_all = d_all[d_all["Pegawai X"] == "Sudah"]
if f_nm:
    d_all = d_all[d_all["Nama Lengkap"].str.contains(f_nm, case=False, na=False)]

out = d_all[["Nama Kantor", "Eselon 3", "Nama Lengkap", "Pegawai V"]].rename(
    columns={"Nama Kantor": "Eselon II", "Eselon 3": "Eselon III", "Pegawai V": "Status"}
)
out = out.reset_index(drop=True)
out["Status"] = out["Status"].apply(lambda x: "✔ Sudah" if x == "Sudah" else "✘ Belum")

# Build HTML table manually to avoid dark-mode iframe issue
rows_html = ""
for i, (_, row) in enumerate(out.iterrows()):
    status_val = row["Status"]
    if "Sudah" in status_val:
        status_style = "color:#059669;font-weight:600"
    else:
        status_style = "color:#DC2626;font-weight:600"
    bg = "#F8FAFC" if i % 2 == 0 else WHITE
    rows_html += (
        f'<tr style="background:{bg};">'
        f'<td style="padding:10px 12px;color:{DARK};border:1px solid {BORDER};">{row["Eselon II"]}</td>'
        f'<td style="padding:10px 12px;color:{DARK};border:1px solid {BORDER};">{row["Eselon III"]}</td>'
        f'<td style="padding:10px 12px;color:{DARK};border:1px solid {BORDER};">{row["Nama Lengkap"]}</td>'
        f'<td style="padding:10px 12px;border:1px solid {BORDER};{status_style}">{status_val}</td>'
        f'</tr>'
    )

table_html = f"""
<div style="max-height:500px; overflow-y:auto; border:1px solid {BORDER}; border-radius:8px;">
<table style="width:100%; border-collapse:collapse; font-size:0.85rem; background:{WHITE};">
    <thead>
        <tr style="background:#E2E8F0; position:sticky; top:0; z-index:1;">
            <th style="padding:10px 12px; text-align:left; font-weight:600; color:{DARK}; border:1px solid {BORDER};">Eselon II</th>
            <th style="padding:10px 12px; text-align:left; font-weight:600; color:{DARK}; border:1px solid {BORDER};">Eselon III</th>
            <th style="padding:10px 12px; text-align:left; font-weight:600; color:{DARK}; border:1px solid {BORDER};">Nama Lengkap</th>
            <th style="padding:10px 12px; text-align:left; font-weight:600; color:{DARK}; border:1px solid {BORDER};">Status</th>
        </tr>
    </thead>
    <tbody>
        {rows_html}
    </tbody>
</table>
</div>
"""
st.markdown(table_html, unsafe_allow_html=True)

# ── Export ──────────────────────────────────────────────
st.markdown(f"<p style='color:{GRAY};font-size:0.9rem;margin:1rem 0 0.8rem'>Export data sesuai filter di atas.</p>", unsafe_allow_html=True)
e1, e2 = st.columns(2)
with e1:
    st.download_button("📥 Download Excel", export_excel(d_all), "monitoring_aktivasi.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    st.caption("Data Pegawai + Ringkasan per Eselon III")
with e2:
    st.download_button("📥 Download PDF", export_pdf(d_all), "monitoring_aktivasi.pdf",
                       mime="application/pdf", use_container_width=True)
    st.caption("Ringkasan + detail pegawai")
