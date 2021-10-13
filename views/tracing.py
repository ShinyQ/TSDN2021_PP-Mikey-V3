import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def penambahan(curr, next):
    return np.abs(curr - next)


def app():
    df = pd.read_excel("dataset/Data Academy_ED.xlsx", sheet_name="Data Suspek dll (Jakarta)")
    df.fillna(0, inplace=True)
    df = df[(df["Tanggal"] >= '2021-01-01') & (df["Tanggal"] <= "2021-10-01")]
    df["bulan"] = pd.DatetimeIndex(df['Tanggal']).month

    q1 = df[0:68].copy()
    q2 = df[68:136].copy()
    q3 = df[136:204].copy()
    q4 = df[204:273].copy()

    q1_prob = q1["Total Probable"].sum(axis=0)
    q1_kontak_erat = q1["Total Kontak Erat"].sum(axis=0)
    q1_suspek = q1['Total Suspek'].sum(axis=0)

    q2_prob = q2["Total Probable"].sum(axis=0)
    q2_kontak_erat = q2["Total Kontak Erat"].sum(axis=0)
    q2_suspek = q2['Total Suspek'].sum(axis=0)

    q3_prob = q3["Total Probable"].sum(axis=0)
    q3_kontak_erat = q3["Total Kontak Erat"].sum(axis=0)
    q3_suspek = q3['Total Suspek'].sum(axis=0)

    q4_prob = q4["Total Probable"].sum(axis=0)
    q4_kontak_erat = q4["Total Kontak Erat"].sum(axis=0)
    q4_suspek = q4['Total Suspek'].sum(axis=0)

    st.write("")
    st.write("#### Kemampuan Quarter Tracing Jakarta (Januari - September 2021)")

    status = ['1 Januari - 9 Maret', '10 Maret - 15 Mei', '16 Mei - 23 Juli', '24 Juli - 30 September']
    list_bar = [go.Bar(x=status, y=[q1_kontak_erat, q2_kontak_erat, q3_kontak_erat, q4_kontak_erat], name="Kontak Erat",
                       text=[q1_kontak_erat, q2_kontak_erat, q3_kontak_erat, q4_kontak_erat]),
                go.Bar(x=status, y=[q1_suspek, q2_suspek, q3_suspek, q4_suspek], name="Suspek",
                       text=[q1_suspek, q2_suspek, q3_suspek, q4_suspek]),
                go.Bar(x=status, y=[q1_prob, q2_prob, q3_prob, q4_prob], name="Probable",
                       text=[q1_prob, q2_prob, q3_prob, q4_prob])]

    fig = go.Figure(data=list_bar)
    fig.update_traces(textposition='outside', )
    fig.update_layout(barmode='group', title_x=0.5)
    fig.update_layout(
        margin=dict(l=20, r=0, t=20, b=20),
        width=1000,
        font=dict(
            size=12.5,
        )
    )

    st.plotly_chart(fig)

    st.write("")
    st.write("#### Total Tracing Jakarta Bulan Januari - September 2021")

    fig = make_subplots(
        rows=3, cols=3,
        horizontal_spacing=0.05, vertical_spacing=0.1,
        subplot_titles=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September"],
    )

    tol_bulan = 1
    for i in range(1, 4):
        for j in range(1, 4):
            kasus = df.loc[df["bulan"] == tol_bulan].copy()
            summed_kasus_kontak_erat = kasus["Total Kontak Erat"].sum(axis=0)
            summed_kasus_suspek = kasus["Total Suspek"].sum(axis=0)
            summed_kasus_probable = kasus["Total Probable"].sum(axis=0)

            fig.append_trace(
                go.Bar(x=["Kontak Erat", "Suspek", "Probable"],
                       y=[summed_kasus_kontak_erat, summed_kasus_suspek, summed_kasus_probable],
                       text=[summed_kasus_kontak_erat, summed_kasus_suspek, summed_kasus_probable]),
                row=i, col=j)

            tol_bulan += 1

    fig.update_traces(textposition="auto")
    fig.update_layout(title_x=0.5, height=950, width=1000,
                      margin=dict(l=20, r=0, t=30, b=20),
                      showlegend=False,
                      font=dict(size=12.5)
                      )

    st.plotly_chart(fig)

    df.reset_index(inplace=True)
    df["penambahan_harian_k"] = 0
    for i in range(len(df) - 1):
        if i == 0:
            pass
        else:
            curr = df.loc[i, "Total Kontak Erat"]
            next = df.loc[i + 1, "Total Kontak Erat"]
            df.loc[i, 'penambahan_harian_k'] = penambahan(curr, next)

    df["penambahan_harian_p"] = 0
    for i in range(len(df) - 1):
        if i == 0:
            pass
        else:
            curr = df.loc[i, "Total Probable"]
            next = df.loc[i + 1, "Total Probable"]
            df.loc[i, 'penambahan_harian_p'] = penambahan(curr, next)

    df["penambahan_harian_s"] = 0
    for i in range(len(df) - 1):
        if i == 0:
            pass
        else:
            curr = df.loc[i, "Total Suspek"]
            next = df.loc[i + 1, "Total Suspek"]
            df.loc[i, 'penambahan_harian_s'] = penambahan(curr, next)

    prev = df.loc[df["Tanggal"] == "2021-01-10", "penambahan_harian_s"]
    df.loc[df["Tanggal"] == "2021-01-11", "penambahan_harian_s"] = prev.values

    st.write("")
    st.write("#### Trend Kemampuan Tracing Harian Jakarta (Januari - September 2021)")

    date = [31, 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30]

    fig = go.Figure()
    data = [
        go.Scatter(x=df["Tanggal"], y=df["penambahan_harian_k"], text=df["penambahan_harian_k"], name="Kontak Erat"),
        go.Scatter(x=df["Tanggal"], y=df["penambahan_harian_s"], text=df["penambahan_harian_s"], name="Suspek"),
        go.Scatter(x=df["Tanggal"], y=df["penambahan_harian_p"], text=df["penambahan_harian_p"], name="Probable")

    ]

    fig.add_traces(data)
    fig.update_layout(title_x=0.5, showlegend=True, width=1000,
                      margin=dict(l=20, r=0, t=20, b=0),
                      font=dict(size=14))

    st.plotly_chart(fig)

    st.write("")
    st.write("#### Kumulatif Tracing Harian Jakarta (Januari - September 2021)")

    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September"],
    )

    tol_bulan = 1
    for i in range(1, 4):
        for j in range(1, 4):
            kasus = df.loc[df["bulan"] == tol_bulan].copy()
            date = kasus["Tanggal"].values[0]
            days = pd.Period(str(date)).days_in_month
            summed_kasus_kontak_erat = kasus["penambahan_harian_k"].sum(axis=0)
            summed_kasus_suspek = kasus["penambahan_harian_s"].sum(axis=0)
            summed_kasus_probable = kasus["penambahan_harian_p"].sum(axis=0)

            persentase_Bulan_k = summed_kasus_kontak_erat // days
            persentase_Bulan_s = summed_kasus_suspek // days
            persentase_Bulan_p = summed_kasus_probable // days
            fig.append_trace(
                go.Bar(x=[f"Kontak Erat, {persentase_Bulan_k}/ Hari", f"Suspek {persentase_Bulan_s}/ Hari",
                          f"Probable {persentase_Bulan_p}/ Hari"],
                       y=[summed_kasus_kontak_erat, summed_kasus_suspek, summed_kasus_probable],
                       text=[summed_kasus_kontak_erat, summed_kasus_suspek, summed_kasus_probable]),
                row=i, col=j)

            tol_bulan += 1

    fig.update_traces(textposition="auto")
    fig.update_layout(title_x=0.5, height=950, width=1000,
                      showlegend=False, margin=dict(l=20, r=0, t=30, b=0),
                      hovermode=False)

    st.plotly_chart(fig)

    df_rate = pd.read_csv("dataset/Data Academy_ED_04.csv")
    df_rate["rata_rata_positivity"] = (df_rate["positivity_rate_harian_antigen"] + df_rate[
        "positivity_rate_harian_pcr"]) / 2
    df_rate["total_test_harian"] = df_rate["jumlah_test_antigen_harian"] + df_rate["jumlah_test_pcr_harian"]

    date = [31, 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30]

    st.write("")
    st.write("#### Positivity Rate Testing Jakarta (Januari - September) 2021")
    fig = go.Figure()
    data = [
        go.Scatter(x=df_rate["Tanggal"], y=df_rate["positivity_rate_harian_antigen"],
                   text=df_rate["positivity_rate_harian_antigen"], name="Antigen"),
        go.Scatter(x=df_rate["Tanggal"], y=df_rate["positivity_rate_harian_pcr"],
                   text=df_rate["positivity_rate_harian_pcr"], name="PCR"),
        go.Scatter(x=df_rate["Tanggal"], y=df_rate["rata_rata_positivity"], text=df_rate["rata_rata_positivity"],
                   name="Rata - Rata Positivity")
    ]
    fig.add_traces(data)
    fig.update_layout(title_x=0.5, width=1000,
                      margin=dict(l=20, r=0, t=10, b=0),
                      font=dict(size=14),
                      showlegend=True)

    st.plotly_chart(fig)

    st.write("")
    st.write("#### Jumlah Testing Jakarta (Januari - September) 2021")
    fig = go.Figure()
    data = [
        go.Scatter(x=df_rate["Tanggal"], y=df_rate["jumlah_test_antigen_harian"],
                   text=df_rate["jumlah_test_antigen_harian"], name="Antigen"),
        go.Scatter(x=df_rate["Tanggal"], y=df_rate["jumlah_test_pcr_harian"], text=df_rate["jumlah_test_pcr_harian"],
                   name="PCR"),
        go.Scatter(x=df_rate["Tanggal"], y=df_rate["total_test_harian"], text=df_rate["total_test_harian"],
                   name="Total Test")
    ]
    fig.add_traces(data)
    fig.update_layout(
        title_x=0.5, showlegend=True, width=1000,
        margin=dict(l=20, r=0, t=10, b=0),
        font=dict(size=14),
    )

    st.plotly_chart(fig)
