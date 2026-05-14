import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.markdown("<style>" + open("styles.css").read() + "</style>", unsafe_allow_html=True)

# --- LOAD DATA ---
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

if "records" not in st.session_state:
    st.session_state.records = load_records()

df = st.session_state.records

# --- TITLE ---
st.markdown("""
    <div style="text-align:center; overflow:visible; padding: 0.5rem 0 1.5rem;">
        <h1 class="glitch" data-text="FINANCES DASHBOARD">FINANCES DASHBOARD</h1>
    </div>
""", unsafe_allow_html=True)

if df.empty:
    st.info("No records yet. Head to **Add Records** to get started.")
    st.stop()

# --- PRECOMPUTE ---
category_totals   = df.groupby("category")["amount"].sum().reset_index()
pending_by_cat    = df.groupby("category")["pending"].sum().reset_index()
total_pending     = df["pending"].sum()

# --- NEON COLOUR MAP (one per category, cycles if more) ---
NEON_COLOURS = [
    "#03ffff",  # blue
    "#ff00ff",  # pink
    "#4bff21",  # green
    "#f8e602",  # yellow
    "#bd00ff",  # purple
    "#ff6b35",  # orange
]
categories   = category_totals["category"].tolist()
colour_map   = {cat: NEON_COLOURS[i % len(NEON_COLOURS)] for i, cat in enumerate(categories)}

# ── ROW 1: pie chart + total pending card ────────────────────────────────────
col_chart, col_total = st.columns([2, 1], gap="large")

with col_chart:
    fig = px.pie(
        category_totals,
        names="category",
        values="amount",
        title="Spending by Category",
        color="category",
        color_discrete_map=colour_map,
        hole=0.35,
    )
    fig.update_traces(
        textfont_size=13,
        textfont_color="white",
        marker=dict(line=dict(color="#02022d", width=2)),
        hovertemplate="<b>%{label}</b><br>€%{value:,.2f}<br>%{percent}<extra></extra>",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Orbitron, sans-serif", color="#000000", size=12),
        title_font=dict(family="Orbitron, sans-serif", color="#ff00ff", size=16),
        legend=dict(
            font=dict(color="#03ffff", size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(t=50, b=20, l=20, r=20),
    )
    st.plotly_chart(fig, width="stretch")

with col_total:
    # vertical centering trick
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="neon-card" style="text-align:center; padding: 2rem 1.5rem;">
            <div style="
                color: var(--neon-blue);
                font-family: 'Orbitron', sans-serif;
                font-size: 0.75rem;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                text-shadow: 0 0 8px var(--neon-blue);
                margin-bottom: 1rem;
            ">Total Pending</div>
            <div style="
                color: var(--neon-yellow);
                font-family: 'Orbitron', sans-serif;
                font-size: 2.2rem;
                font-weight: 700;
                text-shadow: 0 0 16px var(--neon-yellow), 0 0 40px rgba(248,230,2,0.4);
                line-height: 1.1;
            ">€ {total_pending:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── ROW 2: per-category cards ────────────────────────────────────────────────
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.markdown("""
    <div style="
        color: var(--neon-pink);
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        text-shadow: 0 0 6px var(--neon-pink);
        margin-bottom: 1rem;
        text-align: center;
    ">Pending by Category</div>
""", unsafe_allow_html=True)

for _, row in pending_by_cat.iterrows():
    cat    = row["category"]
    amount = row["pending"]
    colour = colour_map.get(cat, "#03ffff")

    st.markdown(
        f"""
        <div class="neon-card category-row" style="
            border-color: {colour};
            box-shadow: 0 0 12px {colour}44;
        ">
            <span style="
                font-family: 'Orbitron', sans-serif;
                font-size: 0.95rem;
                color: {colour};
                text-shadow: 0 0 8px {colour};
                letter-spacing: 0.08em;
                text-transform: uppercase;
            ">{cat}</span>
            <span style="
                font-family: 'Orbitron', sans-serif;
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--neon-yellow);
                text-shadow: 0 0 10px var(--neon-yellow);
            ">€ {amount:,.2f}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
