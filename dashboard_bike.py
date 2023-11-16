import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import statsmodels.api as sm
from babel.numbers import format_currency
sns.set(style='dark')

# Membaca data dari file CSV
all_df = pd.read_csv("all_data.csv")

st.header('Bike Sharing Dataset :sparkles:')


min_date = pd.to_datetime(all_df["dteday"]).min()
max_date = pd.to_datetime(all_df["dteday"]).max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/dimasp-x/SubmissionDicodingData/main/bike_sharing.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Mencetak nilai start_date dan end_date
st.write("Start Date:", start_date)
st.write("End Date:", end_date)

# Memproses data
total_per_bulan = all_df.groupby(by=['mnth', 'yr'], as_index=False)['cnt_hour'].sum()

total_per_bulan['mnth'] = pd.Categorical(total_per_bulan['mnth'], categories=[
    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
], ordered=False)

total_per_bulan = total_per_bulan.sort_values(by=['yr', 'mnth'])

# Kode untuk menampilkan plot di Streamlit
st.subheader('Perbandingan Total Penyewaan Sepeda Per Bulan (2011-2012)')

# Menyiapkan data untuk plot
data_2011 = total_per_bulan[total_per_bulan['yr'] == 2011]
data_2012 = total_per_bulan[total_per_bulan['yr'] == 2012]

# Menampilkan plot menggunakan matplotlib
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(data_2011['mnth'], data_2011['cnt_hour'], label='2011', marker='o')
ax.plot(data_2012['mnth'], data_2012['cnt_hour'], label='2012', marker='o')

# Menambahkan label dan judul plot
ax.set_title('Perbandingan Total Penyewaan Sepeda Per Bulan (2011-2012)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Total Penyewaan')

# Menampilkan legenda
ax.legend()

# Mengatur label sumbu x miring sebesar 15 derajat
plt.xticks(rotation=15, ha='right')

# Menampilkan teks total penyewaan di luar gambar grafik sebagai kolom terpisah
# Menampilkan teks total penyewaan di luar gambar grafik sebagai kolom terpisah
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Penyewaan Tahun 2011", value=data_2011['cnt_hour'].sum())

with col2:
    st.metric("Total Penyewaan Tahun 2012", value=data_2012['cnt_hour'].sum())
# Menampilkan plot di Streamlit
st.pyplot(fig)

# Memproses data per musim
total_per_musim = all_df.groupby('season')['cnt_hour'].sum().reset_index()
total_per_musim_sorted = total_per_musim.sort_values(by="cnt_hour", ascending=False)

st.subheader("Musim Dengan Jumlah Penyewaan Sepeda Paling Rendah")

# Menyiapkan warna untuk plot
colors_ = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#FF6347"]

# Menampilkan plot menggunakan seaborn
plt.figure(figsize=(10, 5))
ax = sns.barplot(x="cnt_hour", y="season", data=total_per_musim_sorted, palette=colors_)

# Menambahkan teks pada bar
for index, value in enumerate(total_per_musim_sorted["cnt_hour"]):
    ax.text(value, index, f'{value:,}', ha='left', va='center', fontsize=10, color='black')

# Mengatur judul dan parameter lainnya
plt.title("Musim Dengan Jumlah Penyewaan Sepeda Paling Rendah", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)

# Menampilkan plot di Streamlit
st.pyplot(plt)

# Menampilkan subheader
st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

# Memproses data
total_per_cuaca = all_df.groupby('weathersit_hour')['cnt_hour'].sum().reset_index()
total_per_cuaca_sorted = total_per_cuaca.sort_values(by='cnt_hour')

# Menyiapkan palet warna untuk plot
palette = sns.color_palette("muted")

# Menampilkan plot menggunakan seaborn
fig, ax = plt.subplots(figsize=(10, 6))
ax = sns.barplot(x='weathersit_hour', y='cnt_hour', data=total_per_cuaca_sorted, palette=palette)

# Menambahkan teks pada bar
for p in ax.patches:
    ax.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10, color='black')

# Menyiapkan legenda
legend_labels = {
    1: "Cerah/Sejuk",
    2: "Berawan/Kabut",
    3: "Hujan Ringan",
    4: "Hujan Lebat"
}

handles = [plt.Rectangle((0, 0), 1, 1, color=palette[i]) for i in range(len(legend_labels))]
plt.legend(handles, legend_labels.values(), loc="upper right")

# Mengatur judul dan parameter lainnya
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Penyewaan Sepeda')

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Menampilkan subheader
st.subheader("Pola Penyewaan Pelanggan Casual dan Registered (2011-2012)")

# Memproses data
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
cust_per_bulan = all_df.resample(rule='M', on='dteday').agg({
    "casual_hour": "sum",
    "registered_hour": "sum"
})
cust_per_bulan.index = cust_per_bulan.index.strftime('%B %Y')

