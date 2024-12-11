import pymysql
import streamlit as st
import pandas as pd

st.title("Insurance Database Analysis")


def get_connection():
    return pymysql.connect(
        host="127.0.0.1",     # MySQL 호스트 주소 (예: localhost, 127.0.0.1, AWS RDS 등)
        user="root",      # MySQL 사용자 이름
        password="12345678",  # MySQL 비밀번호
        database="insurance" )

def fetch_data(query):
    conn = get_connection()
    try:
        data = pd.read_sql_query(query, conn)
    finally:
        conn.close()
    return data

menu = ["Home", "Data Viewer", "Analysis"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.header("Welcome to the Insurance Database Web Application")
    st.write("Explore and analyze your insurance data with ease.")

elif choice == "Data Viewer":
    st.header("Data Viewer")
    st.write("View and search insurance data.")

    # User Inputs for Query
    table_name = st.text_input("Enter Table Name", "policies")
    query = st.text_area("Custom SQL Query", f"SELECT * FROM {table_name} LIMIT 100")

    if st.button("Run Query"):
        try:
            data = fetch_data(query)
            st.write(f"Query Result ({len(data)} rows):")
            st.dataframe(data)
        except Exception as e:
            st.error(f"Error: {e}")

elif choice == "Analysis":
    st.header("Data Analysis")
    st.write("Perform data analysis on the insurance database.")

    # Predefined Analysis Options
    analysis_type = st.selectbox("Select Analysis Type", ["Policy Count by Region", "Claims Distribution"])

    if analysis_type == "Policy Count by Region":
        query = "SELECT region, COUNT(*) as policy_count FROM policies GROUP BY region"
        data = fetch_data(query)
        st.bar_chart(data.set_index('region'))

    elif analysis_type == "Claims Distribution":
        query = "SELECT claim_amount FROM claims"
        data = fetch_data(query)
        st.write("Claims Distribution:")
        st.hist_chart(data['claim_amount'])

# Footer
st.sidebar.info("Developed by [Your Name]")

