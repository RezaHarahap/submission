import calendar
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
)


@st.cache_data
def load_data():
    candidates = [
        Path(__file__).parent / "hour.csv",
        Path("dashboard/hour.csv"),
        Path("data/hour.csv"),
    ]

    for path in candidates:
        if path.exists():
            data = pd.read_csv(path)
            break
    else:
        raise FileNotFoundError("File hour.csv tidak ditemukan.")

    data["dteday"] = pd.to_datetime(data["dteday"])
    data = data.drop_duplicates().dropna(subset=["cnt"]).copy()
    data = data[data["cnt"] >= 0].copy()

    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    workingday_map = {0: "Non-Working Day", 1: "Working Day"}
    weather_map = {
        1: "Clear/Partly Cloudy",
        2: "Mist/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow",
    }

    data["season_name"] = data["season"].map(season_map)
    data["workingday_name"] = data["workingday"].map(workingday_map)
    data["weather_name"] = data["weathersit"].map(weather_map)
    data["month_name"] = data["dteday"].dt.month.map(lambda x: calendar.month_name[x])

    labels = ["Low Demand", "Medium Demand", "High Demand"]
    data["demand_segment"] = pd.qcut(
        data["cnt"], q=3, labels=labels, duplicates="drop"
    )

    return data


df = load_data()

st.title("🚲 Bike Sharing Analytics Dashboard")
st.caption(
    "Analisis pola penyewaan sepeda 2011–2012 dan segmentasi permintaan "
    "menggunakan manual clustering berbasis binning (tanpa machine learning)."
)

st.sidebar.header("Filter Data")
min_date = df["dteday"].min().date()
max_date = df["dteday"].max().date()

start_date = st.sidebar.date_input("Tanggal awal", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Tanggal akhir", max_date, min_value=min_date, max_value=max_date)

selected_season = st.sidebar.multiselect(
    "Musim",
    options=["Spring", "Summer", "Fall", "Winter"],
    default=["Spring", "Summer", "Fall", "Winter"],
)

selected_day_type = st.sidebar.multiselect(
    "Tipe hari",
    options=["Working Day", "Non-Working Day"],
    default=["Working Day", "Non-Working Day"],
)

if start_date > end_date:
    st.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir.")
    st.stop()

filtered_df = df[
    (df["dteday"].dt.date >= start_date)
    & (df["dteday"].dt.date <= end_date)
    & (df["season_name"].isin(selected_season))
    & (df["workingday_name"].isin(selected_day_type))
].copy()

if filtered_df.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()

# KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rentals", f"{int(filtered_df['cnt'].sum()):,}")
col2.metric("Rata-rata / Jam", f"{filtered_df['cnt'].mean():.1f}")
col3.metric("Peak Hour", f"{int(filtered_df.groupby('hr')['cnt'].mean().idxmax()):02d}:00")
col4.metric(
    "High Demand Share",
    f"{(filtered_df['demand_segment'].eq('High Demand').mean() * 100):.1f}%",
)

st.divider()

# Business question 1
st.subheader("1. Pola Penyewaan Berdasarkan Hari Kerja dan Bulan")
monthly_working = (
    filtered_df.groupby([filtered_df["dteday"].dt.month, "workingday_name"])["cnt"]
    .sum()
    .reset_index()
    .rename(columns={"dteday": "month"})
)

fig, ax = plt.subplots(figsize=(11, 5))
sns.lineplot(
    data=monthly_working,
    x="month",
    y="cnt",
    hue="workingday_name",
    marker="o",
    ax=ax,
)
ax.set_title("Total Penyewaan per Bulan Berdasarkan Tipe Hari")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")
ax.set_xticks(range(1, 13))
ax.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)])
ax.grid(axis="y", alpha=0.25)
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.info(
    "Gunakan grafik ini untuk membandingkan kontribusi hari kerja dan non-hari kerja "
    "terhadap total penyewaan pada setiap bulan."
)

# Business question 2
st.subheader("2. Dampak Musim terhadap Penyewaan")
season_summary = (
    filtered_df.groupby("season_name")["cnt"]
    .agg(total="sum", average="mean")
    .reindex(["Spring", "Summer", "Fall", "Winter"])
    .dropna()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=season_summary, x="season_name", y="total", ax=ax)
ax.set_title("Total Penyewaan Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan")
ax.grid(axis="y", alpha=0.25)
st.pyplot(fig, use_container_width=True)
plt.close(fig)

best_season = season_summary.loc[season_summary["total"].idxmax(), "season_name"]
st.success(
    f"Pada rentang filter saat ini, musim dengan total penyewaan tertinggi adalah **{best_season}**."
)

st.divider()

# Advanced analysis
st.header("Advanced Analysis — Manual Clustering dengan Binning")
st.write(
    "Permintaan dibagi menjadi **Low, Medium, dan High Demand** menggunakan `pandas.qcut` "
    "berdasarkan kuantil distribusi `cnt`. Teknik ini merupakan clustering manual berbasis "
    "binning dan **tidak menggunakan algoritma machine learning**."
)

segment_order = ["Low Demand", "Medium Demand", "High Demand"]
segment_summary = (
    filtered_df.groupby("demand_segment", observed=False)["cnt"]
    .agg(Observasi="count", Minimum="min", Median="median", Rata_rata="mean", Maksimum="max")
    .reindex(segment_order)
    .round(2)
)
st.dataframe(segment_summary, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("High Demand berdasarkan Jam")
    high_hour = (
        filtered_df[filtered_df["demand_segment"] == "High Demand"]
        .groupby("hr")["cnt"]
        .agg(frequency="count", average="mean")
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=high_hour, x="hr", y="frequency", ax=ax)
    ax.set_title("Frekuensi High Demand per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Observasi High Demand")
    ax.grid(axis="y", alpha=0.25)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right:
    st.subheader("High Demand berdasarkan Musim & Tipe Hari")
    total_group = (
        filtered_df.groupby(["season_name", "workingday_name"])
        .size()
        .rename("total")
    )
    high_group = (
        filtered_df[filtered_df["demand_segment"] == "High Demand"]
        .groupby(["season_name", "workingday_name"])
        .size()
        .rename("high")
    )
    high_share = pd.concat([total_group, high_group], axis=1).fillna(0)
    high_share["high_demand_share"] = high_share["high"] / high_share["total"] * 100
    high_share = high_share.reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=high_share,
        x="season_name",
        y="high_demand_share",
        hue="workingday_name",
        ax=ax,
    )
    ax.set_title("Proporsi High Demand (%)")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Persentase High Demand")
    ax.grid(axis="y", alpha=0.25)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

peak_high_hour = int(high_hour.sort_values(["frequency", "average"], ascending=False).iloc[0]["hr"])
priority_row = high_share.sort_values("high_demand_share", ascending=False).iloc[0]

st.subheader("Actionable Insight")
st.markdown(
    f"""
- **Jam prioritas:** sekitar **{peak_high_hour:02d}:00** paling sering muncul sebagai periode High Demand pada filter saat ini.
- **Kombinasi kondisi prioritas:** **{priority_row['season_name']} — {priority_row['workingday_name']}** memiliki proporsi High Demand tertinggi pada data terfilter.
- **Rekomendasi:** lakukan redistribusi sepeda dan pemeriksaan ketersediaan dock sebelum jam prioritas, lalu tingkatkan kesiapan operasional pada kombinasi musim dan tipe hari dengan proporsi High Demand tinggi.
"""
)

st.caption(
    "Dashboard dibuat untuk Proyek Analisis Data Dicoding menggunakan Bike Sharing Dataset."
)
