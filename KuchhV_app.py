import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime

# ==========================================
# 1. SETUP & MEGA DATABASE GENERATOR
# ==========================================
st.set_page_config(page_title="KuchhV | Super App", layout="centered", initial_sidebar_state="collapsed")

PRODUCTS_FILE = "mega_catalog_v7.csv"

# Fast Generator for 10,000+ Items (Runs only once)
def generate_mega_catalog():
    categories = {
        "Grocery & Staples": ["Rice", "Dal", "Atta", "Oil", "Sugar", "Salt", "Spices", "Poha", "Besan", "Maida"],
        "Fresh Vegetables": ["Potato", "Onion", "Tomato", "Cabbage", "Carrot", "Spinach", "Capsicum", "Garlic", "Ginger"],
        "Electronics & Gadgets": ["Earphones", "Charger", "Power Bank", "Smart Watch", "USB Cable", "Mouse", "Keyboard"],
        "Local Shops (Sweets/Snacks)": ["Samosa", "Jalebi", "Rasgulla", "Paneer", "Ladoo", "Namkeen", "Kaju Katli"],
        "Home Services": ["Plumber Visit", "Electrician Visit", "AC Repair", "Washing Machine Repair", "House Cleaning"],
        "Local Jobs": ["Data Entry Operator", "Delivery Partner", "Shop Assistant", "Cook (Home Kitchen)", "Mechanic"],
        "Heavy Machinery & Rentals": ["Tractor Rental", "JCB Booking", "Tata Ace", "Concrete Mixer", "Water Tanker"],
        "Apparel & Fashion": ["Cotton T-Shirt (Typography)", "Jeans", "Formal Shirt", "Sports Shoes", "Socks", "Cap"]
    }
    
    brands = ["Premium", "Standard", "Local", "Fresh", "Super", "Gold", "Classic"]
    data = []
    
    # Generate 10,000 items mathematically
    for i in range(10050):
        cat = random.choice(list(categories.keys()))
        item_base = random.choice(categories[cat])
        brand = random.choice(brands)
        
        # Format pricing and names based on category
        if cat == "Local Jobs":
            item_name = f"{item_base} ({brand} Firm)"
            price = random.randint(7000, 18000) # Monthly Salary
            img_text = "Job"
            color = "10b981"
        elif cat == "Home Services":
            item_name = f"{item_base} - {brand} Service"
            price = random.randint(149, 999)
            img_text = "Service"
            color = "3b82f6"
        else:
            item_name = f"{brand} {item_base} - Var {random.randint(1, 500)}"
            price = random.randint(30, 2500)
            img_text = item_base.replace(" ", "+")
            color = "f59e0b"
            
        img_url = f"https://placehold.co/300x300/{color}/ffffff?text={img_text}"
        
        data.append({
            "ID": f"KV{10000+i}",
            "Item_Name": item_name,
            "Category": cat,
            "Price": price,
            "Image_URL": img_url,
            "Partner_Type": "Verified"
        })
    
    df = pd.DataFrame(data)
    df.to_csv(PRODUCTS_FILE, index=False)
    return df

if not os.path.exists(PRODUCTS_FILE):
    with st.spinner("Generating 10,000+ Items Mega Database..."):
        df_catalog = generate_mega_catalog()
else:
    df_catalog = pd.read_csv(PRODUCTS_FILE)

