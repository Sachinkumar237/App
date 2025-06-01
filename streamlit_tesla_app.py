import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Streamlit app title
st.title("Tesla Stock Data Analysis")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload Tesla dataset (CSV)", type="csv")

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_csv(uploaded_file)

    # Display basic information
    st.subheader("First Few Rows of the Dataset")
    st.dataframe(df.head())

    st.subheader("Dataset Info")
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    # Convert 'Date' column to datetime if present
    if 'Date' in df.columns:
        try:
            df['Date'] = pd.to_datetime(df['Date'])
            df.sort_values('Date', inplace=True)
        except Exception as e:
            st.error(f"Error converting 'Date' column to datetime: {e}")
    else:
        st.warning("'Date' column not found in the dataset.")

    # Check for missing values
    st.subheader("Missing Values in Each Column")
    st.write(df.isnull().sum())

    # Fill missing values (forward fill)
    if df.isnull().any().any():
        df.fillna(method='ffill', inplace=True)
        st.info("Missing values filled using forward fill method.")
    else:
        st.info("No missing values found in the dataset.")

    # Plot closing prices if available
    if 'Close' in df.columns and 'Date' in df.columns:
        st.subheader("Tesla Stock Closing Price Over Time")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['Date'], df['Close'], label='Closing Price')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title('Tesla Stock Closing Price Over Time')
        ax.legend()
        ax.grid(True)
        
        # Display the plot in Streamlit
        st.pyplot(fig)
        
        # Provide download link for the plot
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(
            label="Download Plot",
            data=buf,
            file_name="tesla_stock_plot.png",
            mime="image/png"
        )
    else:
        st.warning("'Close' and/or 'Date' column not found for plotting.")
else:
    st.info("Please upload a CSV file to proceed.")