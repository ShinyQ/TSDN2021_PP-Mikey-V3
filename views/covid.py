import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def slice_month(month):
    return int(month[4])


def app():
    st.markdown("### Dataset Yang Digunakan")
    df = pd.read_csv('dataset/Data Academy_ED_03.csv')
    df = df.dropna()
    st.write(df.tail(5))

    df['Tanggal'] = df['Tanggal'].astype('str')
    df['Meninggal Harian'] = df['Meninggal Harian'].astype(int)
    df['Sembuh Harian'] = df['Sembuh Harian'].astype(int)
    df['Positif Harian'] = df['Positif Harian'].astype(int)
    df['Month'] = df['Tanggal'].apply(slice_month)

    st.markdown("#### Kasus Covid Jakarta 1 Januari - 30 September 2021")

    line_stat = [go.Scatter(x=df.Tanggal, y=df['Positif Harian'], name='Positif Harian', mode='lines'),
                 go.Scatter(x=df.Tanggal, y=df['Sembuh Harian'], name='Sembuh Harian', mode='lines'),
                 go.Scatter(x=df.Tanggal, y=df['Meninggal Harian'], name='Meninggal Harian', mode='lines')]

    fig = go.Figure(data=line_stat)
    fig.update_layout(
        margin=dict(l=20, r=0, t=20, b=20),
        width=1000,
    )
    st.plotly_chart(fig)

    st.text("")
    st.markdown("#### Jumlah Pasien Covid Jakarta 1 Januari - 30 September 2021")

    line_stat = [go.Scatter(x=df.Tanggal, y=df['Self Isolation'], name='Isolasi Mandiri', mode='lines'),
                 go.Scatter(x=df.Tanggal, y=df['Masih Perawatan'], name='Masih Dirawat', mode='lines')]

    fig = go.Figure(data=line_stat)
    fig.update_layout(
        margin=dict(l=20, r=0, t=20, b=20),
        width=1000,
    )

    st.plotly_chart(fig)

    total_tanpa_gejala = sum(df['Tanpa Gejala'])
    total_gejala = sum(df['Bergejala'])
    total_unknown = sum(df['Belum Ada Data'])

    segment_get_covid = [total_tanpa_gejala, total_gejala, total_unknown]

    total_isolation = sum(df['Self Isolation'])
    total_treat = sum(df['Masih Perawatan'])

    segment_patient_covid = [total_isolation, total_treat]

    col1, col2 = st.columns(2)

    with col1:
        st.text("")
        st.markdown("##### Segmentasi Orang Yang Terkena COVID-19")
        name = ['Tanpa Gejala', 'Bergejala', 'Tidak Diketahui']

        fig = px.pie(
            values=segment_get_covid, names=name,
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.layout.showlegend = False
        fig.update_traces(textposition='inside', textinfo='percent+label+value')
        fig.update_layout(
            width=450,
            height=300,
            margin=dict(l=0, r=0, t=20, b=20),
            title_x=0.5
        )

        st.plotly_chart(fig)

    with col2:
        st.text("")
        st.markdown("##### Segmentasi Pasien Covid Jakarta")
        name = ['Isolasi Mandiri', 'Dalam Perawatan']

        fig = px.pie(
            values=segment_patient_covid, names=name,
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.layout.showlegend = False
        fig.update_traces(textposition='inside', textinfo='percent+label+value')
        fig.update_layout(
            width=450,
            height=300,
            margin=dict(l=0, r=0, t=20, b=20),
            title_x=0.5
        )

        st.plotly_chart(fig)

    st.text("")
    st.markdown("#### Pembagian Quarter Data COVID-19 Jakarta (Januari - September 2021)")

    q1 = df[0:68]
    q2 = df[68:136]
    q3 = df[136:204]
    q4 = df[204:273]

    q1_cov = sum(q1['Positif Harian'])
    q1_rec = sum(q1['Sembuh Harian'])
    q1_mor = sum(q1['Meninggal Harian'])

    q2_cov = sum(q2['Positif Harian'])
    q2_rec = sum(q2['Sembuh Harian'])
    q2_mor = sum(q2['Meninggal Harian'])

    q3_cov = sum(q3['Positif Harian'])
    q3_rec = sum(q3['Sembuh Harian'])
    q3_mor = sum(q3['Meninggal Harian'])

    q4_cov = sum(q4['Positif Harian'])
    q4_rec = sum(q4['Sembuh Harian'])
    q4_mor = sum(q4['Meninggal Harian'])

    status = ['1 Januari - 9 Maret', '10 Maret - 15 Mei', '16 Mei - 23 Juli', '24 Juli - 30 September']

    fig = go.Figure(data=[
        go.Bar(name='Positif', x=status, y=[q1_cov, q2_cov, q3_cov, q4_cov], text=[q1_cov, q2_cov, q3_cov, q4_cov]),
        go.Bar(name='Sembuh', x=status, y=[q1_rec, q2_rec, q3_rec, q4_rec], text=[q1_rec, q2_rec, q3_rec, q4_rec]),
        go.Bar(name='Meninggal', x=status, y=[q1_mor, q2_mor, q3_mor, q4_mor], text=[q1_mor, q2_mor, q3_mor, q4_mor]),
    ])

    fig.update_traces(textposition='outside')
    fig.update_layout(
        barmode='group', title_x=0.5,
        margin=dict(l=20, r=0, t=20, b=20),
        width=1000,
    )

    st.plotly_chart(fig)
    st.text("")
    st.markdown("#### Jumlah Sebaran COVID-19 Jakarta Bulan Januari - September 2021")

    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=("Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September"),
        horizontal_spacing=0.05, vertical_spacing=0.1
    )

    counter = 1

    for i in range(1, 4):
        for j in range(1, 4):
            monthly_case = df.loc[(df['Month'] == counter)]

            fig.append_trace(
                go.Bar(
                    x=['Positif', 'Sembuh', 'Meninggal'],
                    y=[sum(monthly_case['Positif Harian']), sum(monthly_case['Sembuh Harian']),
                       sum(monthly_case['Meninggal Harian'])],
                    text=[sum(monthly_case['Positif Harian']), sum(monthly_case['Sembuh Harian']),
                          sum(monthly_case['Meninggal Harian'])]
                ), row=i, col=j
            )

            counter += 1

    fig.update_traces(textposition='auto')
    fig.update_layout(title_x=0.5, height=950, width=1000,
                      showlegend=False,
                      hovermode=False, margin=dict(l=20, r=0, t=30, b=20))

    st.plotly_chart(fig)