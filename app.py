import streamlit as st
import pandas as pd

# --- 1. SETTINGS ---
st.set_page_config(page_title="VOGUE", layout="wide")

# --- 2. DATA ENGINE ---
@st.cache_data
def load_data():
    return pd.read_csv("products.csv")

df = load_data()

# --- 3. SESSION STATE INITIALIZATION ---
if 'view' not in st.session_state: st.session_state.view = 'gallery'
if 'selected_product' not in st.session_state: st.session_state.selected_product = None
if 'cart' not in st.session_state: st.session_state.cart = []

# --- 4. HEADER ---
st.markdown("<h1 style='text-align:center; font-family:serif;'>VOGUE & ARROW</h1>", unsafe_allow_html=True)

# --- 5. NAVIGATION LOGIC ---
def go_to_product(product):
    st.session_state.selected_product = product
    st.session_state.view = 'details'

def go_to_gallery():
    st.session_state.view = 'gallery'

# --- 6. GALLERY VIEW ---
if st.session_state.view == 'gallery':
    # Sidebar Filters
    with st.sidebar:
        st.header("🛒 Bag")
        if not st.session_state.cart:
            st.write("Your bag is empty.")
        else:
            total = sum(item['Price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"• {item['Name']} (${item['Price']})")
            st.write(f"**Total: ${total:.2f}**")
            if st.button("Proceed to Checkout"):
                st.session_state.view = 'checkout'
                st.rerun()

    # Product Grid
    cols = st.columns(4)
    for idx, row in df.iterrows():
        with cols[idx % 4]:
            st.image(row['Image'], use_container_width=True)
            st.write(f"**{row['Name']}**")
            st.write(f"${row['Price']}")
            if st.button("View Details", key=f"view_{row['ID']}"):
                go_to_product(row)
                st.rerun()

# --- 7. PRODUCT DETAIL VIEW ---
elif st.session_state.view == 'details':
    product = st.session_state.selected_product
    
    if st.button("← Back to Collection"):
        go_to_gallery()
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(product['Image'], use_container_width=True)
    with col2:
        st.title(product['Name'])
        st.subheader(f"${product['Price']}")
        st.write(f"Category: {product['Category']} | Gender: {product['Gender']}")
        st.write("---")
        st.write("Premium quality material, designed for the 2026 Spring/Summer collection. This piece combines comfort with timeless style.")
        
        size = st.selectbox("Select Size", ["S", "M", "L", "XL"])
        
        if st.button("Add to Bag"):
            st.session_state.cart.append({"Name": product['Name'], "Price": product['Price'], "Size": size})
            st.toast(f"Added {product['Name']} to your bag!")

# --- 8. CHECKOUT VIEW ---
elif st.session_state.view == 'checkout':
    st.title("Secure Checkout")
    if st.button("← Return to Shop"):
        go_to_gallery()
        st.rerun()
        
    if not st.session_state.cart:
        st.warning("Your bag is empty!")
    else:
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.markdown("### 1. Delivery Details")
            st.text_input("Full Name")
            st.text_input("Shipping Address")
            st.text_input("Email")
            
        with col_b:
            st.markdown("### 2. Order Summary")
            total = sum(item['Price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"{item['Name']} ({item['Size']}) - ${item['Price']}")
            st.divider()
            st.write(f"**Grand Total: ${total:.2f}**")
            if st.button("Complete Purchase"):
                st.balloons()
                st.success("Thank you! Your order has been placed.")
                st.session_state.cart = []
