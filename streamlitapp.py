{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pymysql\n",
    "import streamlit as st\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-12-11 19:04:45.297 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run /opt/anaconda3/lib/python3.12/site-packages/ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "st.title(\"Insurance Database Analysis\")\n",
    "\n",
    "\n",
    "def get_connection():\n",
    "    return pymysql.connect(\n",
    "        host=\"127.0.0.1\",     # MySQL 호스트 주소 (예: localhost, 127.0.0.1, AWS RDS 등)\n",
    "        user=\"root\",      # MySQL 사용자 이름\n",
    "        password=\"12345678\",  # MySQL 비밀번호\n",
    "        database=\"insurance\" )\n",
    "\n",
    "def fetch_data(query):\n",
    "    conn = get_connection()\n",
    "    try:\n",
    "        data = pd.read_sql_query(query, conn)\n",
    "    finally:\n",
    "        conn.close()\n",
    "    return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-12-11 19:04:50.769 Session state does not function when running a script without `streamlit run`\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator(_root_container=1, _parent=DeltaGenerator())"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "menu = [\"Home\", \"Data Viewer\", \"Analysis\"]\n",
    "choice = st.sidebar.selectbox(\"Menu\", menu)\n",
    "\n",
    "if choice == \"Home\":\n",
    "    st.header(\"Welcome to the Insurance Database Web Application\")\n",
    "    st.write(\"Explore and analyze your insurance data with ease.\")\n",
    "\n",
    "elif choice == \"Data Viewer\":\n",
    "    st.header(\"Data Viewer\")\n",
    "    st.write(\"View and search insurance data.\")\n",
    "\n",
    "    # User Inputs for Query\n",
    "    table_name = st.text_input(\"Enter Table Name\", \"policies\")\n",
    "    query = st.text_area(\"Custom SQL Query\", f\"SELECT * FROM {table_name} LIMIT 100\")\n",
    "\n",
    "    if st.button(\"Run Query\"):\n",
    "        try:\n",
    "            data = fetch_data(query)\n",
    "            st.write(f\"Query Result ({len(data)} rows):\")\n",
    "            st.dataframe(data)\n",
    "        except Exception as e:\n",
    "            st.error(f\"Error: {e}\")\n",
    "\n",
    "elif choice == \"Analysis\":\n",
    "    st.header(\"Data Analysis\")\n",
    "    st.write(\"Perform data analysis on the insurance database.\")\n",
    "\n",
    "    # Predefined Analysis Options\n",
    "    analysis_type = st.selectbox(\"Select Analysis Type\", [\"Policy Count by Region\", \"Claims Distribution\"])\n",
    "\n",
    "    if analysis_type == \"Policy Count by Region\":\n",
    "        query = \"SELECT region, COUNT(*) as policy_count FROM policies GROUP BY region\"\n",
    "        data = fetch_data(query)\n",
    "        st.bar_chart(data.set_index('region'))\n",
    "\n",
    "    elif analysis_type == \"Claims Distribution\":\n",
    "        query = \"SELECT claim_amount FROM claims\"\n",
    "        data = fetch_data(query)\n",
    "        st.write(\"Claims Distribution:\")\n",
    "        st.hist_chart(data['claim_amount'])\n",
    "\n",
    "# Footer\n",
    "st.sidebar.info(\"Developed by [Your Name]\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
