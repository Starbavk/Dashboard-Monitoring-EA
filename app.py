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

BLUE = "#69ACF1"
GREEN = "#5BAF7B"
RED = "#E8836B"
DARK = "#222222"
GRAY = "#555555"
LIGHT = "#F5F5F5"
WHITE = "#FFFFFF"

st.markdown(f"""
<style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
    [data-testid="stHeader"], [data-testid="stBottomBlockContainer"] {{
        background: {WHITE} !important;
    }}
    [data-testid="stSidebar"] {{ background: {WHITE} !important; }}
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
    .stMarkdown, [data-testid="stMarkdownContainer"] {{
        color: {DARK};
    }}
    [data-testid="stHeader"] {{ border-bottom: none; }}

    /* Input, select, multiselect widgets -> light */
    [data-baseweb="select"] > div, [data-baseweb="input"] > div,
    [data-baseweb="base-input"], .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {{
        background: {WHITE} !important; color: {DARK} !important;
        border-color: #D0D0D0 !important;
    }}
    [data-baseweb="tag"] {{
        background: {LIGHT} !important; color: {DARK} !important;
    }}
    [data-baseweb="tag"] span {{ color: {DARK} !important; }}
    [data-baseweb="popover"] li, [data-baseweb="menu"] li {{
        background: {WHITE} !important; color: {DARK} !important;
    }}
    [data-baseweb="popover"] ul, [data-baseweb="menu"] ul {{ background: {WHITE} !important; }}
    div[data-testid="stDataFrame"] {{ background: {WHITE} !important; }}

    /* File uploader -> light */
    [data-testid="stFileUploader"], [data-testid="stFileUploaderDropzone"],
    section[data-testid="stFileUploaderDropzone"] {{
        background: {LIGHT} !important; color: {DARK} !important;
        border: 1px dashed #C8C8C8 !important;
    }}
    [data-testid="stFileUploaderDropzone"] * {{ color: {DARK} !important; }}

    /* Buttons -> light */
    .stButton > button, [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"], [data-testid="baseButton-secondary"] {{
        background: {WHITE} !important; color: {DARK} !important;
        border: 1px solid #D0D0D0 !important;
    }}
    .stButton > button:hover {{ border-color: {BLUE} !important; color: {BLUE} !important; }}
    .stButton > button p, .stButton > button span {{ color: inherit !important; }}

    .block-container {{ padding: 1.2rem 1.5rem !important; max-width: 100% !important; }}
    #root > div:first-child {{ background: {WHITE}; }}

    .app-header {{
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 1.2rem; padding-bottom: 0.8rem;
        border-bottom: 1px solid #E8E8E8;
    }}
    .app-header .left {{ display: flex; flex-direction: column; gap: 0; }}
    .app-header h1 {{ font-size: 1.3rem; font-weight: 600; color: {DARK}; margin: 0; line-height: 1.2; }}
    .app-header .sub {{ font-size: 1.1rem; font-weight: 600; color: {DARK}; margin: 0; line-height: 1.2; }}
    .app-header .right {{ display: flex; align-items: center; gap: 10px; }}
    .app-header .right img {{ height: 38px; width: auto; object-fit: contain; }}
    .app-header .right img.logo-kiri {{ height: 65px; }}
    .app-header .right img.logo-kanan {{ height: 28px; }}

    .card {{
        background: {WHITE}; border-radius: 6px; padding: 1rem 1.2rem;
        border: 1px solid #E8E8E8; border-left: 4px solid {BLUE};
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }}
    .card.green {{ border-left-color: {GREEN}; }}
    .card.red {{ border-left-color: {RED}; }}
    .card.gold {{ border-left-color: #F0C060; }}
    .card-label {{ font-size: 0.75rem; color: {GRAY}; margin-bottom: 0.15rem; }}
    .card-value {{ font-size: 1.7rem; font-weight: 700; color: {DARK}; }}
    .card-footer {{ font-size: 0.75rem; color: #666666; margin-top: 0.2rem; }}

    section[data-testid="stSidebar"] > div:first-child {{
        background: {WHITE}; border-right: 1px solid #E8E8E8;
    }}
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px;
        color: {GRAY}; font-weight: 600;
    }}

    .badge {{
        display: inline-block; padding: 2px 10px; border-radius: 3px;
        font-size: 0.75rem; font-weight: 500;
    }}
    .badge-ok {{ background: #E4F3E8; color: #2D6A4F; }}
    .badge-not {{ background: #F8E6E2; color: #9B3A2A; }}

    .stDownloadButton button {{
        background: {WHITE} !important; color: {DARK} !important;
        border: 1px solid #D0D0D0 !important; border-radius: 4px !important;
        font-size: 0.85rem !important;
    }}
    .stDownloadButton button:hover {{
        border-color: {BLUE} !important; color: {BLUE} !important;
    }}

    .metric-box {{
        background: {WHITE}; border: 1px solid #E8E8E8; border-radius: 6px;
        padding: 0.7rem 1rem; text-align: center;
    }}
    .metric-box .lbl {{ font-size: 0.7rem; color: {GRAY}; text-transform: uppercase; letter-spacing: 0.3px; }}
    .metric-box .val {{ font-size: 1.4rem; font-weight: 700; color: {DARK}; }}

    div[data-testid="stDataFrame"] {{ font-size: 0.82rem; }}
    .stCaption, .stMarkdown p, .stMarkdown li, label, .stSelectbox label, .stMultiSelect label {{
        color: #333333 !important;
    }}
    section[data-testid="stSidebar"] .stCaption {{
        color: #444444 !important;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="app-header">
    <div class="left">
        <h1>Dashboard Monitoring Aktivasi Employee Advocacy</h1>
        <div class="sub">Kanwil DJPb Provinsi Jawa Barat</div>
    </div>
    <div class="right">
        <img class="logo-kiri" src="data:image/png;base64,{logo_djpb}" alt="DJPb">
        <img class="logo-kanan" src="data:image/png;base64,{logo_intress}" alt="InTress">
    </div>
</div>
""", unsafe_allow_html=True)

