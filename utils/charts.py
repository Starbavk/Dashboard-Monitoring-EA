import plotly.graph_objects as go
import pandas as pd

COLOR_OK = "#5BAF7B"
COLOR_NOT = "#E8836B"
COLOR_BG = "#FAFAFA"


def chart_overall(df: pd.DataFrame) -> go.Figure:
    aktif = int((df["Pegawai V"] == "Sudah").sum())
    belum = int((df["Pegawai X"] == "Sudah").sum())

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Pegawai",
        x=["Sudah Aktivasi", "Belum Aktivasi"],
        y=[aktif, belum],
        marker_color=[COLOR_OK, COLOR_NOT],
        text=[f"{aktif}", f"{belum}"],
        textposition="outside",
        textfont=dict(size=15, color="#333"),
        width=[0.5, 0.5],
    ))
    fig.update_layout(
        title=dict(text="Status Aktivasi Keseluruhan", font=dict(size=14, color="#333")),
        yaxis_title="Jumlah Pegawai",
        height=360,
        plot_bgcolor=COLOR_BG,
        paper_bgcolor="white",
        font=dict(color="#333"),
        yaxis=dict(gridcolor="#E8E8E8", title_font=dict(size=12, color="#333")),
        xaxis=dict(title_font=dict(size=12, color="#333")),
        margin=dict(l=40, r=20, t=40, b=30),
    )
    return fig


def chart_donut(df: pd.DataFrame) -> go.Figure:
    aktif = int((df["Pegawai V"] == "Sudah").sum())
    belum = int((df["Pegawai X"] == "Sudah").sum())

    fig = go.Figure(data=[go.Pie(
        labels=["Sudah Aktivasi", "Belum Aktivasi"],
        values=[aktif, belum],
        marker_colors=[COLOR_OK, COLOR_NOT],
        hole=0.55,
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(size=12),
        pull=[0.02, 0],
    )])
    fig.update_layout(
        title=dict(text="Komposisi Aktivasi", font=dict(size=14, color="#333")),
        height=360,
        paper_bgcolor="white",
        font=dict(color="#333"),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def chart_per_kantor(df: pd.DataFrame) -> go.Figure:
    group_col = "Eselon 3" if "Eselon 3" in df.columns else "Nama Kantor"
    per_kantor = (
        df.groupby(group_col)
        .agg(
            Total=("Nama Lengkap", "count"),
            Aktif=("Pegawai V", lambda x: (x == "Sudah").sum()),
            Belum=("Pegawai X", lambda x: (x == "Sudah").sum()),
        )
        .reset_index()
        .sort_values("Total", ascending=True)
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=per_kantor[group_col],
        x=per_kantor["Aktif"],
        name="Sudah Aktivasi",
        orientation="h",
        marker_color=COLOR_OK,
    ))
    fig.add_trace(go.Bar(
        y=per_kantor[group_col],
        x=per_kantor["Belum"],
        name="Belum Aktivasi",
        orientation="h",
        marker_color=COLOR_NOT,
    ))
    fig.update_layout(
        title=dict(text="Aktivasi per Eselon III", font=dict(size=14, color="#333")),
        barmode="group",
        xaxis_title="Jumlah Pegawai",
        height=max(320, len(per_kantor) * 32),
        plot_bgcolor=COLOR_BG,
        paper_bgcolor="white",
        font=dict(color="#333"),
        xaxis=dict(gridcolor="#E8E8E8", title_font=dict(size=12, color="#333")),
        yaxis=dict(title_font=dict(size=12, color="#333")),
        legend=dict(orientation="h", y=1.04, x=0.8, font=dict(size=11)),
        margin=dict(l=120, r=20, t=40, b=30),
    )
    return fig
