import streamlit as st
import pandas as pd
import os
import random
import difflib
from datetime import datetime

# ==========================================
# 1. SETUP & MEGA DATABASE GENERATOR
# ==========================================
st.set_page_config(page_title="KuchhV | Super App", layout="centered", initial_sidebar_state="collapsed")

PRODUCTS_FILE = "mega_catalog_v8.csv"

@st.cache_data
def generate_mega_catalog():
    # Massive Pan-India Categories
    categories = {
        "Grocery & Staples": ["Rice", "Dal", "Atta", "Refined Oil", "Mustard Oil", "Sugar", "Salt", "Spices", "Poha", "Besan", "Maida", "Dry Fruits"],
        "Fresh Produce & Dairy": ["Potato", "Onion", "Tomato", "Milk 1L", "Paneer 1kg", "Curd", "Apple", "Banana", "Mango"],
        "Local Shops & Eateries": ["Samosa", "Jalebi", "Rasgulla", "Kaju Katli", "Namkeen", "Cold Drink", "Burger", "Pizza"],
        "Home Repairs & Maintenance": ["Plumber Visit", "Electrician Visit", "AC Service", "Washing Machine Repair", "RO Repair", "Carpenter"],
        "Freelance & IT Services": ["Data Entry (Excel)", "Python Developer", "Website Setup", "Logo Design", "Video Editing", "Social Media Manager"],
        "Local Jobs & Hiring": ["Data Entry Operator", "Delivery Boy", "Shop Assistant", "Cook (Home Kitchen)", "Mechanic", "Security Guard", "Bouncer"],
        "Heavy Machinery & Transport": ["Tractor Rental", "JCB Booking", "Tata Ace Booking", "Concrete Mixer", "Water Tanker", "Bike Taxi", "Cab Booking"],
        "E-Governance & Paperwork": ["Pension Form Fill", "JMMMSY Registration", "GST Filing", "ITR Return", "Aadhaar Update Help", "Notary Affidavit"],
        "Fashion & Apparel": ["Cotton T-Shirt", "Typography Shirt", "Jeans", "Formal Pants", "Sneakers", "Socks", "Cap"],
        "Events & Ceremonies": ["Tent House Set", "DJ Booking", "Halwai (Caterer)", "Pandit Ji (Puja)", "Bridal Makeup", "Mehndi Artist"]
    }
    
    brands = ["Premium", "Standard", "Local", "Fresh", "Super", "Gold", "Classic", "Verified"]
    districts = ["Chatra", "Ranchi", "Hazaribagh", "Patna", "Gaya", "Muzaffarpur", "Kanpur", "Delhi", "Pan-India"]
    data = []
    
    # Generate 10,000+ items
    for i in range(10100):
        cat = random.choice(list(categories.keys()))
        item_base = random.choice(categories[cat])
        brand = random.choice(brands)
        district = random.choice(districts)
        
        # Dynamic Formatting based on category
        if "Jobs" in cat:
            item_name = f"{item_base} ({brand} Firm)"
            price = random.randint(7000, 25000) # Monthly Salary
            img_text = "Job+Vacancy"
            color = "10b981"
        elif "Services" in cat or "Repairs" in cat or "Governance" in cat:
            item_name = f"{item_base} - {brand} Service"
            price = random.randint(99, 1500)
            img_text = item_base.replace(" ", "+")
            color = "3b82f6"
        else:
            item_name = f"{brand} {item_base} ({random.randint(1, 5)} kg/pc)"
            price = random.randint(30, 2500)
            img_text = item_base.replace(" ", "+")
            color = "f59e0b"
            
        img_url = f"https://placehold.co/300x300/{color}/ffffff?text={img_text}"
        
        data.append({
            "ID": f"KV{10000+i}",
            "Item_Name": item_name,
            "Category": cat,
            "Price": price,
            "Location": district,
            "Image_URL": img_url,
        })
    
    df = pd.DataFrame(data)
    df.to_csv(PRODUCTS_FILE, index=False)
    return df

