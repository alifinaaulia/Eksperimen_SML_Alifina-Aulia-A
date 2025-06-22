import pandas as pd
import os

def preprocess_transaction_data(df):
    # Menghapus baris dengan missing value pada kolom penting
    df = df.dropna(subset=['Description', 'CustomerID'])

    # Menghapus duplikat
    df = df.drop_duplicates()

    # Menghapus transaksi yang tidak valid (Quantity dan UnitPrice <= 0)
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # Menambahkan kolom TotalPrice
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    # Mengubah CustomerID ke tipe string
    df['CustomerID'] = df['CustomerID'].astype(str)

    # Ekstraksi fitur waktu
    df['InvoiceYearMonth'] = df['InvoiceDate'].dt.to_period('M')
    df['InvoiceMonth'] = df['InvoiceDate'].dt.month
    df['InvoiceDay'] = df['InvoiceDate'].dt.day
    df['InvoiceHour'] = df['InvoiceDate'].dt.hour

    # Menghapus kolom yang tidak relevan
    df = df.drop(columns=['InvoiceNo', 'StockCode'])

    # Menghapus outlier berdasarkan IQR untuk Quantity, UnitPrice, dan TotalPrice
    for col in ['Quantity', 'UnitPrice', 'TotalPrice']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]

    return df

if __name__ == '__main__':
    # Baca data mentah dari root folder
    df = pd.read_csv('online_retail_raw.csv', parse_dates=['InvoiceDate'])

    # Jalankan fungsi preprocessing
    df_clean = preprocess_transaction_data(df)

    # Simpan hasil ke file CSV langsung (bukan folder)
    df_clean.to_csv('preprocessing/online_retail_preprocessing.csv', index=False)
    print("Preprocessing selesai. File disimpan sebagai 'preprocessing/online_retail_preprocessing.csv'")