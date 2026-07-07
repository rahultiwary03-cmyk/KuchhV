import streamlit as st
import pandas as pd
import os
import random
import difflib
from datetime import datetime

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="KuchhV | Har Zarurat, Ek Platform", layout="wide", page_icon="🚀")

# Database Files
CATALOG_FILE = "kuchhv_mega_catalog.csv"
PARTNERS_FILE = "kuchhv_partners.csv"
ORDERS_FILE = "kuchhv_orders.csv"
REQ_FILE = "kuchhv_requirements.csv"

# ==========================================
# 2. MEGA DATABASE GENERATOR (10,000+ Items)
# ==========================================
@st.cache_data
def load_or_generate_mega_catalog():
    if os.path.exists(CATALOG_FILE):
        return pd.read_csv(CATALOG_FILE, dtype=str)
    
    with st.spinner("🚀 Generating Pan-India Mega Database (10,000+ Items)... Please wait."):
        categories = {
            "Grocery & Staples": ["Aashirvaad Atta", "Fortune Oil", "Basmati Rice", "Toor Dal", "Tata Salt", "Sugar", "Spices", "Dry Fruits"],
            "Fresh Produce": ["Onion", "Potato", "Tomato", "Apple", "Banana", "Milk 1L", "Paneer", "Curd"],
            "Home Services": ["Plumber Visit", "Electrician Visit", "AC Repair & Gas Fill", "Washing Machine Repair", "RO Repair", "Deep Cleaning"],
            "IT & Freelance": ["Excel Data Entry", "Python Developer", "Website Design", "Logo Design", "Video Editing", "GST Filing"],
            "Local Jobs": ["Delivery Boy", "Shop Assistant", "Data Entry Operator", "Cook (Home)", "Mechanic", "Security Guard"],
            "Rentals & Heavy": ["Tractor Rental", "JCB Booking", "Tata Ace Booking", "Concrete Mixer", "Water Tanker", "Bike Taxi"],
            "Fashion & Lifestyle": ["Cotton T-Shirt", "Jeans", "Formal Shirt", "Sneakers", "Watch", "Sunglass"],
            "Events & Medical": ["Tent House", "Halwai", "Pandit Ji", "Bridal Makeup", "Lab Test at Home", "Medicine Delivery"]
        }
        districts = ["Chatra", "Ranchi", "Patna", "Gaya", "Hazaribagh", "Delhi", "Pune", "Pan-India"]
        brands = ["Premium", "Standard", "Local", "Verified", "Express"]
        
        data = []
        for i in range(10100):
            cat = random.choice(list(categories.keys()))
            item = random.choice(categories[cat])
            district = random.choice(districts)
            brand = random.choice(brands)
            
            if cat == "Local Jobs":
                item_name = f"{item} ({brand} Firm)"
                price = str(random.randint(8000, 25000))
                color = "10b981" # Green
            elif cat in ["Home Services", "IT & Freelance"]:
                item_name = f"{item} - {brand} Professional"
                price = str(random.randint(199, 2999))
                color = "3b82f6" # Blue
            else:
                item_name = f"{brand} {item}"
                price = str(random.randint(40, 1500))
                color = "f59e0b" # Orange
                
            img_text = item.replace(" ", "+")
            img_url = f"https://placehold.co/400x300/{color}/ffffff?text={img_text}"
            
            data.append({
                "ID": f"KV{10000+i}", "Item_Name": item_name, "Category": cat, 
                "Price": price, "Location": district, "Image_URL": img_url
            })
            
        df = pd.DataFrame(data)
        df.to_csv(CATALOG_FILE, index=False)
        return df

mega_catalog = load_or_generate_mega_catalog()

# Helper file loaders
def init_file(filename, cols):
    if not os.path.exists(filename):
        pd.DataFrame(columns=cols).to_csv(filename, index=False)

init_file(PARTNERS_FILE, ["Phone", "Password", "Business_Name", "Category", "Verification_Status"])
init_file(ORDERS_FILE, ["Timestamp", "Customer_Phone", "Item_Name", "Price", "Partner_Assigned", "Status"])
init_file(REQ_FILE, ["Timestamp", "Phone", "Requirement", "Location", "Status"])

