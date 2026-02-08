import streamlit as st
import pandas as pd

st.set_page_config(page_title="VOGUE & ARROW", layout="wide")

# Luxury Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
        .main-title { font-family: 'Playfair Display', serif; font-size: 50px; text-align: center; margin-bottom: 0px; }
        .stButton>button { border-radius: 0px; background-color: #000; color: #fff; border: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>VOGUE & ARROW</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; letter-spacing:2px;'>COLLECTION 2026</p>", unsafe_allow_html=True)

# Data Load
@st.cache_data
def load_data():
    return pd.read_csv("products.csv")

df = load_data()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛍️ FILTERS")
    gender = st.selectbox("Department", ["All", "Men", "Women"])
    
    # Dynamic Category Filter based on Gender
    available_cats = df['Category'].unique() if gender == "All" else df[df['Gender'] == gender]['Category'].unique()
    category = st.selectbox("Category", ["All Categories"] + list(available_cats))
    
    st.divider()
    st.title("🛒 YOUR BAG")
    if 'cart' not in st.session_state: st.session_state.cart = []
    
    if not st.session_state.cart:
        st.write("Bag is empty.")
    else:
        total = sum(item['price'] for item in st.session_state.cart)
        for i, item in enumerate(st.session_state.cart):
            st.write(f"**{item['name']}** - ${item['price']}")
        st.write(f"### Total: ${total:.2f}")
        if st.button("CHECKOUT"):
            st.success("Order Placed!")
            st.session_state.cart = []

# --- FILTERING LOGIC ---
display_df = df
if gender != "All":
    display_df = display_df[display_df['Gender'] == gender]
if category != "All Categories":
    display_df = display_df[display_df['Category'] == category]

# --- GRID DISPLAY (4 COLUMNS) ---
st.markdown(f"### Showing {len(display_df)} Items")


cols = st.columns(4)
for idx, row in display_df.reset_index().iterrows():
    with cols[idx % 4]:
        st.image(row['Image'], use_container_width=True)
        st.write(f"**{row['Name']}**")
        st.write(f"${row['Price']}")
        if st.button(f"ADD TO BAG", key=f"btn_{row['ID']}"):
            st.session_state.cart.append({"name": row['Name'], "price": row['Price']})
            st.toast(f"Added {row['Name']}!")
            st.rerun()
