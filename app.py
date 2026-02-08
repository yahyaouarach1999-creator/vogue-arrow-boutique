import streamlit as st
import pandas as pd

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="CLOTHYA", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;700&display=swap');
        .stApp { background-color: #FFFFFF; }
        .brand-name { 
            font-family: 'Montserrat', sans-serif; 
            font-size: 65px; 
            text-align: center; 
            font-weight: 700;
            color: #000; 
            letter-spacing: 10px;
            margin-bottom: 0px;
        }
        .stButton>button { 
            border-radius: 0px; 
            background-color: #000; 
            color: #fff; 
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover { background-color: #333; color: #fff; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA LOAD ---
@st.cache_data
def load_data():
    return pd.read_csv("products.csv")

df = load_data()

# --- 3. STATE MANAGEMENT ---
if 'view' not in st.session_state: st.session_state.view = 'gallery'
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_prod_id' not in st.session_state: st.session_state.selected_prod_id = None

# --- 4. HEADER ---
st.markdown("<h1 class='brand-name'>CLOTHYA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; letter-spacing:5px;'>DESIGNED BY YAHYA</p>", unsafe_allow_html=True)
st.divider()

# --- 5. GALLERY VIEW ---
if st.session_state.view == 'gallery':
    # Sidebar Filters & Cart Summary
    with st.sidebar:
        st.header("🛒 YOUR BAG")
        if not st.session_state.cart:
            st.write("Bag is empty.")
        else:
            total = sum(item['Price'] for item in st.session_state.cart)
            for i, item in enumerate(st.session_state.cart):
                c1, c2 = st.columns([3, 1])
                c1.write(f"{item['Name']} (${item['Price']})")
                if c2.button("Remove", key=f"rem_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            st.divider()
            st.write(f"**Total: ${total:.2f}**")
            if st.button("PROCEED TO CHECKOUT"):
                st.session_state.view = 'checkout'
                st.rerun()

    # Product Grid
    cols = st.columns(4)
    for idx, row in df.iterrows():
        with cols[idx % 4]:
            st.image(row['Image'], use_container_width=True)
            st.write(f"**{row['Name']}**")
            st.write(f"${row['Price']}")
            if st.button("SEE DETAILS", key=f"details_{row['ID']}"):
                st.session_state.selected_prod_id = row['ID']
                st.session_state.view = 'details'
                st.rerun()

# --- 6. DETAIL VIEW ---
elif st.session_state.view == 'details':
    product = df[df['ID'] == st.session_state.selected_prod_id].iloc[0]
    
    if st.button("← BACK TO COLLECTION"):
        st.session_state.view = 'gallery'
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(product['Image'], use_container_width=True)
    with col2:
        st.title(product['Name'])
        st.header(f"${product['Price']}")
        st.write(f"Category: {product['Category']} | Gender: {product['Gender']}")
        st.write("---")
        st.write("Exclusively crafted for CLOTHYA. This piece represents the intersection of modern street-style and high-end luxury.")
        
        size = st.select_slider("SELECT SIZE", options=["XS", "S", "M", "L", "XL"])
        
        if st.button("ADD TO BAG"):
            st.session_state.cart.append({"Name": product['Name'], "Price": product['Price'], "Size": size})
            st.toast(f"Added {product['Name']} to Bag!")

# --- 7. CHECKOUT VIEW ---
elif st.session_state.view == 'checkout':
    st.title("CHECKOUT")
    if st.button("← RETURN TO SHOP"):
        st.session_state.view = 'gallery'
        st.rerun()
    
    if not st.session_state.cart:
        st.info("Nothing in your bag yet.")
    else:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Shipping Details")
            st.text_input("Full Name")
            st.text_input("Address Line 1")
            st.text_input("City")
            st.button("CONFIRM & PAY")
        with c2:
            st.subheader("Order Summary")
            total = sum(item['Price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"• {item['Name']} - ${item['Price']}")
            st.divider()
            st.write(f"### TOTAL: ${total:.2f}")
