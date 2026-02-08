import streamlit as st
import pandas as pd

# --- CLOTHYA BRANDING ---
st.set_page_config(page_title="CLOTHYA | Fes to NYC", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@400;600&display=swap');
        .stApp { background-color: #FCF9F5; }
        .brand { font-family: 'Cinzel', serif; font-size: 60px; text-align: center; color: #1E3A8A; letter-spacing: 10px; margin-bottom: 0px; }
        .sub-brand { font-family: 'Inter', sans-serif; text-align: center; color: #B45309; letter-spacing: 5px; font-weight: 600; margin-top: -10px; }
        .stButton>button { border-radius: 0px; background-color: #1E3A8A; color: white; border: none; font-weight: 600; }
        .stButton>button:hover { background-color: #B45309; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_products():
    return pd.read_csv("products.csv")

try:
    df = load_products()
except:
    st.error("Missing products.csv! Please upload it to your GitHub.")
    st.stop()

# --- INITIALIZE STATE ---
if 'view' not in st.session_state: st.session_state.view = 'gallery'
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_id' not in st.session_state: st.session_state.selected_id = None

# --- HEADER ---
st.markdown("<h1 class='brand'>CLOTHYA</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-brand'>MOROCCAN HERITAGE • USA STREETWEAR</p>", unsafe_allow_html=True)
st.divider()

# --- NAVIGATION ---
if st.session_state.view == 'gallery':
    with st.sidebar:
        st.title("🏺 SOUK FILTERS")
        gender = st.radio("Department", ["All", "Men", "Women"])
        st.divider()
        st.title("🛒 BAG")
        if not st.session_state.cart: st.write("Bag is empty.")
        else:
            for i, item in enumerate(st.session_state.cart):
                st.write(f"• {item['Name']} (${item['Price']})")
            if st.button("CHECKOUT"): 
                st.session_state.view = 'checkout'
                st.rerun()

    # Filtered View
    display_df = df if gender == "All" else df[df['Gender'] == gender]
    
    # 4-Column Grid
    cols = st.columns(4)
    for idx, row in display_df.reset_index().iterrows():
        with cols[idx % 4]:
            st.image(row['Image'], use_container_width=True)
            st.write(f"**{row['Name']}**")
            st.write(f"${row['Price']}")
            if st.button("DISCOVER", key=f"btn_{row['ID']}"):
                st.session_state.selected_id = row['ID']
                st.session_state.view = 'details'
                st.rerun()

elif st.session_state.view == 'details':
    prod = df[df['ID'] == st.session_state.selected_id].iloc[0]
    if st.button("← BACK"):
        st.session_state.view = 'gallery'
        st.rerun()
    
    c1, c2 = st.columns(2)
    with c1:
        st.image(prod['Image'], use_container_width=True)
    with c2:
        st.title(prod['Name'])
        st.header(f"${prod['Price']}")
        st.write("Exclusively crafted Moroccan-USA fusion piece. Blending NYC functionality with Marrakech textures.")
        size = st.selectbox("Size", ["S", "M", "L", "XL"])
        if st.button("ADD TO BAG"):
            st.session_state.cart.append({"Name": prod['Name'], "Price": prod['Price'], "Size": size})
            st.toast("Added!")

elif st.session_state.view == 'checkout':
    st.title("Checkout")
    if st.button("← BACK"): st.session_state.view = 'gallery'; st.rerun()
    st.write("Order confirmation and payment integration goes here.")
