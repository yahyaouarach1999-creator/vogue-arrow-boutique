import streamlit as st
import pandas as pd

# --- 1. SETTINGS & BOUTIQUE THEME ---
st.set_page_config(page_title="VOGUE & ARROW", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
        .stApp { background-color: #FFFFFF; }
        .main-title { 
            font-family: 'Playfair Display', serif; 
            font-size: 60px; 
            text-align: center; 
            color: #111; 
            letter-spacing: 4px;
            margin-bottom: 0px;
        }
        .stButton>button { 
            border-radius: 0px; 
            background-color: #000; 
            color: #fff; 
            width: 100%; 
            border: none; 
            transition: 0.3s;
        }
        .stButton>button:hover { background-color: #444; }
        .price-tag { font-weight: bold; font-size: 20px; color: #333; }
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.markdown("<h1 class='main-title'>VOGUE & ARROW</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; letter-spacing:3px; font-size:14px;'>SPRING SUMMER 2026</p>", unsafe_allow_html=True)
st.divider()

# --- 3. DATA ENGINE (The Inventory) ---
@st.cache_data
def load_products():
    # If you have a products.csv, use: return pd.read_csv("products.csv")
    # For now, we use these high-end placeholders:
    data = {
        'Name': ['Classic Silk Blouse', 'Tailored Wool Blazer', 'High-Waist Denim', 'Linen Midi Dress', 'Cashmere Sweater', 'Leather Chelsea Boot'],
        'Category': ['Tops', 'Outerwear', 'Bottoms', 'Dresses', 'Knitwear', 'Accessories'],
        'Price': [120, 350, 95, 180, 210, 290],
        'Image': [
            'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=500',
            'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500',
            'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500',
            'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=500',
            'https://images.unsplash.com/photo-1556905055-8f358a7a4bb4?w=500',
            'https://images.unsplash.com/photo-1638247025967-b4e38f787b76?w=500'
        ]
    }
    return pd.DataFrame(data)

df = load_products()

# --- 4. SIDEBAR & CART ---
if 'cart' not in st.session_state: st.session_state.cart = []

with st.sidebar:
    st.markdown("### 🏷️ COLLECTIONS")
    cat = st.selectbox("Filter by Category", ["All Collections"] + list(df['Category'].unique()))
    
    st.divider()
    st.markdown("### 🛒 YOUR BAG")
    if not st.session_state.cart:
        st.write("Your bag is empty.")
    else:
        total = sum(item['price'] for item in st.session_state.cart)
        for i, item in enumerate(st.session_state.cart):
            st.write(f"**{item['name']}** - ${item['price']}")
        st.write(f"**TOTAL: ${total:.2f}**")
        if st.button("CLEAR BAG"):
            st.session_state.cart = []
            st.rerun()

# --- 5. PRODUCT GRID ---
filtered_df = df if cat == "All Collections" else df[df['Category'] == cat]

# Layout for a clean boutique grid

cols = st.columns(3)
for idx, row in filtered_df.reset_index().iterrows():
    with cols[idx % 3]:
        st.image(row['Image'], use_container_width=True)
        st.subheader(row['Name'])
        st.markdown(f"<p class='price-tag'>${row['Price']}</p>", unsafe_allow_html=True)
        if st.button(f"ADD TO BAG", key=f"btn_{idx}"):
            st.session_state.cart.append({"name": row['Name'], "price": row['Price']})
            st.toast(f"Added {row['Name']} to bag!")
            st.rerun()