col_sub = st.columns([0.4, 0.6])
with col_sub[0]:
    edisi_sekarang = data_store.load_edisi()
    if st.session_state.get("role") == "Admin" and st.session_state.get("admin_auth", False):
        baru = st.text_input("Edisi EA", value=edisi_sekarang, key="edisi", placeholder="Contoh: EA-06-APBN KiTa Juni 2026")
        if baru != edisi_sekarang:
            data_store.save_edisi(baru)
            st.rerun()
    else:
        if edisi_sekarang:
            st.markdown(f"<div style='font-size:0.9rem;color:{GRAY};margin-top:0.3rem'><strong>Edisi EA:</strong> {edisi_sekarang}</div>", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    if "data" in st.session_state and st.session_state["data"] is not None:
        st.checkbox("Pilih Semua", value=True, key="sa")
        es3_list = sorted(st.session_state["data"]["Eselon 3"].dropna().unique())
        if st.session_state.get("sa", True):
            st.multiselect("Unit", es3_list, default=es3_list, key="es3_dummy", disabled=True, label_visibility="collapsed")
        else:
            st.multiselect("Unit", es3_list, key="es3")
        st.divider()

    st.radio("Mode", ["Admin", "User"], index=1, key="role")

    if st.session_state["role"] == "Admin":
        if not st.session_state.get("admin_auth", False):
            st.markdown("### Login Admin")
            user = st.text_input("Username", key="login_user")
            pwd = st.text_input("Password", type="password", key="login_pwd")
            if st.button("Login", use_container_width=True):
                if user == "admin" and pwd == "djpb89":
                    st.session_state["admin_auth"] = True
                    st.rerun()
                else:
                    st.error("Username atau password salah")
            uploaded_file = None
        else:
            st.markdown("### Upload")
            uploaded_file = st.file_uploader("File Excel", type=["xlsx"], label_visibility="collapsed")

            if uploaded_file is not None and st.button("Reset", use_container_width=True):
                for k in ["data", "uploaded_name"]:
                    if k in st.session_state: del st.session_state[k]
                st.rerun()

            if "data" in st.session_state and st.session_state["data"] is not None:
                df_s = st.session_state["data"]
                st.caption(f"**{len(df_s)}** pegawai · **{df_s['Eselon 3'].nunique()}** unit")
            else:
                st.caption("Upload file Excel (.xlsx) dari Dashboard Aktivasi")

            if st.button("Logout", use_container_width=True):
                del st.session_state["admin_auth"]
                st.rerun()
    else:
        uploaded_file = None
        if data_store.exists():
            st.caption("Mode User — hanya melihat data")
        else:
            st.caption("Mode User — menunggu admin upload data")

# ── Load data ──────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state["data"] = None

# Admin upload flow
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

# Load from persistent store if session is empty but file exists
if st.session_state["data"] is None and data_store.exists():
    st.session_state["data"] = data_store.load()
    st.rerun()

df = st.session_state["data"]

if df is None:
    if st.session_state["role"] == "Admin" and not st.session_state.get("admin_auth", False):
        msg = "Login sebagai Admin untuk upload data"
    elif st.session_state["role"] == "Admin":
        msg = "Upload file Excel di sidebar untuk memulai"
    else:
        msg = "Admin belum mengupload data. Silakan tunggu."
    st.markdown(f"""
    <div style="text-align:center; padding:4rem 1rem; background:{LIGHT}; border-radius:8px;">
        <div style="font-size:3rem; margin-bottom:0.5rem;">📊</div>
        <h3 style="color:{GRAY}; font-weight:500;">{msg}</h3>
        <p style="color:#AAAAAA; font-size:0.9rem;">File export dari Dashboard Aktivasi</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Ambil filter dari sidebar ──────────────────────────
es3_list = sorted(df["Eselon 3"].dropna().unique())

if st.session_state.get("sa", True):
    selected_units = st.session_state.get("es3_dummy", es3_list)
else:
    selected_units = st.session_state.get("es3", es3_list)

d_filter = df[df["Eselon 3"].isin(selected_units)] if selected_units else df
sum_f = get_summary(d_filter)

# ── Cards ───────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='card'><div class='card-label'>Total Pegawai</div><div class='card-value'>{sum_f['total']}</div><div class='card-footer'>{d_filter['Eselon 3'].nunique()} unit eselon III</div></div>", unsafe_allow_html=True)
with c2:
    pct = f"{sum_f['aktif']/sum_f['total']*100:.1f}%" if sum_f['total'] else "0%"
    st.markdown(f"<div class='card green'><div class='card-label'>Sudah Aktivasi</div><div class='card-value'>{sum_f['aktif']}</div><div class='card-footer'>{pct} dari total</div></div>", unsafe_allow_html=True)
with c3:
    pct = f"{sum_f['belum']/sum_f['total']*100:.1f}%" if sum_f['total'] else "0%"
    st.markdown(f"<div class='card red'><div class='card-label'>Belum Aktivasi</div><div class='card-value'>{sum_f['belum']}</div><div class='card-footer'>{pct} dari total</div></div>", unsafe_allow_html=True)

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
with col_ch_a: st.plotly_chart(chart_overall(d_filter), use_container_width=True, key="ch_bar", config=CHART_CONFIG)
with col_ch_b: st.plotly_chart(chart_donut(d_filter), use_container_width=True, key="ch_donut", config=CHART_CONFIG)
st.plotly_chart(chart_per_kantor(d_filter), use_container_width=True, key="ch_per_es3", config=CHART_CONFIG)

# ── Table ───────────────────────────────────────────────
st.divider()
cf1, cf2, cf3 = st.columns(3)
with cf1: f_st = st.selectbox("Status", ["Semua", "Sudah Aktivasi", "Belum Aktivasi"], key="st_flt")
with cf2: f_nm = st.text_input("Cari Nama", placeholder="Ketik nama...", key="nm_flt")
with cf3: st.markdown(f"<div style='padding-top:1.5rem;color:#666;font-size:0.82rem'>{len(d_filter)} pegawai</div>", unsafe_allow_html=True)

d_all = d_filter.copy()
if f_st == "Sudah Aktivasi": d_all = d_all[d_all["Pegawai V"] == "Sudah"]
elif f_st == "Belum Aktivasi": d_all = d_all[d_all["Pegawai X"] == "Sudah"]
if f_nm: d_all = d_all[d_all["Nama Lengkap"].str.contains(f_nm, case=False, na=False)]

out = d_all[["Nama Kantor", "Eselon 3", "Nama Lengkap", "Pegawai V"]].rename(
    columns={"Nama Kantor": "Eselon II", "Eselon 3": "Eselon III", "Pegawai V": "Status"}
)
out["Status"] = out["Status"].apply(lambda x: "✔ Sudah" if x == "Sudah" else "✘ Belum")

def _warnai_status(val):
    return "color: #2D6A4F; font-weight: 600" if "Sudah" in val else "color: #9B3A2A; font-weight: 600"

styled = out.style.map(_warnai_status, subset=["Status"])
st.dataframe(styled, use_container_width=True, hide_index=True)

# ── Export ──────────────────────────────────────────────
st.divider()
st.markdown(f"<p style='color:{GRAY};font-size:0.9rem;margin-bottom:0.8rem'>Export data sesuai filter di atas.</p>", unsafe_allow_html=True)
e1, e2 = st.columns(2)
with e1:
    st.download_button("📥 Download Excel", export_excel(d_filter), "monitoring_aktivasi.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    st.caption("Data Pegawai + Ringkasan per Eselon III")
with e2:
    st.download_button("📥 Download PDF", export_pdf(d_filter), "monitoring_aktivasi.pdf", mime="application/pdf", use_container_width=True)
    st.caption("Ringkasan + detail pegawai")