# ==========================================
# 3. ENTERPRISE UI/UX CSS
# ==========================================
st.markdown("""
    <style>
    /* Hide Default Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #f1f5f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Professional Blue Sidebar */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e3a8a 0%, #2563eb 100%); border-right: 1px solid #1e40af;}
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    
    /* Product Cards with Hover Physics */
    .product-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); margin-bottom: 20px;}
    .product-card:hover { transform: translateY(-6px); box-shadow: 0 15px 25px -5px rgba(59, 130, 246, 0.15); border-color: #93c5fd; }
    .card-img { width: 100%; height: 160px; object-fit: cover; }
    .card-content { padding: 15px; }
    .card-title { font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
    .card-cat { font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 10px;}
    .card-price { font-size: 20px; font-weight: 800; color: #059669; }
    
    /* Smart Empty State Box */
    .empty-state-box { background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); padding: 25px; border-radius: 16px; color: white; text-align: center; box-shadow: 0 10px 15px -3px rgba(234, 88, 12, 0.3); margin-bottom: 30px;}
    </style>
""", unsafe_allow_html=True)

if 'logged_in_partner' not in st.session_state:
    st.session_state['logged_in_partner'] = None

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🚀 KuchhV Super App")
st.sidebar.caption("Har Zarurat, Ek Platform.")
st.sidebar.write("---")
menu = st.sidebar.radio("Navigation:", ["🏠 Mega Marketplace", "📢 Requirement Hub", "💼 Partner Portal", "⚙️ Super Admin Center"])
st.sidebar.write("---")
st.sidebar.info("🎧 24/7 Support\n\n📞 8521413089\n\n✉️ Rahultiwary03@gmail.com")

