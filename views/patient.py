import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def make_it_easy(q1, q2, q3, q4, col_kontak_erat, col_probable, col_suspek):
    ans = []
    for i in range(0, len(col_kontak_erat)):
        q1_isolasi_rs_ke = q1[col_kontak_erat[i]].sum(axis=0)
        q1_isolasi_rs_prob = q1[col_probable[i]].sum(axis=0)
        q1_isolasi_rs_su = q1[col_suspek[i]].sum(axis=0)

        q2_isolasi_rs_ke = q2[col_kontak_erat[i]].sum(axis=0)
        q2_isolasi_rs_prob = q2[col_probable[i]].sum(axis=0)
        q2_isolasi_rs_su = q2[col_suspek[i]].sum(axis=0)

        q3_isolasi_rs_ke = q3[col_kontak_erat[i]].sum(axis=0)
        q3_isolasi_rs_prob = q3[col_probable[i]].sum(axis=0)
        q3_isolasi_rs_su = q3[col_suspek[i]].sum(axis=0)

        q4_isolasi_rs_ke = q4[col_kontak_erat[i]].sum(axis=0)
        q4_isolasi_rs_prob = q4[col_probable[i]].sum(axis=0)
        q4_isolasi_rs_su = q4[col_suspek[i]].sum(axis=0)

        ans.append((q1_isolasi_rs_ke, q1_isolasi_rs_prob, q1_isolasi_rs_su,
                    q2_isolasi_rs_ke, q2_isolasi_rs_prob, q2_isolasi_rs_su,
                    q3_isolasi_rs_ke, q3_isolasi_rs_prob, q3_isolasi_rs_su,
                    q4_isolasi_rs_ke, q4_isolasi_rs_prob, q4_isolasi_rs_su))
    return ans


def get_rs_or_house(q1, q2, q3, q4, col_isolasi_rs, col_isolasi_rumah):
    ans = []
    tot_isolasi_rs_q1 = 0
    tot_isolasi_rs_q2 = 0
    tot_isolasi_rs_q3 = 0
    tot_isolasi_rs_q4 = 0

    tot_isolasi_rmh_q1 = 0
    tot_isolasi_rmh_q2 = 0
    tot_isolasi_rmh_q3 = 0
    tot_isolasi_rmh_q4 = 0

    for i in range(0, len(col_isolasi_rs)):
        tot_isolasi_rs_q1 += q1[col_isolasi_rs[i]].sum(axis=0)
        tot_isolasi_rs_q2 += q2[col_isolasi_rs[i]].sum(axis=0)
        tot_isolasi_rs_q3 += q3[col_isolasi_rs[i]].sum(axis=0)
        tot_isolasi_rs_q4 += q4[col_isolasi_rs[i]].sum(axis=0)

    for i in range(0, len(col_isolasi_rumah)):
        tot_isolasi_rmh_q1 += q1[col_isolasi_rumah[i]].sum(axis=0)
        tot_isolasi_rmh_q2 += q2[col_isolasi_rumah[i]].sum(axis=0)
        tot_isolasi_rmh_q3 += q3[col_isolasi_rumah[i]].sum(axis=0)
        tot_isolasi_rmh_q4 += q4[col_isolasi_rumah[i]].sum(axis=0)

    isolasi_rs = (tot_isolasi_rs_q1, tot_isolasi_rs_q2,
                  tot_isolasi_rs_q3, tot_isolasi_rs_q4)
    isolasi_rmh = (tot_isolasi_rmh_q1, tot_isolasi_rmh_q2,
                   tot_isolasi_rmh_q3, tot_isolasi_rmh_q4)
    ans.append(isolasi_rs)
    ans.append(isolasi_rmh)
    return ans


