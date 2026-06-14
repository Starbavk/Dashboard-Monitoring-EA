import plotly.graph_objects as go
import pandas as pd

COLOR_OK = "#059669"
COLOR_NOT = "#DC2626"
COLOR_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_COLOR = "#111827"
GRID_COLOR = "#D1D5DB"


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
        textfont=dict(size=15, color=FONT_COLOR),
        cliponaxis=False,
        width=[0.45, 0.45],
        marker=dict(cornerradius=4),
    ))
    fig.update_layout(
        yaxis_title="Jumlah Pegawai",
        height=300,
        plot_bgcolor=COLOR_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, size=13),
        yaxis=dict(gridcolor=GRID_COLOR, automargin=True, showgrid=True,
                   tickfont=dict(size=12, color=FONT_COLOR),
                   title_font=dict(size=12, color=FONT_COLOR)),
        xaxis=dict(automargin=True, tickfont=dict(size=13, color=FONT_COLOR)),
        margin=dict(l=50, r=30, t=20, b=40),
        showlegend=False,
    )
    return fig


def chart_donut(df: pd.DataFrame) -> go.Figure:
    aktif = int((df["Pegawai V"] == "Sudah").sum())
    belum = int((df["Pegawai X"] == "Sudah").sum())
    total = aktif + belum

    fig = go.Figure(data=[go.Pie(
        labels=["Sudah Aktivasi", "Belum Aktivasi"],
        values=[aktif, belum],
        marker_colors=[COLOR_OK, COLOR_NOT],
        hole=0.6,
        textinfo="label+value",
        textposition="outside",
        textfont=dict(size=12, color=FONT_COLOR),
        pull=[0.02, 0],
        automargin=True,
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    )])
    fig.update_layout(
        height=420,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, size=13),
        showlegend=False,
        margin=dict(l=60, r=60, t=60, b=60),
        uniformtext_minsize=10,
        annotations=[dict(
            text=f"<b>{aktif}</b><br><span style='font-size:11px'>Sudah Aktivasi</span>",
            x=0.5, y=0.5, font=dict(size=22, color=FONT_COLOR),
            showarrow=False
        )],
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
        .sort_values("Aktif", ascending=True)
    )

    # Show top 10 by total for cleaner display
    if len(per_kantor) > 10:
        per_kantor = per_kantor.tail(10)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=per_kantor[group_col],
        x=per_kantor["Aktif"],
        name="Sudah",
        orientation="h",
        marker_color=COLOR_OK,
        text=per_kantor["Aktif"],
        textposition="outside",
        textfont=dict(size=12, color=FONT_COLOR),
        cliponaxis=False,
        marker=dict(cornerradius=3),
    ))
    fig.add_trace(go.Bar(
        y=per_kantor[group_col],
        x=per_kantor["Belum"],
        name="Belum",
        orientation="h",
        marker_color=COLOR_NOT,
        text=per_kantor["Belum"],
        textposition="outside",
        textfont=dict(size=12, color=FONT_COLOR),
        cliponaxis=False,
        marker=dict(cornerradius=3),
    ))
    fig.update_layout(
        barmode="group",
        height=max(320, len(per_kantor) * 36),
        plot_bgcolor=COLOR_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, size=12),
        xaxis=dict(gridcolor=GRID_COLOR, automargin=True, showgrid=True,
                   tickfont=dict(size=12, color=FONT_COLOR)),
        yaxis=dict(automargin=True, tickfont=dict(size=12, color=FONT_COLOR)),
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center",
                    font=dict(size=12, color=FONT_COLOR)),
        margin=dict(l=10, r=50, t=30, b=30),
        hovermode="y unified",
    )
    return fig
