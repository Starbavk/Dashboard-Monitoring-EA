import plotly.graph_objects as go
import pandas as pd

FONT_COLOR = "#111827"
GRID_COLOR = "#D1D5DB"


def chart_top_bottom(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar: Top & Bottom 5 KPPN by activation percentage."""
    group_col = "Eselon 3" if "Eselon 3" in df.columns else "Nama Kantor"
    per = (
        df.groupby(group_col)
        .agg(
            Total=("Nama Lengkap", "count"),
            Aktif=("Pegawai V", lambda x: (x == "Sudah").sum()),
        )
        .reset_index()
    )
    per["Pct"] = (per["Aktif"] / per["Total"] * 100).round(1)

    top = per.nlargest(5, "Pct").sort_values("Pct", ascending=True)
    bot = per.nsmallest(5, "Pct").sort_values("Pct", ascending=True)

    combined = pd.concat([bot, top], ignore_index=True).drop_duplicates(subset=[group_col])
    combined = combined.sort_values("Pct", ascending=True)

    colors = ["#059669" if row[group_col] in top[group_col].values else "#DC2626" for _, row in combined.iterrows()]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=combined[group_col],
        x=combined["Pct"],
        orientation="h",
        marker_color=colors,
        text=combined.apply(lambda r: f"{r['Pct']:.1f}% ({int(r['Aktif'])}/{int(r['Total'])})", axis=1),
        textposition="outside",
        textfont=dict(size=11, color=FONT_COLOR),
        cliponaxis=False,
        marker=dict(cornerradius=3),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        height=max(340, len(combined) * 38),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_COLOR, size=12),
        xaxis=dict(
            gridcolor=GRID_COLOR, automargin=True, showgrid=True,
            tickfont=dict(size=11, color=FONT_COLOR),
            title_text="% Aktivasi",
            title_font=dict(size=11, color=FONT_COLOR),
            range=[0, 115],
        ),
        yaxis=dict(automargin=True, tickfont=dict(size=11, color=FONT_COLOR)),
        margin=dict(l=10, r=60, t=20, b=40),
        showlegend=False,
    )
    return fig


def chart_donut(df: pd.DataFrame) -> go.Figure:
    aktif = int((df["Pegawai V"] == "Sudah").sum())
    belum = int((df["Pegawai X"] == "Sudah").sum())

    fig = go.Figure(data=[go.Pie(
        labels=["Sudah Aktivasi", "Belum Aktivasi"],
        values=[aktif, belum],
        marker_colors=["#059669", "#DC2626"],
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
        paper_bgcolor="rgba(0,0,0,0)",
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

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=per_kantor[group_col],
        x=per_kantor["Aktif"],
        name="Sudah",
        orientation="h",
        marker_color="#059669",
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
        marker_color="#DC2626",
        text=per_kantor["Belum"],
        textposition="outside",
        textfont=dict(size=12, color=FONT_COLOR),
        cliponaxis=False,
        marker=dict(cornerradius=3),
    ))
    fig.update_layout(
        barmode="group",
        height=max(320, len(per_kantor) * 50),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
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