def app():
    df = pd.read_excel("dataset/Data Academy_ED.xlsx", sheet_name="Data Suspek dll (Jakarta)")
    q1 = df[0:68].copy()
    q2 = df[68:136].copy()
    q3 = df[136:204].copy()
    q4 = df[204:273].copy()

    col_kontak_erat = ["Isolasi di RS (Kontak Erat)", "Isolasi di Rumah (Kontak Erat)",
                       "Meninggal (Kontak Erat)", "Selesai Isolasi (Kontak Erat)"]

    col_probable = ['Isolasi di RS (Probable)', 'Isolasi di Rumah (Probable)',
                    'Meninggal (Probable)', 'Selesai Isolasi (Probable)']

    col_suspek = ['Isolasi di RS (Suspek)', 'Isolasi di Rumah (Suspek)',
                  'Meninggal (Suspek)', 'Selesai Isolasi (Suspek)']

    col_isolasi_rs = ["Isolasi di RS (Kontak Erat)", "Isolasi di RS (Probable)", "Isolasi di RS (Suspek)"]
    col_isolasi_rumah = ["Isolasi di Rumah (Kontak Erat)", 'Isolasi di Rumah (Probable)', "Isolasi di Rumah (Suspek)"]

    ans_rs_or_house = get_rs_or_house(q1, q2, q3, q4, col_isolasi_rs, col_isolasi_rumah)

    rs = ans_rs_or_house[0]
    rumah = ans_rs_or_house[1]

    st.write("")
    st.write("#### Isolasi Kumulatif Quarter Jakarta (Januari - September 2021) ")

    status = ['1 Januari - 9 Maret', '10 Maret - 15 Mei', '16 Mei - 23 Juli', '24 Juli - 30 September']
    list_bar = [go.Bar(x=status, y=rs, name="Kumulatif Isolasi di Rumah Sakit", text=rs),
                go.Bar(x=status, y=rumah, name="Kumulatif Isolasi di Rumah", text=rumah)]

    fig = go.Figure(data=list_bar)
    fig.update_traces(textposition='outside', )
    fig.update_layout(barmode='group',
                      height=400,
                      title_x=0.5, width=1000,
                      margin=dict(l=20, r=0, t=20, b=0),
                      font=dict(size=14),
                      )

    st.plotly_chart(fig)

    ans = make_it_easy(q1, q2, q3, q4, col_kontak_erat, col_probable, col_suspek)

    rs = ans[0]
    rumah = ans[1]
    meninggal = ans[2]
    selesai = ans[3]

    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Isolasi Quarter Jakarta")
        status = ['1 Januari - 9 Maret', '10 Maret - 15 Mei', '16 Mei - 23 Juli', '24 Juli - 30 September']
        list_bar = [go.Bar(x=status, y=rs, name="Isolasi di Rumah Sakit", text=rs),
                    go.Bar(x=status, y=rumah, name="Isolasi di Rumah", text=rumah)]

        fig = go.Figure(data=list_bar)
        fig.update_traces(textposition='outside', )
        fig.update_layout(barmode='group', title_x=0.5,
                          width=500,
                          margin=dict(l=20, r=0, t=10, b=0),
                          legend=dict(
                              yanchor="top",
                              y=0.99,
                              xanchor="left",
                              x=0.01
                          )
                          )

        st.plotly_chart(fig)

    with col2:
        st.write("")
        st.write("")
        st.write("")

        status = ['1 Januari - 9 Maret', '10 Maret - 15 Mei', '16 Mei - 23 Juli', '24 Juli - 30 September']
        list_bar = [go.Bar(x=status, y=meninggal, name="Isolasi Meninggal", text=meninggal),
                    go.Bar(x=status, y=selesai, name="Isolasi Selesai", text=selesai)]

        fig = go.Figure(data=list_bar)
        fig.update_traces(textposition='outside', )
        fig.update_layout(barmode='group',
                          title_x=0.5, width=500,
                          margin=dict(l=20, r=0, t=10, b=0),
                          legend=dict(
                              yanchor="top",
                              y=0.99,
                              xanchor="left",
                              x=0.01
                          )
                          )

        st.plotly_chart(fig)

    df = pd.read_csv('dataset/Data Academy_ED_03.csv')
    df = df.dropna()

    total_tanpa_gejala = sum(df['Tanpa Gejala'])
    total_gejala = sum(df['Bergejala'])
    total_unknown = sum(df['Belum Ada Data'])

    segment_get_covid = [total_tanpa_gejala, total_gejala, total_unknown]

    total_isolation = sum(df['Self Isolation'])
    total_treat = sum(df['Masih Perawatan'])

    segment_patient_covid = [total_isolation, total_treat]

    st.text("")
    st.markdown("#### Jumlah Pasien Covid Jakarta 1 Januari - 30 September 2021")

    line_stat = [go.Scatter(x=df.Tanggal, y=df['Self Isolation'], name='Isolasi Mandiri', mode='lines'),
                 go.Scatter(x=df.Tanggal, y=df['Masih Perawatan'], name='Masih Dirawat', mode='lines')]

    fig = go.Figure(data=line_stat)
    fig.update_layout(
        margin=dict(l=20, r=0, t=20, b=20),
        width=1000,
        font=dict(size=14)
    )

    st.plotly_chart(fig)

    col1, col2 = st.columns(2)

    with col1:
        st.text("")
        st.markdown("#### Segmentasi Orang Yang Terkena COVID-19")
        name = ['Tanpa Gejala', 'Bergejala', 'Tidak Diketahui']

        fig = px.pie(
            values=segment_get_covid, names=name,
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.layout.showlegend = False
        fig.update_traces(textposition='inside', textinfo='percent+label+value')
        fig.update_layout(
            width=450,
            height=350,
            margin=dict(l=0, r=0, t=20, b=20),
            title_x=0.5,
            font=dict(size=14)
        )

        st.plotly_chart(fig)

    with col2:
        st.text("")
        st.markdown("#### Segmentasi Pasien Covid Jakarta")
        name = ['Isolasi Mandiri', 'Dalam Perawatan']

        fig = px.pie(
            values=segment_patient_covid, names=name,
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.layout.showlegend = False
        fig.update_traces(textposition='inside', textinfo='percent+label+value')
        fig.update_layout(
            width=450,
            height=350,
            margin=dict(l=0, r=0, t=20, b=20),
            title_x=0.5,
            font=dict(size=14)
        )

        st.plotly_chart(fig)
