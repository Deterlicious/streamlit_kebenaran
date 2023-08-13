import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import locale

# Konfigurasi tampilan Streamlit
st.set_page_config(page_title='Antrian Pemesanan Makanan', layout='wide')

# Menambahkan harga menu
menu_prices = {
    'Nasi Goreng': 10000,
    'Mie Goreng': 5000,
    'Ayam Bakar': 20000
}

# Fungsi untuk menambahkan pesanan
def add_order(order_df, name, menu, quantity, delivery_datetime):
    if not name:
        st.warning('Nama pelanggan tidak boleh kosong.')
        return order_df

    if quantity <= 0:
        st.warning('Jumlah pesanan harus lebih dari 0.')
        return order_df

    order_data = {
        'No': len(order_df) + 1,
        'Nama': name,
        'Menu': menu,
        'Jumlah': quantity,
        'Waktu Pengiriman': delivery_datetime,
        'Harga': menu_prices[menu] * quantity
    }
    order_df.loc[len(order_df.index)] = order_data  # Use loc instead of append
    st.success('Pesanan berhasil ditambahkan ke antrian.')

    # Simpan data pesanan ke file CSV
    order_df.to_csv('order_history.csv', index=False)
    st.success('Data pesanan berhasil disimpan ke file CSV.')

    return order_df

def main():
    # Membuat DataFrame pesanan jika belum ada
    if 'order_history.csv' not in os.listdir():
        order_df = pd.DataFrame(columns=['No', 'Nama', 'Menu', 'Jumlah', 'Waktu Pengiriman', 'Harga'])
    else:
        order_df = pd.read_csv('order_history.csv') 

    st.title('Antrian Pemesanan Makanan')

    # Mendapatkan informasi pemesanan
    with st.form(key='order_form'):
        st.header('Form Pemesanan')
        name = st.text_input('Nama Pelanggan', key='name_input')
        menu = st.selectbox("Menu", list(menu_prices.keys()), key='menu_select')
        quantity = st.number_input('Jumlah Pesanan', min_value=1, step=1, key='quantity_input')
        delivery_time = st.time_input('Waktu Pengiriman', key='delivery_time_input')

        # Mengatur waktu pengiriman
        current_time = datetime.now().time()
        delivery_datetime = datetime.combine(datetime.today(), delivery_time)
        if delivery_datetime < datetime.now():
            delivery_datetime += timedelta(days=1)

        # Menambahkan pesanan ke DataFrame
        submit_button = st.form_submit_button('Tambahkan ke Antrian')
        if submit_button:
            order_df = add_order(order_df, name, menu, quantity, delivery_datetime)

    # Menampilkan antrian pemesanan saat ini
    st.subheader('Antrian Pemesanan Saat Ini:')
    if not order_df.empty:
        st.dataframe(order_df)
    else:
        st.write('Antrian pemesanan kosong.')

    # Menghapus pesanan dari antrian
    if st.button('Hapus Pesanan', key='remove_order_button'):
        if not order_df.empty:
            order_df = order_df.iloc[1:]
            st.success('Pesanan pertama dalam antrian berhasil dihapus.')
            order_df.reset_index(drop=True, inplace=True)
            order_df.to_csv('order_history.csv', index=False)
        else:
            st.warning('Antrian pemesanan kosong.')

    # Menampilkan waktu pengiriman terdekat
    if st.button('Waktu Pengiriman Terdekat', key='nearest_delivery_time_button'):
        if not order_df.empty:
            nearest_delivery_time = min(order_df['Waktu Pengiriman'])
            st.success(f'Waktu pengiriman terdekat: {nearest_delivery_time}')
        else:
            st.warning('Antrian pemesanan kosong.')

    # Menampilkan total pesanan dalam antrian
    if st.button('Total Pesanan', key='total_orders_button'):
        total_orders = order_df['Jumlah'].sum()
        st.success(f'Total pesanan dalam antrian: {total_orders}')

    # Menampilkan jumlah pesanan untuk setiap menu
    if st.button('Jumlah Pesanan per Menu', key='menu_counts_button'):
        menu_counts = order_df.groupby('Menu')['Jumlah'].sum()
        st.success('Jumlah Pesanan per menu:')
        st.dataframe(menu_counts)

    #Menampilkan jumlah pesanan dalam antrian
    if st.button('Jumlah Pesanan dalam Antrian', key='total_orders_in_queue_button'):
        st.success(f'Jumlah pesanan dalam antrian: {len(order_df)}')

    # Pencarian Pesanan
    st.subheader('Pencarian Pesanan')
    search_name = st.text_input('Nama Pelanggan untuk Pencarian', key='search_name_input')    
    if st.button('Cari Pesanan', key='search_button'):
        search_results = order_df[order_df['Nama'] == search_name]
        if not search_results.empty:
            st.success(f'Pesanan ditemukan untuk {search_name}:')
            st.dataframe(search_results)
        else:
            st.warning(f'Tidak ditemukan pesanan untuk {search_name}.')

if __name__ == "__main__":
    main()
