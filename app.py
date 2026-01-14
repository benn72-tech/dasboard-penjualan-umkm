import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

st.title("📊 Dashboard Penjualan UMKM + Export Excel & PDF Lengkap")

uploaded_file = st.file_uploader("Upload file penjualan (CSV atau Excel)", type=["csv", "xlsx"])
logo_file = st.file_uploader("Upload logo UMKM (PNG/JPG)", type=["png","jpg","jpeg"])

# Pilihan tema warna
theme = st.selectbox("Pilih tema warna laporan:", ["Biru", "Hijau", "Merah"])

# Mapping warna sesuai tema
colors = {
    "Biru": {"harian": "#1f77b4", "cabang": "skyblue", "kasir": "#6699cc", "produk": "#3366cc"},
    "Hijau": {"harian": "#2ca02c", "cabang": "lightgreen", "kasir": "#228b22", "produk": "#006400"},
    "Merah": {"harian": "#d62728", "cabang": "salmon", "kasir": "#ff0000", "produk": "#8b0000"}
}
palette = colors[theme]

def safe_group_sum(df, by_col, val_col):
    if by_col not in df.columns or val_col not in df.columns or df.empty:
        return pd.DataFrame(columns=[by_col, val_col])
    out = df.groupby(by_col)[val_col].sum().reset_index()
    return out.sort_values(val_col, ascending=False)

def fig_to_buf(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    required_cols = ["Tanggal", "Produk", "Jumlah", "Harga", "Kasir", "Cabang"]
    if all(col in df.columns for col in required_cols):
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
        df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
        df["Harga"] = pd.to_numeric(df["Harga"], errors="coerce").fillna(0)
        df["Total"] = df["Jumlah"] * df["Harga"]

        st.subheader("Data Penjualan")
        st.dataframe(df)

        st.subheader("Ringkasan")
        st.metric("Total Penjualan (Rp)", f"{df['Total'].sum():,}")

        # --- Semua grafik di dashboard ---
        daily = df.dropna(subset=["Tanggal"]).groupby("Tanggal")["Total"].sum().reset_index()
        cabang_summary = safe_group_sum(df, "Cabang", "Total")
        kasir_summary = safe_group_sum(df, "Kasir", "Total")
        produk_summary = safe_group_sum(df, "Produk", "Total")

        # Grafik tren harian
        st.subheader("Grafik Penjualan Harian")
        fig1, ax1 = plt.subplots()
        if not daily.empty:
            ax1.plot(daily["Tanggal"], daily["Total"], marker="o", color=palette["harian"])
        ax1.set_xlabel("Tanggal"); ax1.set_ylabel("Total (Rp)")
        ax1.set_title("Tren Penjualan Harian")
        st.pyplot(fig1); plt.close(fig1)

        # Grafik bar per Cabang
        st.subheader("Grafik Penjualan per Cabang")
        fig2, ax2 = plt.subplots()
        if not cabang_summary.empty:
            ax2.bar(cabang_summary["Cabang"], cabang_summary["Total"], color=palette["cabang"])
            ax2.set_xticklabels(cabang_summary["Cabang"], rotation=30, ha="right")
        ax2.set_ylabel("Total (Rp)")
        ax2.set_title("Total Penjualan per Cabang")
        st.pyplot(fig2); plt.close(fig2)

        # Grafik bar per Kasir
        st.subheader("Grafik Penjualan per Kasir")
        fig3, ax3 = plt.subplots()
        if not kasir_summary.empty:
            ax3.bar(kasir_summary["Kasir"], kasir_summary["Total"], color=palette["kasir"])
            ax3.set_xticklabels(kasir_summary["Kasir"], rotation=30, ha="right")
        ax3.set_ylabel("Total (Rp)")
        ax3.set_title("Total Penjualan per Kasir")
        st.pyplot(fig3); plt.close(fig3)

        # Grafik pie per Produk
        st.subheader("Distribusi Penjualan per Produk")
        fig4, ax4 = plt.subplots()
        if not produk_summary.empty:
            ax4.pie(produk_summary["Total"], labels=produk_summary["Produk"], autopct="%1.1f%%", colors=[palette["produk"]]*len(produk_summary))
        ax4.set_title("Distribusi Penjualan per Produk")
        st.pyplot(fig4); plt.close(fig4)

        # --- Export ke Excel ---
        st.subheader("📥 Export Laporan ke Excel")
        def convert_df_to_excel(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                dataframe.to_excel(writer, index=False, sheet_name="Penjualan")
                cabang_summary.to_excel(writer, index=False, sheet_name="Ringkasan Cabang")
                kasir_summary.to_excel(writer, index=False, sheet_name="Ringkasan Kasir")
            return output.getvalue()

        excel_file = convert_df_to_excel(df)
        st.download_button(
            label="Download Laporan Excel",
            data=excel_file,
            file_name="laporan_penjualan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # --- Export ke PDF ---
        st.subheader("📥 Export Laporan ke PDF Lengkap")
        def convert_df_to_pdf(dataframe):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Logo di kanan atas
            if logo_file is not None:
                logo_bytes = logo_file.read()
                pdf.image(BytesIO(logo_bytes), x=160, y=10, w=35, type="PNG")

            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 10, txt="Laporan Penjualan UMKM", ln=True, align="C")

            pdf.set_font("Arial", size=11)
            total_penjualan = dataframe["Total"].sum()
            pdf.ln(5)
            pdf.cell(0, 8, txt=f"Total Penjualan: Rp {total_penjualan:,}", ln=True)

            # Ringkasan per Cabang
            pdf.ln(4)
            pdf.cell(0, 8, txt="Ringkasan per Cabang:", ln=True)
            for _, row in cabang_summary.iterrows():
                pdf.cell(0, 7, txt=f"- {row['Cabang']}: Rp {int(row['Total']):,}", ln=True)

            # Ringkasan per Kasir
            pdf.ln(4)
            pdf.cell(0, 8, txt="Ringkasan per Kasir:", ln=True)
            for _, row in kasir_summary.iterrows():
                pdf.cell(0, 7, txt=f"- {row['Kasir']}: Rp {int(row['Total']):,}", ln=True)

            # Tambahkan semua grafik ke PDF
            for fig in [fig1, fig2, fig3, fig4]:
                buf = fig_to_buf(fig)
                pdf.image(buf, x=10, y=None, w=180, type="PNG")

            pdf_bytes = bytes(pdf.output(dest="S"))
            return pdf_bytes

        pdf_file = convert_df_to_pdf(df)
        st.download_button(
            label="Download Laporan PDF Lengkap",
            data=pdf_file,
            file_name="laporan_penjualan.pdf",
            mime="application/pdf"
        )

    else:
        st.error("File harus punya kolom: Tanggal, Produk, Jumlah, Harga, Kasir, Cabang")
else:
    st.info("Silakan upload file CSV atau Excel penjualan untuk melihat dashboard.")
