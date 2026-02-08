import streamlit as st
import pandas as pd

# --- 1. SETTINGS & MOROCCAN-USA THEME ---
st.set_page_config(page_title="CLOTHYA | Fes to NYC", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@300;600&display=swap');
        
        .stApp { background-color: #FFFDF9; } /* Sand Beige Tint */
        
        .brand-name { 
            font-family: 'Cinzel', serif; 
            font-size: 70px; 
            text-align: center; 
            color: #1E3A8A; /* Atlas Blue */
            letter-spacing: 12px;
            margin-bottom: 0px;
        }
        
        .motto {
            text-align: center;
            color: #B45309; /* Saffron Orange */
            letter-spacing: 4px;
            font-weight: 600;
            margin-top: -10px;
        }

        /* Styling buttons to look like leather/luxury tags */
        .stButton>button { 
            border-radius: 0px; 
            background-color: #1E3A8A; 
            color: #fff; 
            border: 2px solid #1E3A8A;
            font-weight: 600;
        }
        .stButton>button:hover { 
            background-color: #B45309; 
            border-color: #B45309;
            color: white; 
        }
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
st.markdown("<p class='motto'>MARRAKECH HERITAGE • NYC STREETWEAR</p>", unsafe_allow_html=True)
st.write("---")

# --- 5. GALLERY VIEW ---
if st.session_state.view == 'gallery':
    with st.sidebar:
        st.markdown("### 🏺 COLLECTIONS")
        gender = st.radio("Department", ["All", "Men", "Women"])
        
        st.divider()
        st.markdown("### 🛒 SHOPPING BAG")
        if not st.session_state.cart:
            st.write("Empty bag.")
        else:
            total = sum(item['Price'] for item in st.session_state.cart)
            for i, item in enumerate(st.session_state.cart):
                c1, c2 = st.columns([3, 1])
                c1.write(f"{item['Name']} ({item['Size']})")
                if c2.button("✕", key=f"rem_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            st.write(f"**Total: ${total:.2f}**")
            if st.button("PROCEED TO CHECKOUT"):
                st.session_state.view = 'checkout'
                st.rerun()

    # Filtered View
    display_df = df if gender == "All" else df[df['Gender'] == gender]
    
    
    cols = st.columns(4)
    for idx, row in display_df.reset_index().iterrows():
        with cols[idx % 4]:
            st.image(row['Image'], use_container_width=True)
            st.markdown(f"**{row['Name']}**")
            st.write(f"${row['Price']}")
            if st.button("DISCOVER", key=f"det_{row['ID']}"):
                st.session_state.selected_prod_id = row['ID']
                st.session_state.view = 'details'
                st.rerun()

# --- 6. DETAIL VIEW ---
elif st.session_state.view == 'details':
    product = df[df['ID'] == st.session_state.selected_prod_id].iloc[0]
    
    if st.button("← BACK TO SOUK"):
        st.session_state.view = 'gallery'
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(product['Image'], use_container_width=True)
    with col2:
        st.title(product['Name'])
        st.subheader(f"${product['Price']}")
        st.write("---")
        st.write("**Designer's Note:** Hand-selected patterns inspired by Moroccan Zellige and North African textures, tailored for a modern Western silhouette.")
        
        size = st.selectbox("SELECT SIZE", ["S", "M", "L", "XL"])
        if st.button("ADD TO BAG"):
            st.session_state.cart.append({"Name": product['Name'], "Price": product['Price'], "Size": size})
            st.toast("Item added to bag!")

# --- 7. CHECKOUT VIEW ---
elif st.session_state.view == 'checkout':
    st.title("Secure Checkout")
    if st.button("← RETURN"):
        st.session_state.view = 'gallery'
        st.rerun()
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.text_input("Full Name")
        st.text_input("Shipping Address")
        if st.button("COMPLETE ORDER"):
            st.balloons()
            st.success("B'saha! Your order is confirmed.")
            st.session_state.cart = []
    with c2:
        st.markdown("### Order Summary")
        for item in st.session_state.cart:
            st.write(f"• {item['Name']} - ${item['Price']}")
