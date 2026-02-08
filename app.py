import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="VOGUE & ARROW", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    .main-title { font-family: 'Playfair Display', serif; font-size: 55px; text-align: center; color: #111; letter-spacing: 3px; }
    .stButton>button { border-radius: 0px; background-color: #000; color: #fff; width: 100%; border: none; }
    .stButton>button:hover { background-color: #444; color: #fff; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='main-title'>VOGUE & ARROW</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; letter-spacing:2px;'>SPRING SUMMER 2026</p>", unsafe_allow_html=True)
st.divider()

# --- DATA ---
@st.cache_data
def get_data():
    return pd.read_csv("products.csv")

try:
    df = get_data()
except:
    st.error("Please ensure products.csv is uploaded to GitHub.")
    st.stop()

# --- SHOPPING BAG (CART) ---
if 'cart' not in st.session_state: st.session_state.cart = []

with st.sidebar:
    st.title("🛒 YOUR BAG")
    if not st.session_state.cart:
        st.write("Bag is empty.")
    else:
        total = 0
        for i, item in enumerate(st.session_state.cart):
            st.write(f"**{item['name']}** - ${item['price']}")
            total += item['price']
        st.divider()
        st.write(f"#### Total: ${total:.2f}")
        if st.button("CHECKOUT"):
            st.success("Order Received!")
            st.session_state.cart = []

# --- PRODUCT GRID ---
cols = st.columns(3)
for idx, row in df.iterrows():
    with cols[idx % 3]:
        st.image(row['Image'], use_container_width=True)
        st.subheader(row['Name'])
        st.write(f"**${row['Price']}**")
        if st.button(f"ADD TO BAG", key=f"btn_{idx}"):
            st.session_state.cart.append({"name": row['Name'], "price": row['Price']})
            st.toast(f"Added {row['Name']}")
            st.rerun()
