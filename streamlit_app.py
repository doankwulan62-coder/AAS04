from io import BytesIO
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

HTML_FILE = Path(__file__).parent / "aas_ca.html"
DEFAULT_URL = "https://gangguan-ca-aas.streamlit.app"

st.set_page_config(
    page_title="Gangguan Ca pada AAS-Nyala",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    "<style>.block-container{padding-top:1rem;padding-bottom:0;max-width:100%}</style>",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_html():
    return HTML_FILE.read_text(encoding="utf-8")


def make_qr_png(url):
    import qrcode

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    buf = BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(buf, format="PNG")
    return buf.getvalue()


with st.sidebar:
    st.header("📱 QR Code")
    url = st.text_input("URL aplikasi", value=DEFAULT_URL)
    if url.strip():
        png = make_qr_png(url.strip())
        st.image(png, use_container_width=True)
        st.download_button("⬇️ Unduh QR (PNG)", png, file_name="qr_aas_ca.png", mime="image/png")

if not HTML_FILE.exists():
    st.error("File aas_ca.html tidak ditemukan di repo.")
else:
    components.html(load_html(), height=950, scrolling=True)
