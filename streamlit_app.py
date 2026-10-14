"""
Gangguan Analisis Ca pada Spektrofotometri Serapan Atom-Nyala (AAS)
Aplikasi Streamlit: membungkus aplikasi HTML interaktif (model 3D, kalkulator,
laporan praktikum) + generator QR code untuk membagikan aplikasi.
"""
from io import BytesIO
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE = Path(_file_).parent
HTML_FILE = BASE / "aas_ca.html"
DEFAULT_URL = "https://gangguan-ca-aas.streamlit.app"

st.set_page_config(
    page_title="Gangguan Ca pada AAS-Nyala",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Rapatkan margin agar aplikasi HTML tampil hampir penuh layar
st.markdown(
    """
    <style>
      .block-container{padding-top:1rem;padding-bottom:0;max-width:100%}
      header[data-testid="stHeader"]{background:transparent}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_html() -> str:
    return HTML_FILE.read_text(encoding="utf-8")


def make_qr_png(url: str, box_size: int = 10) -> bytes:
    import qrcode  # qrcode[pil]

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------- Sidebar: QR code ----------------
with st.sidebar:
    st.header("📱 QR Code")
    st.caption("Tempel URL aplikasi (setelah di-deploy) lalu scan dengan HP.")
    url = st.text_input("URL aplikasi", value=DEFAULT_URL)
    if url.strip():
        png = make_qr_png(url.strip())
        st.image(png, use_container_width=True)
        st.download_button(
            "⬇️ Unduh QR (PNG)", png, file_name="qr_aplikasi_aas_ca.png", mime="image/png"
        )
    st.divider()
    st.caption("Ca 422,7 nm · Lampu katoda berongga Ca · Nyala udara–asetilen")

# ---------------- Aplikasi utama ----------------
if not HTML_FILE.exists():
    st.error("File aas_ca.html tidak ditemukan. Pastikan berada satu folder dengan app.py.")
else:
    components.html(load_html(), height=950, scrolling=True)