# ==========================================
# 5. AI MARKETPLACE ENGINE
# ==========================================
if menu == "🏠 Mega Marketplace":
    st.title("🛍️ Explore 10,000+ Products & Services")
    
    search_query = st.text_input("🔍 What are you looking for today?", placeholder="Try typing 'plambar', 'tretar', 'atta', 'job'...")
    
    results = pd.DataFrame()
    
    if search_query:
        query = str(search_query).lower().strip()
        # 1. Exact/Substring Match
        exact = mega_catalog[mega_catalog['Item_Name'].str.lower().str.contains(query) | mega_catalog['Category'].str.lower().str.contains(query)]
        if not exact.empty:
            results = exact
        else:
            # 2. AI Fuzzy Logic (Typo Corrector)
            all_words = set(" ".join(mega_catalog['Item_Name'].str.lower().tolist()).split())
            close_matches = difflib.get_close_matches(query, all_words, n=3, cutoff=0.4)
            if close_matches:
                pattern = '|'.join(close_matches)
                results = mega_catalog[mega_catalog['Item_Name'].str.lower().str.contains(pattern, regex=True)]
    else:
        results = mega_catalog.sample(12) # Default Home Screen

    # Render Results or Smart Empty State
    if not results.empty:
        if search_query:
            st.success(f"✅ Found {len(results)} matches for '{search_query}'")
        
        cols = st.columns(4)
        for i, (_, row) in enumerate(results.head(20).iterrows()):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="{row['Image_URL']}" class="card-img">
                    <div class="card-content">
                        <div class="card-cat">📍 {row['Location']} • {row['Category'].split('&')[0]}</div>
                        <div class="card-title">{row['Item_Name']}</div>
                        <div class="card-price">₹{row['Price']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander(f"⚡ Book {row['Item_Name'][:10]}..."):
                    with st.form(f"form_{row['ID']}"):
                        phone = st.text_input("Mobile No.")
                        if st.form_submit_button("Confirm Order"):
                            if phone:
                                new_order = pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "Customer_Phone": phone, "Item_Name": row['Item_Name'], "Price": row['Price'], "Partner_Assigned": "Unassigned", "Status": "Pending"}])
                                new_order.to_csv(ORDERS_FILE, mode='a', header=False, index=False)
                                st.success("✅ Order Placed! Admin will assign a partner.")
                            else:
                                st.error("Enter phone number.")
    else:
        # SMART EMPTY STATE (Zero Dead Ends)
        st.markdown("""
        <div class="empty-state-box">
            <h2 style='color: white; margin-top: 0;'>🎙️ Not found? We'll arrange it!</h2>
            <p style='font-size: 16px;'>Post your custom requirement below. Our local partners will bid and fulfill your exact need.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("custom_order_form"):
            st.write("### Post to Requirement Hub")
            c_phone = st.text_input("Your Mobile Number")
            c_req = st.text_area("What do you need?", value=search_query)
            c_loc = st.text_input("Pincode / Location")
            if st.form_submit_button("Broadcast to Local Partners 🚀"):
                if c_phone and c_req:
                    pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "Phone": c_phone, "Requirement": c_req, "Location": c_loc, "Status": "Open"}]).to_csv(REQ_FILE, mode='a', header=False, index=False)
                    st.success("✅ Broadcasted Successfully!")

# ==========================================
# 6. REQUIREMENT HUB
# ==========================================
elif menu == "📢 Requirement Hub":
    st.title("📢 Custom Requirement Hub")
    st.info("Public requests broadcasted by customers for custom jobs, bulk orders, or missing items.")
    req_df = pd.read_csv(REQ_FILE, dtype=str)
    if not req_df.empty:
        st.dataframe(req_df[::-1], use_container_width=True)
    else:
        st.write("No open requirements right now.")

# ==========================================
# 7. PARTNER PORTAL (Secure Auth)
# ==========================================
elif menu == "💼 Partner Portal":
    st.title("💼 Partner Business Portal")
    
    if st.session_state['logged_in_partner'] is None:
        t1, t2 = st.tabs(["🔐 Secure Login", "📝 Join Network"])
        
        with t2:
            st.markdown("### Register your business (1% Platform Fee Only)")
            with st.form("partner_reg"):
                biz = st.text_input("Business / Name")
                ph = st.text_input("Mobile Number")
                pw = st.text_input("Create Password", type="password")
                cat = st.selectbox("Primary Category", mega_catalog['Category'].unique())
                if st.form_submit_button("Submit for KYC"):
                    pdf = pd.read_csv(PARTNERS_FILE, dtype=str)
                    if ph in pdf['Phone'].values:
                        st.error("Number already registered.")
                    else:
                        pd.DataFrame([{"Phone": ph, "Password": pw, "Business_Name": biz, "Category": cat, "Verification_Status": "Pending"}]).to_csv(PARTNERS_FILE, mode='a', header=False, index=False)
                        st.success("✅ Application sent! Awaiting Admin Approval.")
        
        with t1:
            st.markdown("### Login to Dashboard")
            l_ph = st.text_input("Registered Mobile Number ")
            l_pw = st.text_input("Password ", type="password")
            if st.button("Login"):
                pdf = pd.read_csv(PARTNERS_FILE, dtype=str)
                user = pdf[(pdf['Phone'] == l_ph) & (pdf['Password'] == l_pw)]
                if not user.empty:
                    if user.iloc[0]['Verification_Status'] == 'Verified ✅':
                        st.session_state['logged_in_partner'] = user.iloc[0]['Business_Name']
                        st.rerun()
                    else:
                        st.error("Account approval pending by Admin.")
                else:
                    st.error("Invalid credentials.")
    else:
        st.success(f"👋 Welcome back, {st.session_state['logged_in_partner']}!")
        if st.button("Logout"):
            st.session_state['logged_in_partner'] = None
            st.rerun()
        
        st.subheader("📦 Orders Assigned to You")
        odf = pd.read_csv(ORDERS_FILE, dtype=str)
        my_orders = odf[odf['Partner_Assigned'] == st.session_state['logged_in_partner']]
        st.dataframe(my_orders, use_container_width=True)

# ==========================================
# 8. SUPER ADMIN CENTER
# ==========================================
elif menu == "⚙️ Super Admin Center":
    st.title("⚙️ Super Admin Control Room")
    st.markdown("Manage millions of items, approve partners, and route orders dynamically.")
    
    t_orders, t_partners, t_catalog = st.tabs(["🛒 Manage Orders", "👥 Approve Partners", "📸 Mega Catalog"])
    
    with t_orders:
        st.subheader("Order Routing Engine")
        odf = pd.read_csv(ORDERS_FILE, dtype=str)
        unassigned = odf[odf['Partner_Assigned'] == 'Unassigned']
        if not unassigned.empty:
            st.error(f"🚨 ALERT: {len(unassigned)} Order(s) need partner assignment!")
        
        edited_odf = st.data_editor(odf, num_rows="dynamic", use_container_width=True, key="admin_orders")
        if st.button("💾 Save Order Updates"):
            edited_odf.to_csv(ORDERS_FILE, index=False)
            st.success("Orders saved successfully.")
            
    with t_partners:
        st.subheader("Partner KYC Verification")
        pdf = pd.read_csv(PARTNERS_FILE, dtype=str)
        edited_pdf = st.data_editor(
            pdf, num_rows="dynamic", use_container_width=True, key="admin_partners",
            column_config={"Verification_Status": st.column_config.SelectboxColumn("Status", options=["Pending", "Verified ✅", "Rejected ❌"])}
        )
        if st.button("💾 Save Partner Status"):
            edited_pdf.to_csv(PARTNERS_FILE, index=False)
            st.success("Partner database updated.")
            
    with t_catalog:
        st.subheader("10,000+ Item Catalog Editor")
        st.warning("⚠️ Warning: Modifying large datasets here. Search by column to edit specific items.")
        st.dataframe(mega_catalog, use_container_width=True) # Read-only for 10k items to prevent browser crash, editing 10k rows in st.data_editor causes UI lag.
