import pandas as pd
from io import BytesIO
from fpdf import FPDF


def export_excel(df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export_df = df.rename(columns={
            "Pegawai V": "Status Aktivasi",
        })
        cols = [c for c in ["Eselon 3", "Nama Kantor", "Nama Lengkap", "Status Aktivasi"] if c in export_df.columns]
        export_df = export_df[cols]
        export_df.to_excel(writer, index=False, sheet_name="Data Pegawai")

        group_col = "Eselon 3" if "Eselon 3" in df.columns else "Nama Kantor"
        summary = (
            df.groupby(group_col)
            .agg(
                Total=("Nama Lengkap", "count"),
                Sudah_Aktivasi=("Pegawai V", lambda x: (x == "Sudah").sum()),
                Belum_Aktivasi=("Pegawai X", lambda x: (x == "Sudah").sum()),
            )
            .reset_index()
        )
        summary.to_excel(writer, index=False, sheet_name="Ringkasan per Eselon III")
    output.seek(0)
    return output


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Monitoring Aktivasi Media Sosial", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Halaman {self.page_no()}/{{nb}}", align="C")


def export_pdf(df: pd.DataFrame) -> BytesIO:
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    total = len(df)
    aktif = int((df["Pegawai V"] == "Sudah").sum())
    belum = int((df["Pegawai X"] == "Sudah").sum())

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Ringkasan Keseluruhan", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Total Pegawai: {total}", ln=True)
    pdf.cell(0, 8, f"Sudah Aktivasi: {aktif} ({aktif/total*100:.1f}%)" if total else str(aktif), ln=True)
    pdf.cell(0, 8, f"Belum Aktivasi: {belum} ({belum/total*100:.1f}%)" if total else str(belum), ln=True)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Ringkasan per Eselon III", ln=True)

    group_col = "Eselon 3" if "Eselon 3" in df.columns else "Nama Kantor"
    per_kantor = (
        df.groupby(group_col)
        .agg(
            Total=("Nama Lengkap", "count"),
            Aktif=("Pegawai V", lambda x: (x == "Sudah").sum()),
            Belum=("Pegawai X", lambda x: (x == "Sudah").sum()),
        )
        .reset_index()
    )

    pdf.set_font("Helvetica", "B", 9)
    col_widths = [60, 20, 30, 30]
    label = "Eselon III" if "Eselon 3" in df.columns else "Kantor"
    headers = [label, "Total", "Sudah Aktivasi", "Belum Aktivasi"]
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for _, row in per_kantor.iterrows():
        pdf.cell(col_widths[0], 7, str(row[group_col])[:35], border=1)
        pdf.cell(col_widths[1], 7, str(row["Total"]), border=1, align="C")
        pdf.cell(col_widths[2], 7, str(row["Aktif"]), border=1, align="C")
        pdf.cell(col_widths[3], 7, str(row["Belum"]), border=1, align="C")
        pdf.ln()

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Detail Pegawai", ln=True)

    has_es3 = "Eselon 3" in df.columns
    if has_es3:
        cols = [55, 40, 30, 30]
        headers2 = ["Eselon III", "Nama Lengkap", "Status Aktivasi"]
    else:
        cols = [50, 40, 30]
        headers2 = ["Nama Kantor", "Nama Lengkap", "Status Aktivasi"]
    pdf.set_font("Helvetica", "B", 8)
    for i, h in enumerate(headers2):
        pdf.cell(cols[i], 7, h, border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    for _, row in df.iterrows():
        status = "Sudah" if row["Pegawai V"] == "Sudah" else "Belum"
        if has_es3:
            pdf.cell(cols[0], 6, str(row["Eselon 3"])[:30], border=1)
            pdf.cell(cols[1], 6, str(row["Nama Lengkap"])[:22], border=1)
            pdf.cell(cols[2], 6, status, border=1, align="C")
        else:
            pdf.cell(cols[0], 6, str(row["Nama Kantor"])[:28], border=1)
            pdf.cell(cols[1], 6, str(row["Nama Lengkap"])[:22], border=1)
            pdf.cell(cols[2], 6, status, border=1, align="C")
        pdf.ln()

    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return output
