import streamlit as st
import pandas as pd

# --- BRAND CONFIG ---
st.set_page_config(page_title="CLOTHYA | Fes x NYC", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@400;600&display=swap');
        .stApp { background-color: #FCF9F5; }
        .brand { font-family: 'Cinzel', serif; font-size: 75px; text-align: center; color: #1E3A8A; letter-spacing: 12px; margin-bottom: 0px; }
        .motto { font-family: 'Inter', sans-serif; text-align: center; color: #B45309; letter-spacing: 5px; font-weight: 600; margin-top: -10px; }
        
        .stButton>button { 
            border-radius: 0px; 
            background-color: #1E3A8A; 
            color: white; 
            border: none;
            width: 100%;
            height: 45px;
            font-weight: bold;
        }
        .stButton>button:hover { background-color: #B45309; transition: 0.3s; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv("products.csv")

df = load_data()

# --- INITIALIZE STATE ---
if 'view' not in st.session_state: st.session_state.view = 'gallery'
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_id' not in st.session_state: st.session_state.selected_id = None

# --- HEADER ---
st.markdown("<h1 class='brand'>CLOTHYA</h1>", unsafe_allow_html=True)
st.markdown("<p class='motto'>MARRAKECH SOUL • AMERICAN STYLE</p>", unsafe_allow_html=True)
st.divider()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("### 🏺 DISCOVER")
    gender = st.radio("Gender", ["All", "Men", "Women"])
    cat = st.selectbox("Category", ["All Categories"] + list(df['Category'].unique()))
    
    st.divider()
    st.markdown(f"### 🛒 BAG ({len(st.session_state.cart)})")
    if len(st.session_state.cart) > 0:
        if st.button("PROCEED TO CHECKOUT"):
            st.session_state.view = 'checkout'
            st.rerun()

# --- VIEW CONTROLLER ---
if st.session_state.view == 'gallery':
    # Filtering
    filtered = df
    if gender != "All": filtered = filtered[filtered['Gender'] == gender]
    if cat != "All Categories": filtered = filtered[filtered['Category'] == cat]

    # Grid Display
    
    cols = st.columns(4)
    for idx, row in filtered.reset_index().iterrows():
        with cols[idx % 4]:
            st.image(row['Image'], use_container_width=True)
            st.write(f"**{row['Name']}**")
            st.write(f"${row['Price']}")
            if st.button("SEE PIECE", key=f"p_{row['ID']}"):
                st.session_state.selected_id = row['ID']
                st.session_state.view = 'details'
                st.rerun()

elif st.session_state.view == 'details':
    prod = df[df['ID'] == st.session_state.selected_id].iloc[0]
    if st.button("← BACK TO COLLECTION"):
        st.session_state.view = 'gallery'
        st.rerun()
        
    c1, c2 = st.columns(2)
    with c1:
        st.image(prod['Image'], use_container_width=True)
    with c2:
        st.title(prod['Name'])
        st.header(f"${prod['Price']}")
        st.markdown("---")
        st.write("A signature CLOTHYA piece. Fusing the ancient artisan spirit of Fes with modern Manhattan street aesthetics.")
        size = st.selectbox("SELECT SIZE", ["S", "M", "L", "XL"])
        if st.button("ADD TO BAG"):
            st.session_state.cart.append(prod['Name'])
            st.toast(f"{prod['Name']} added!")

elif st.session_state.view == 'checkout':
    st.title("Checkout")
    if st.button("← BACK"):
        st.session_state.view = 'gallery'
        st.rerun()
    st.info("Payment portal loading...")
