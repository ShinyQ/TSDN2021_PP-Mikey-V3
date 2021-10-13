import streamlit as st
from views import home, covid

st.set_page_config(
    page_title='PP Mikey V3 - Turnamen Sains Data Nasional',
    page_icon='https://telkomuniversity.ac.id/wp-content/uploads/2019/07/cropped-favicon-2-32x32.png',
    layout='wide'
)

PAGES = {
    "🏠 Halaman Utama": home,
    "🏠 Sebaran COVID-19 Jakarta": covid,

}
st.sidebar.subheader('Navigasi')

page = st.sidebar.selectbox("Pindah Halaman", list(PAGES.keys()))
page = PAGES[page]
page.app()
