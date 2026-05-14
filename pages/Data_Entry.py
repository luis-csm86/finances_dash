import streamlit as st
import pandas as pd
from datetime import date
import json
import os

st.markdown("<style>" + open("styles.css").read() + "</style>", unsafe_allow_html=True)

# --- PERSISTENCE: load from disk on first run ---
DATA_FILE = "records.json"

def load_records():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_json(DATA_FILE, orient="records")
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"]).dt.date
            return df
        except Exception:
            pass
    return pd.DataFrame(columns=["date", "category", "company", "amount", "paid", "pending", "status"])

def save_records(df):
    df_save = df.copy()
    df_save["date"] = df_save["date"].astype(str)
    df_save.to_json(DATA_FILE, orient="records", indent=2)

if "records" not in st.session_state:
    st.session_state.records = load_records()

# --- TITLE ---
st.markdown("""
    <div style="text-align:center; overflow: visible; padding: 0.5rem 0 1rem;">
        <h1 class="glitch" data-text="ADD NEW RECORD">ADD NEW RECORD</h1>
    </div>
""", unsafe_allow_html=True)

# --- FORM ---
with st.form("add_record_form"):
    col1, col2 = st.columns(2)

    with col1:
        entry_date = st.date_input("Date", value=date.today(), format="DD/MM/YYYY")
        category = st.selectbox(
            "Category",
            ["Finances", "Purchases", "Personal", "Admin", "Miscellaneous"]
        )
        company = st.text_input("Company")

    with col2:
        amount = st.number_input("Amount (€)", min_value=0.0, step=0.01)
        paid = st.number_input("Paid (€)", min_value=0.0, step=0.01)
        status = st.selectbox("Status", ["Completed", "Pending", "On going"])

    submitted = st.form_submit_button("Add Entry")

if submitted:
    pending = amount - paid
    new_row = {
        "date": entry_date,
        "category": category,
        "company": company,
        "amount": amount,
        "paid": paid,
        "pending": pending,
        "status": status
    }
    st.session_state.records = pd.concat(
        [st.session_state.records, pd.DataFrame([new_row])],
        ignore_index=True
    )
    save_records(st.session_state.records)
    st.success("Entry added successfully")

# --- EDITABLE TABLE ---
st.markdown("### Current Records")
st.markdown(
    '<p style="color: var(--neon-blue); font-size:0.85rem; margin-bottom:0.5rem;">'
    '✏️ Click any cell to edit · Changes are saved automatically</p>',
    unsafe_allow_html=True
)

if not st.session_state.records.empty:
    edited_df = st.data_editor(
        st.session_state.records,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
            "category": st.column_config.SelectboxColumn(
                "Category",
                options=["Finances", "Purchases", "Personal", "Admin", "Miscellaneous"]
            ),
            "company": st.column_config.TextColumn("Company"),
            "amount": st.column_config.NumberColumn("Amount (€)", format="€%.2f", min_value=0),
            "paid": st.column_config.NumberColumn("Paid (€)", format="€%.2f", min_value=0),
            "pending": st.column_config.NumberColumn("Pending (€)", format="€%.2f", disabled=True),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=["Completed", "Pending", "On going"]
            ),
        },
        key="records_editor"
    )

    edited_df["pending"] = edited_df["amount"] - edited_df["paid"]
    st.session_state.records = edited_df.reset_index(drop=True)
    save_records(st.session_state.records)

else:
    st.info("No records yet. Add one above!")