# Initialize Data
if not os.path.exists(PRODUCTS_FILE):
    with st.spinner("Generating 10,000+ Items Mega Database for all districts..."):
        df_catalog = generate_mega_catalog()
else:
    df_catalog = pd.read_csv(PRODUCTS_FILE)

# ==========================================
# 2. AI SMART SEARCH ENGINE (Fuzzy Logic)
# ==========================================
def smart_search(query, df):
    query = str(query).lower().strip()
    if not query:
        return pd.DataFrame()
        
    # 1. Direct/Substring Match
    exact_matches = df[df['Item_Name'].str.lower().str.contains(query) | df['Category'].str.lower().str.contains(query)]
    if not exact_matches.empty:
        return exact_matches
        
    # 2. AI Fuzzy Match (Auto-corrects Typos like 'palambar' -> 'plumber')
    all_words = set(" ".join(df['Item_Name'].str.lower().tolist() + df['Category'].str.lower().tolist()).split())
    close_words = difflib.get_close_matches(query, all_words, n=3, cutoff=0.5)
    
    if close_words:
        # If it finds a typo correction, search using the corrected words
        pattern = '|'.join(close_words)
        fuzzy_matches = df[df['Item_Name'].str.lower().str.contains(pattern, regex=True) | df['Category'].str.lower().str.contains(pattern, regex=True)]
        return fuzzy_matches
        
    return pd.DataFrame() # Still empty

