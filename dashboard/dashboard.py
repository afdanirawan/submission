import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Styling
sns.set(style='darkgrid')

# Helper functions
def load_data():
    # Gantikan ini dengan pengambilan data aktual Anda dari Google Colab.
    df = pd.read_csv('main_data.csv')
    df['Date'] = pd.to_datetime(df['Date']) # mengubah kolom tanggal menjadi tipe datetime
    return df

def daily_email_count(df):
    return df.groupby(df['Date'].dt.date).size().reset_index(name='Count')

def top_senders(df):
    return df['From'].value_counts().head(10)

@st.cache
def load_processed_data():
    df = load_data()
    daily = daily_email_count(df)
    top = top_senders(df)
    return daily, top

# Load processed data
daily_df, top_df = load_processed_data()

# Streamlit App
st.title('Email Analysis Dashboard')
st.write('A simple dashboard to analyze email data.')

# Time series plot
st.subheader('Daily Email Count')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=daily_df['Date'], y=daily_df['Count'], ax=ax)
st.pyplot(fig)

# Top senders bar plot
st.subheader('Top 10 Senders by Email Count')
fig, ax = plt.subplots(figsize=(12, 6))
top_df.plot(kind='bar', ax=ax)
ax.set_ylabel('Number of Emails')
ax.set_xlabel('Sender')
st.pyplot(fig)

# Detailed email table
st.subheader('Detailed Email Data')
st.write(load_data())

# Ending note
st.write('This is a basic email analysis dashboard. Further analysis and visualizations can be added based on additional available data and requirements.')
