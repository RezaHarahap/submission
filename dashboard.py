
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import seaborn as sns
import numpy as np 

df = pd.read_csv("hour.csv")

st.sidebar.title("Navigation")

menu_options = ["Dashboard", "Month"]


selected_page = st.sidebar.selectbox("Go to", menu_options)

if selected_page == "Dashboard":
    st.title("DASHBOARD")
    st.write("Welcome to the Dashboard Reza Pahlevi!")


    @st.cache_data
    def load_data():
        df = pd.read_csv("hour.csv")
        df['dteday'] = pd.to_datetime(df['dteday'])
        return df

    df = load_data()

 #SIDE BAR TANGGAL
    st.sidebar.title('Range Tanggal')
    min_date = df['dteday'].min()
    max_date = df['dteday'].max()
    start_date = st.sidebar.date_input('Start Date', min_date)
    end_date = st.sidebar.date_input('End Date', max_date)

    filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

#KORELASI
    st.subheader('Heatmap Corellation')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(filtered_df.corr(), annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
    st.pyplot(fig)

    # Jumlah Penggunaan Sepeda Motor per Bulan Berdasarkan Hari Kerja
    st.subheader('Total of Bicycle Rentals per Month by Working Day')
    workingday = filtered_df.groupby(by=['mnth', 'workingday']).agg({'cnt': 'sum'})
    workingday_pivot = workingday.reset_index().pivot(index='mnth', columns='workingday', values='cnt')
    months_order = ['January','Februuary','March','April','Mei','June','July','August','September','October','November','December']
    fig, ax = plt.subplots(figsize=(10, 6))
    for category in workingday_pivot.columns:
        ax.plot(workingday_pivot.index, workingday_pivot[category], marker='o', label=category)
    ax.set_title('Total of Bicycle  Rentals per Month by Working Day')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(months_order, rotation=45)
    ax.legend()
    st.pyplot(fig)

#BERDASARKAN MUSIM
    st.subheader('Total of Bicyle by Season')
    season_totals = filtered_df.groupby('season')['cnt'].sum()
    max_season = season_totals.idxmax()
    min_season = season_totals.idxmin()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(season_totals.index, season_totals.values, color=['blue', 'green', 'orange', 'red'])
    ax.text(max_season, season_totals[max_season], f'{season_totals[max_season]}', ha='center', va='bottom')
    ax.text(min_season, season_totals[min_season], f'{season_totals[min_season]}', ha='center', va='bottom')
    ax.set_title('Total of Bicyle by Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Total')
    ax.set_xticks(season_totals.index)
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    ax.grid(axis='y')
    st.pyplot(fig)

#BERDASARKAN MUSIM DAN BULAN
    st.subheader('Total of Bicycle Rentals by Season and Month')
    season_month_totals = filtered_df.groupby(['season', 'mnth'])['cnt'].sum()
    all_months_season_totals = pd.DataFrame(index=range(1, 13))
    for season in season_month_totals.index.get_level_values('season').unique():
        filtered_df['season'] = filtered_df['season'].replace({1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin',})
        all_months_season_totals[f'Musim {season}'] = season_month_totals[season]
    fig, ax = plt.subplots(figsize=(10, 6))
    all_months_season_totals.plot(kind='bar', ax=ax, color=['blue', 'green', 'orange', 'red'])
    ax.set_title('Total of Bicycle Rentals by Season and Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total')
    ax.set_xticks(range(0, 12))
    ax.set_xticklabels(['January','Februuary','March','April','Mei','June','July','August','September','October','November','December'], rotation=45)
    ax.grid(axis='y')
    ax.legend(title='Season')
    st.pyplot(fig)


elif selected_page == "Month":
   
    def get_month_names():
        return [calendar.month_name[i] for i in range(1, 13)]

    months = get_month_names()
    selected_month = st.sidebar.selectbox("Choose Month", months)
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['workingday'] = df['workingday'].replace({0: 'work', 1: 'not work'})
    df['season'] = df['season'].replace({
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    })

    filtered_df = df[df['dteday'].dt.month == months.index(selected_month) + 1]

    workingday_counts = filtered_df.groupby('workingday')['cnt'].sum()
    total_renters = filtered_df['cnt'].sum()
    selected_season = filtered_df['season'].unique()[0]


    st.title(f"The Bicycle Rent for {selected_month}")
    st.subheader(f"*Season: {selected_season}*")
    st.subheader('Monthly Rent')
    st.metric("Total Rent", value=total_renters)
    st.bar_chart(workingday_counts)

 


