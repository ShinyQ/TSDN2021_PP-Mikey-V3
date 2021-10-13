import streamlit as st


def app():
    st.markdown("# Halaman Utama")
    st.image('https://dataacademy.co.id/wp-content/uploads/2021/10/anner-tsdn-new@3x-2048x540.png')
    st.write("""
        <div style="text-align:justify;">
            Turnamen Sains Data 2021 (TSDN 2021) adalah kompetisi data science/datathon berskala nasional
            yang ditujukan bagi para Penggiat Sains Data ataupun Pemerhati Data (Data Enthusiast). 
            Seluruh peserta akan diberi tantangan untuk dapat mengidentifikasi pertanyaan atau tantangan bisnis 
            terkini menjadi sebuah solusi analitis, bekerja sama untuk membuat kerangka solusi berbasis data 
            menggunakan perangkat lunak pemrograman dan visualisasi dengan tujuan untuk meningkatkan kinerja bisnis 
            dan menciptakan peluang baru yang dapat di implementasikan dalam kasus nyata.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## **Latar Belakang**")

    col1, col2 = st.columns(2)

    with col2:
        st.image('image/latarbelakang.png', width=450)

    with col1:
        st.write("""
            <div style="text-align:justify; margin-bottom: 1%">
                DKI Jakarta adalah suatu kota metropolitan yang padat penduduk dan memiliki mobilitas yang tinggi 
                mengakibatkan virus Covid-19 berkembang begitu cepat. Usaha demi usaha dikeluarkan oleh 
                pemerintah guna menekan persebaran Virus Covid-19.
                <br><br>
                Namun, dari usaha yang dikeluarkan pemerintah tentu memiliki efektifitas yang berbeda - beda.
                Tujuan dari studi ini adalah memahami efektifitas penanganan Covid-19 di Jakarta sehingga dapat 
                dijadikan bahan acuan dalam memberikan kebijakan dimasa yang akan datang.
            </div>
        """, unsafe_allow_html=True)