# ==========================================
# 3. MOBILE-FIRST UI CSS
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f3f4f6; font-family: 'Segoe UI', sans-serif; }
    .app-header { background: #ffffff; padding: 15px; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;}
    .loc-text { font-size: 13px; color: #4b5563; font-weight: 600;}
    .loc-title { font-size: 16px; color: #111827; font-weight: 800;}
    
    .search-container { padding: 15px; background: white; border-bottom: 1px solid #e5e7eb; }
    
    .item-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; position: relative; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .item-img { width: 100%; height: 160px; object-fit: cover; background: #e5e7eb;}
    .item-info { padding: 12px;}
    .item-title { font-size: 15px; font-weight: 700; color: #1f2937; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
    .item-cat { font-size: 12px; color: #6b7280; margin-bottom: 8px;}
    .item-price { font-size: 18px; font-weight: 800; color: #059669;}
    .add-btn { background: #10b981; color: white; border-radius: 6px; padding: 6px 16px; font-size: 14px; font-weight: bold; float: right; border: none; cursor: pointer;}
    
    .fallback-box { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; margin: 20px 0;}
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. APP HEADER & SEARCH LAYER
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

st.markdown("<div class='search-container'>", unsafe_allow_html=True)
search_query = st.text_input("🔍 Search 10,000+ Products, Jobs & Services...", placeholder="Try 'atta', 'tretar', 'palambar', 'job'...")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. DYNAMIC CONTENT RENDERING
# ==========================================
if search_query:
    results = smart_search(search_query, df_catalog)
    
    if not results.empty:
        st.success(f"🔍 Found {len(results)} results matching your search:")
        
        # Display top 10 results to keep mobile UI clean
        display_results = results.head(10)
        cols = st.columns(2)
        for i, (_, row) in enumerate(display_results.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="item-card">
                    <img src="{row['Image_URL']}" class="item-img">
                    <div class="item-info">
                        <div class="item-title">{row['Item_Name']}</div>
                        <div class="item-cat">📍 {row['Location']} • {row['Category']}</div>
                        <div class="item-price">₹{row['Price']} <button class="add-btn">Get</button></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    else:
        # THE FALLBACK MECHANISM (Khali Kuchh V Nahi Rhe)
        st.markdown("""
        <div class="fallback-box">
            <h3 style="color:white; margin-top:0;">🤖 We couldn't find an exact match</h3>
            <p style="font-size:14px; margin-bottom:0;">But don't worry! Tap below to send this directly to local partners. They will arrange it for you.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("👉 Request Custom Order", expanded=True):
            st.text_area("Your Requirement", value=search_query)
            st.text_input("Phone Number")
            st.button("Send Request to Local Partners 🚀", type="primary")
            
        st.write("---")
        st.subheader("🔥 Popular in your area instead:")
        
        # Show random popular items so screen is never empty
        home_items = df_catalog.sample(4)
        cols = st.columns(2)
        for i, (_, row) in enumerate(home_items.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="item-card">
                    <img src="{row['Image_URL']}" class="item-img">
                    <div class="item-info">
                        <div class="item-title">{row['Item_Name']}</div>
                        <div class="item-price">₹{row['Price']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

else:
    # DEFAULT HOME SCREEN (When search is empty)
    tab_home, tab_grocery, tab_services, tab_jobs = st.tabs(["🏠 Home", "🛒 Grocery", "🔧 Services", "💼 Jobs"])

    with tab_home:
        st.subheader("Daily Deals & Essentials")
        home_items = df_catalog[df_catalog['Category'] == 'Grocery & Staples'].sample(4)
        cols = st.columns(2)
        for i, (_, row) in enumerate(home_items.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="item-card">
                    <img src="{row['Image_URL']}" class="item-img">
                    <div class="item-info">
                        <div class="item-title">{row['Item_Name']}</div>
                        <div class="item-price">₹{row['Price']} <button class="add-btn">Add</button></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        st.write("---")
        st.subheader("Top Local Services")
        service_items = df_catalog[df_catalog['Category'] == 'Home Repairs & Maintenance'].sample(2)
        for _, row in service_items.iterrows():
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:12px; margin-bottom:15px; display:flex; align-items:center; border: 1px solid #e5e7eb;">
                <img src="{row['Image_URL']}" style="width:70px; height:70px; border-radius:8px; margin-right:15px; object-fit: cover;">
                <div style="flex-grow: 1;">
                    <div style="font-weight:700; font-size:15px; color:#111827;">{row['Item_Name']}</div>
                    <div style="font-size:13px; color:#6b7280;">📍 {row['Location']}</div>
                    <div style="font-weight:800; font-size:16px; color:#059669; margin-top:5px;">₹{row['Price']}</div>
                </div>
                <button class="add-btn">Book</button>
            </div>
            """, unsafe_allow_html=True)

    with tab_grocery:
        st.subheader("Fresh Produce & Grocery")
        g_items = df_catalog[df_catalog['Category'].isin(['Grocery & Staples', 'Fresh Produce & Dairy'])].sample(10)
        for _, row in g_items.iterrows():
            st.markdown(f"**{row['Item_Name']}** - ₹{row['Price']} (📍 {row['Location']})")

    with tab_services:
        st.subheader("Hire Professionals")
        s_items = df_catalog[df_catalog['Category'].isin(['Home Repairs & Maintenance', 'Freelance & IT Services', 'Heavy Machinery & Transport'])].sample(10)
        for _, row in s_items.iterrows():
            st.markdown(f"**{row['Item_Name']}** - ₹{row['Price']} (📍 {row['Location']})")

    with tab_jobs:
        st.subheader("Local Job Openings")
        jobs_df = df_catalog[df_catalog['Category'] == 'Local Jobs & Hiring'].sample(5)
        for _, row in jobs_df.iterrows():
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:12px; margin-bottom:15px; border: 1px solid #e5e7eb;">
                <div style="float:right; background:#dcfce7; color:#059669; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:bold;">Hiring</div>
                <div style="font-size: 16px; font-weight: 700; color: #111827;">{row['Item_Name']}</div>
                <div style="color: #059669; font-weight: 700; font-size: 14px; margin: 5px 0;">₹{row['Price']}/mo</div>
                <div style="font-size:13px; color:#6b7280;">📍 {row['Location']}</div>
            </div>
            """, unsafe_allow_html=True)
