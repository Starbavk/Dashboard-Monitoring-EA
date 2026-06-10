import streamlit as st
import pandas as pd
from utils.data_loader import load_excel, get_summary
from utils.charts import chart_overall, chart_donut, chart_per_kantor
from utils.export import export_excel, export_pdf

st.set_page_config(page_title="Monitoring Aktivasi Pegawai", page_icon="📊", layout="wide")

BLUE = "#69ACF1"
GREEN = "#5BAF7B"
RED = "#E8836B"
DARK = "#222222"
GRAY = "#555555"
LIGHT = "#F5F5F5"
WHITE = "#FFFFFF"

st.markdown(f"""
<style>
    .block-container {{ padding: 1.2rem 1.5rem !important; max-width: 100% !important; }}
    #root > div:first-child {{ background: {WHITE}; }}

    .app-header {{
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 1.2rem; padding-bottom: 0.8rem;
        border-bottom: 1px solid #E8E8E8;
    }}
    .app-header h1 {{ font-size: 1.3rem; font-weight: 600; color: {DARK}; margin: 0; }}
    .app-header span {{ font-size: 0.8rem; color: {GRAY}; }}

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

    .stTabs [data-baseweb="tab-list"] {{
        background: {WHITE}; border-bottom: 1px solid #E8E8E8; gap: 0; padding: 0;
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 0.5rem 1rem; font-size: 0.82rem; color: {GRAY};
        border-bottom: 2px solid transparent;
    }}
    .stTabs [aria-selected="true"] {{
        color: {DARK} !important; border-bottom-color: {BLUE} !important;
        font-weight: 600;
    }}

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
    <h1>Monitoring Aktivasi Media Sosial Pegawai</h1>
    <span>Kementerian Keuangan · DJPb</span>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────
with st.sidebar:
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

# ── Load data — only once per file ──────────────────────
if "data" not in st.session_state:
    st.session_state["data"] = None

if uploaded_file is not None and st.session_state.get("uploaded_name") != uploaded_file.name:
    try:
        uploaded_file.seek(0)
        df = load_excel(uploaded_file)
        st.session_state["data"] = df
        st.session_state["uploaded_name"] = uploaded_file.name
        st.rerun()
    except Exception as e:
        st.error(f"Gagal memuat: {e}")

df = st.session_state["data"]

if df is None:
    st.markdown(f"""
    <div style="text-align:center; padding:4rem 1rem; background:{LIGHT}; border-radius:8px;">
        <div style="font-size:3rem; margin-bottom:0.5rem;">📊</div>
        <h3 style="color:{GRAY}; font-weight:500;">Upload file Excel di sidebar untuk memulai</h3>
        <p style="color:#AAAAAA; font-size:0.9rem;">File export dari Dashboard Aktivasi</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

summary = get_summary(df)

# ── Cards ───────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='card'><div class='card-label'>Total Pegawai</div><div class='card-value'>{summary['total']}</div><div class='card-footer'>{df['Eselon 3'].nunique()} unit eselon III</div></div>", unsafe_allow_html=True)
with c2:
    pct = f"{summary['aktif']/summary['total']*100:.1f}%" if summary['total'] else "0%"
    st.markdown(f"<div class='card green'><div class='card-label'>Sudah Aktivasi</div><div class='card-value'>{summary['aktif']}</div><div class='card-footer'>{pct} dari total</div></div>", unsafe_allow_html=True)
with c3:
    pct = f"{summary['belum']/summary['total']*100:.1f}%" if summary['total'] else "0%"
    st.markdown(f"<div class='card red'><div class='card-label'>Belum Aktivasi</div><div class='card-value'>{summary['belum']}</div><div class='card-footer'>{pct} dari total</div></div>", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────
t1, t2, t3 = st.tabs(["📈 Dashboard", "📋 Data Pegawai", "📤 Export"])

with t1:
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1: st.plotly_chart(chart_overall(df), use_container_width=True, key="dash_bar")
    with col_ch2: st.plotly_chart(chart_donut(df), use_container_width=True, key="dash_donut")
    st.plotly_chart(chart_per_kantor(df), use_container_width=True, key="dash_per_es3")

with t2:
    es3_list = sorted(df["Eselon 3"].dropna().unique())

    col_f1, col_f2 = st.columns([0.15, 0.85])
    with col_f1:
        select_all = st.checkbox("Pilih Semua", value=True, key="sa")
    with col_f2:
        if select_all:
            selected_units = es3_list
            st.multiselect("Unit", es3_list, default=es3_list, key="t2es3_dummy", disabled=True, label_visibility="collapsed")
        else:
            selected_units = st.multiselect("Unit", es3_list, key="t2es3")

    d_filter = df[df["Eselon 3"].isin(selected_units)] if selected_units else df
    sum_f = get_summary(d_filter)

    mc1, mc2, mc3 = st.columns(3)
    with mc1: st.markdown(f"<div class='metric-box'><div class='lbl'>Total</div><div class='val'>{sum_f['total']}</div></div>", unsafe_allow_html=True)
    with mc2: st.markdown(f"<div class='metric-box'><div class='lbl'>Sudah Aktivasi</div><div class='val' style='color:{GREEN}'>{sum_f['aktif']}</div></div>", unsafe_allow_html=True)
    with mc3: st.markdown(f"<div class='metric-box'><div class='lbl'>Belum Aktivasi</div><div class='val' style='color:{RED}'>{sum_f['belum']}</div></div>", unsafe_allow_html=True)

    col_ch_a, col_ch_b = st.columns(2)
    with col_ch_a: st.plotly_chart(chart_overall(d_filter), use_container_width=True, key="data_bar")
    with col_ch_b: st.plotly_chart(chart_donut(d_filter), use_container_width=True, key="data_donut")

    st.plotly_chart(chart_per_kantor(d_filter), use_container_width=True, key="data_per_es3")

    cf1, cf2, cf3 = st.columns(3)
    with cf1: f_st = st.selectbox("Status", ["Semua", "Sudah Aktivasi", "Belum Aktivasi"], key="t2st")
    with cf2: f_nm = st.text_input("Cari Nama", placeholder="Ketik nama...", key="t2nm")
    with cf3: st.markdown(f"<div style='padding-top:1.5rem;color:#666;font-size:0.82rem'>{len(d_filter)} pegawai</div>", unsafe_allow_html=True)

    d_all = d_filter.copy()
    if f_st == "Sudah Aktivasi": d_all = d_all[d_all["Pegawai V"] == "Sudah"]
    elif f_st == "Belum Aktivasi": d_all = d_all[d_all["Pegawai X"] == "Sudah"]
    if f_nm: d_all = d_all[d_all["Nama Lengkap"].str.contains(f_nm, case=False, na=False)]

    out = d_all[["Nama Kantor", "Eselon 3", "Nama Lengkap", "Pegawai V"]].rename(
        columns={"Nama Kantor": "Eselon II", "Eselon 3": "Eselon III", "Pegawai V": "Status"}
    )
    out["Status"] = out["Status"].apply(lambda x: "✔ Sudah" if x == "Sudah" else "✘ Belum")
    st.dataframe(out, use_container_width=True, hide_index=True)

with t3:
    st.markdown(f"<p style='color:{GRAY};font-size:0.9rem;margin-bottom:0.8rem'>Export data sesuai filter Eselon III yang aktif.</p>", unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    with e1:
        st.download_button("📥 Download Excel", export_excel(df), "monitoring_aktivasi.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        st.caption("Data Pegawai + Ringkasan per Eselon III")
    with e2:
        st.download_button("📥 Download PDF", export_pdf(df), "monitoring_aktivasi.pdf", mime="application/pdf", use_container_width=True)
        st.caption("Ringkasan + detail pegawai")
