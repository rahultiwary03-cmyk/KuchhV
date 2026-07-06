import streamlit as st
import pandas as pd
import os
import random
import difflib
from datetime import datetime

# ==========================================
# 1. SETUP & DATABASE
# ==========================================
st.set_page_config(page_title="KuchhV | Super App", layout="wide", page_icon="🛍️")

PRODUCTS_FILE = "mega_catalog_v9.csv"
ORDERS_FILE = "orders_v9.csv"
PARTNERS_FILE = "partners_v9.csv"

# Professional Blue Sidebar & Dashboard CSS
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%); color: white !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stApp { background-color: #f8fafc; }
    .product-card { background: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; margin-bottom: 15px;}
    .add-btn { background: #10b981; color: white; border: none; padding: 5px 15px; border-radius: 5px; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# Generate Database (If not exists)
if not os.path.exists(PRODUCTS_FILE):
    data = [{"Item_Name": f"Product {i}", "Category": "Grocery", "Price": random.randint(10, 1000)} for i in range(10000)]
    pd.DataFrame(data).to_csv(PRODUCTS_FILE, index=False)

df_catalog = pd.read_csv(PRODUCTS_FILE)

# ==========================================
# 2. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("📱 KuchhV Super App")
st.sidebar.write("---")
app_mode = st.sidebar.radio("Navigation Menu:", ["🏠 Explore Marketplace", "📢 Requirement Hub", "💼 Partner Portal", "⚙️ Admin Control Room"])

# 24/7 Support in Sidebar
st.sidebar.markdown("---")
st.sidebar.write("### 🎧 24/7 Support")
st.sidebar.write("📞 8521413089")
st.sidebar.write("✉️ Rahultiwary03@gmail.com")

# ==========================================
# 3. MARKETPLACE WITH AI SEARCH
# ==========================================
if app_mode == "🏠 Explore Marketplace":
    st.title("🛍️ KuchhV Marketplace")
    query = st.text_input("🔍 Search 10,000+ Items (Typo friendly)...")
    
    # AI Search Logic
    if query:
        all_items = df_catalog['Item_Name'].tolist()
        matches = difflib.get_close_matches(query, all_items, n=10, cutoff=0.3)
        results = df_catalog[df_catalog['Item_Name'].isin(matches)]
    else:
        results = df_catalog.head(12) # Show top items by default

    cols = st.columns(4)
    for i, (_, row) in enumerate(results.iterrows()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class='product-card'>
                <h4>{row['Item_Name']}</h4>
                <p><b>Price: ₹{row['Price']}</b></p>
                <button class='add-btn'>Add to Cart</button>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 4. ADMIN & PARTNER LOGIC (As per requirement)
# ==========================================
elif app_mode == "⚙️ Admin Control Room":
    st.title("⚙️ Admin Center")
    st.write("Manage Catalog, Partners, and Orders here.")
    # Admin tabs and database edit logic same as before...