# ==========================================
# 2. MOBILE-FIRST CSS DESIGN
# ==========================================
st.markdown("""
    <style>
    /* Simulate Mobile App Container */
    .stApp { background-color: #f3f4f6; font-family: 'Segoe UI', sans-serif; }
    
    /* Header styling */
    .app-header { background: #ffffff; padding: 15px; border-bottom: 1px solid #e5e7eb; position: sticky; top: 0; z-index: 999; display: flex; justify-content: space-between; align-items: center;}
    .loc-text { font-size: 13px; color: #4b5563; font-weight: 600;}
    .loc-title { font-size: 16px; color: #111827; font-weight: 800;}
    
    /* Custom Order Voice Box (Like your screenshot) */
    .custom-order-box { background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 16px; color: white; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2);}
    .custom-order-box h3 { margin: 0; font-size: 18px; color: white;}
    .voice-input-mock { background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; margin-top: 10px; display: flex; justify-content: space-between;}
    
    /* Grid & Cards */
    .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding-bottom: 80px;}
    .job-card { background: white; padding: 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #e5e7eb;}
    .job-title { font-size: 16px; font-weight: 700; color: #111827;}
    .job-sal { color: #059669; font-weight: 700; font-size: 14px; margin: 5px 0;}
    
    .item-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; position: relative;}
    .item-img { width: 100%; height: 140px; object-fit: cover;}
    .item-info { padding: 10px;}
    .item-title { font-size: 14px; font-weight: 600; color: #374151; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
    .item-price { font-size: 16px; font-weight: 800; color: #111827; margin-top: 4px;}
    .add-btn { background: #10b981; color: white; border-radius: 6px; padding: 4px 12px; font-size: 12px; font-weight: bold; float: right; border: none;}
    
    /* Hide Streamlit default UI elements for app feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. APP HEADER
# ==========================================
st.markdown("""
<div class="app-header">
    <div>
        <div class="loc-text">Deliver To <span style="color:#10b981;">▼</span></div>
        <div class="loc-title">Ward 4, Main Road, Chatra</div>
    </div>
    <div style="font-size: 24px;">👤</div>
</div>
""", unsafe_allow_html=True)

search_query = st.text_input("🔍 Search 10,000+ Products, Jobs & Services...")

# ==========================================
# 4. BOTTOM NAVIGATION TABS
# ==========================================
tab_home, tab_grocery, tab_shops, tab_jobs, tab_profile = st.tabs(["🏠 Home", "🛒 Grocery", "🏪 Shops", "💼 Jobs", "👤 Profile"])

with tab_home:
    st.markdown("""
    <div class="custom-order-box">
        <h3>⚡ Custom Order</h3>
        <p style="font-size: 13px; margin:0;">Can't find it? Just type or record what you need.</p>
        <div class="voice-input-mock">
            <span>e.g., 1kg fresh paneer...</span>
            <span>🎤</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔥 Popular Right Now")
    home_items = df_catalog.sample(6)
    
    cols = st.columns(2)
    for i, (_, row) in enumerate(home_items.iterrows()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="item-card">
                <img src="{row['Image_URL']}" class="item-img">
                <div class="item-info">
                    <div class="item-title">{row['Item_Name']}</div>
                    <div class="item-price">₹{row['Price']} <button class="add-btn">ADD</button></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")

with tab_grocery:
    st.subheader("Groceries & Staples")
    st.caption("Delivery in ~30 min from shops near Chatra")
    
    # Filter only Grocery
    g_items = df_catalog[df_catalog['Category'] == 'Grocery & Staples'].head(10)
    for _, row in g_items.iterrows():
        st.markdown(f"""
        <div style="background:white; padding:12px; border-radius:12px; margin-bottom:10px; display:flex; align-items:center; border: 1px solid #e5e7eb;">
            <img src="{row['Image_URL']}" style="width:60px; height:60px; border-radius:8px; margin-right:15px;">
            <div style="flex-grow: 1;">
                <div style="font-weight:700; font-size:15px;">{row['Item_Name']}</div>
                <div style="font-weight:800; font-size:16px; color:#111827;">₹{row['Price']}</div>
            </div>
            <button class="add-btn" style="padding: 8px 16px; font-size: 14px;">Add</button>
        </div>
        """, unsafe_allow_html=True)

with tab_shops:
    st.subheader("Local Shops Near You")
    shops = ["Maa Sharda Sweets", "Verma Hardware", "Green Medicos", "Jai Maa Stationery", "Chatra General Store"]
    for shop in shops:
        rating = round(random.uniform(4.0, 4.9), 1)
        dist = round(random.uniform(0.2, 3.5), 1)
        st.markdown(f"""
        <div class="job-card" style="display:flex; align-items:center;">
            <div style="font-size:30px; background:#f3f4f6; padding:10px; border-radius:10px; margin-right:15px;">🏪</div>
            <div>
                <div class="job-title">{shop}</div>
                <div style="font-size:13px; color:#6b7280;">⭐ {rating} • 📍 {dist} km away</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_jobs:
    st.subheader("Local Jobs (Work near home)")
    st.caption("Connecting Chatra businesses with local talent.")
    
    jobs_df = df_catalog[df_catalog['Category'] == 'Local Jobs'].head(5)
    for _, row in jobs_df.iterrows():
        st.markdown(f"""
        <div class="job-card">
            <div style="float:right; background:#fef3c7; color:#d97706; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:bold;">Full-time</div>
            <div class="job-title">{row['Item_Name']}</div>
            <div style="font-size:13px; color:#6b7280; margin: 4px 0;">🏢 KuchhV Verified Partner</div>
            <div class="job-sal">₹{row['Price']}/mo  <span style="color:#6b7280; font-weight:normal; font-size:12px;">📍 Chatra</span></div>
            <button style="width:100%; background:#10b981; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; margin-top:10px;">Apply now</button>
        </div>
        """, unsafe_allow_html=True)

with tab_profile:
    st.markdown("""
    <div style="background:#10b981; color:white; padding:20px; border-radius:16px; margin-top:10px;">
        <h2 style="color:white; margin:0;">Aarti Kumari</h2>
        <p style="margin:5px 0;">📞 +91 98xxx xxx21</p>
        <p style="margin:0; font-size:14px;">📍 Ward 4, Main Road, Chatra</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("#### 📦 My orders & bookings")
    st.markdown("#### 📍 Saved addresses")
    st.markdown("#### ❤️ Favourites")
    st.markdown("#### 🎧 Help & support")