# Memisahkan data untuk tahun 2011 dan 2012
data_2011 = cust_per_bulan[cust_per_bulan.index.str.contains('2011')]
data_2012 = cust_per_bulan[cust_per_bulan.index.str.contains('2012')]

# Menyiapkan ukuran dan bar_width
fig, ax = plt.subplots(figsize=(15, 8))

# Plot untuk tahun 2011
bar_width = 0.35
index_2011 = range(len(data_2011))
ax.bar(index_2011, data_2011['casual_hour'], width=bar_width, label='Casual', color='lightblue')
ax.bar([i + bar_width for i in index_2011], data_2011['registered_hour'], width=bar_width, label='Registered', color='orange')
ax.set_title('Pola Penyewaan Pelanggan Casual dan Registered (2011)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks([i + bar_width/2 for i in index_2011])
ax.set_xticklabels(data_2011.index, rotation=45)
ax.legend()
ax.grid(True)

# Menampilkan total penyewaan di luar gambar grafik sebagai kolom terpisah untuk tahun 2011
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Casual Tahun 2011", value=data_2011['casual_hour'].sum())

with col2:
    st.metric("Total Registered Tahun 2011", value=data_2011['registered_hour'].sum())

with col3:
    st.metric("Total Penyewaan Tahun 2011", value=data_2011['casual_hour'].sum() + data_2011['registered_hour'].sum())

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Menampilkan subheader untuk tahun 2012
st.subheader("Pola Penyewaan Pelanggan Casual dan Registered (2012)")

# Memisahkan data untuk tahun 2012
data_2012 = cust_per_bulan[cust_per_bulan.index.str.contains('2012')]

# Menyiapkan ukuran dan bar_width untuk tahun 2012
fig, ax = plt.subplots(figsize=(15, 8))

# Plot untuk tahun 2012
bar_width = 0.35
index_2012 = range(len(data_2012))
ax.bar(index_2012, data_2012['casual_hour'], width=bar_width, label='Casual', color='lightblue')
ax.bar([i + bar_width for i in index_2012], data_2012['registered_hour'], width=bar_width, label='Registered', color='orange')
ax.set_title('Pola Penyewaan Pelanggan Casual dan Registered (2012)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks([i + bar_width/2 for i in index_2012])
ax.set_xticklabels(data_2012.index, rotation=45)
ax.legend()
ax.grid(True)

# Menampilkan total penyewaan di luar gambar grafik sebagai kolom terpisah untuk tahun 2012
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Casual Tahun 2012", value=data_2012['casual_hour'].sum())

with col2:
    st.metric("Total Registered Tahun 2012", value=data_2012['registered_hour'].sum())

with col3:
    st.metric("Total Penyewaan Tahun 2012", value=data_2012['casual_hour'].sum() + data_2012['registered_hour'].sum())

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Menampilkan subheader untuk tahun 2012
st.subheader("Pola Penyewaan Sepeda pada Hari Libur dan Hari Kerja")

# Memilih kolom yang diperlukan
selected_columns = ['holiday', 'hr', 'cnt_hour']
df_selected = all_df[selected_columns]

# Membuat plot
fig, ax = plt.subplots(figsize=(12, 6))

df_holiday = df_selected[df_selected['holiday'] == 1]
df_workday = df_selected[df_selected['holiday'] == 0]

sns.pointplot(data=df_workday, x='hr', y='cnt_hour', color='blue', markers=['o'], linestyles=['-'], label='Hari Kerja')
sns.pointplot(data=df_holiday, x='hr', y='cnt_hour', color='orange', markers=['o'], linestyles=['--'], label='Hari Libur')

plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Pola Penyewaan Sepeda pada Hari Libur dan Hari Kerja Berdasarkan Jam')
plt.legend(title='Jenis Hari')

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Menentukan variabel independen (X) dan variabel dependen (y)
X = all_df[['temp_hour', 'atemp_hour', 'hum_hour', 'windspeed_hour']]
y = all_df['cnt_hour']

# Menambahkan kolom konstanta
X = sm.add_constant(X)

# Membuat model regresi
model = sm.OLS(y, X).fit()

# Menampilkan hasil analisis regresi di Streamlit
st.header('Hasil Analisis Regresi')
st.text('Ringkasan Model:')
st.text(model.summary())

# Membersihkan gambar sebelum membuat yang baru
plt.clf()

# Menambahkan visualisasi residual plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(model.predict(), model.resid)
ax.axhline(y=0, color='r', linestyle='--')
ax.set_title('Residual Plot')
ax.set_xlabel('Predicted Values')
ax.set_ylabel('Residuals')

# Menampilkan plot di Streamlit
st.pyplot(fig)

st.caption('Copyright (c) 2023')