import streamlit as st
import pandas as pd
import os
import random
import difflib
from datetime import datetime

# ==========================================
# 1. SETUP & SESSION STATE ISOLATION
# ==========================================
st.set_page_config(page_title="KuchhV | Super App", layout="centered", initial_sidebar_state="collapsed")

# Database Files
DB_CATALOG = "v14_catalog.csv"
DB_JOBS = "v14_jobs.csv"
DB_PARTNERS = "v14_partners.csv"
DB_ORDERS = "v14_orders.csv"
DB_JOB_APPS = "v14_job_apps.csv"

# Pan-India Locations & Tiers (For Dynamic Pricing)
LOCATIONS = {
    "Chatra": 0.7, "Hazaribagh": 0.8, "Ranchi": 0.9, "Patna": 0.9, 
    "Gaya": 0.8, "Kanpur": 0.9, "Delhi": 1.2, "Mumbai": 1.3, "Bangalore": 1.2
}

# Ensure Session States
if 'user_role' not in st.session_state:
    st.session_state.update({'user_role': 'Customer', 'logged_in': False, 'phone': '', 'name': '', 'city': 'Chatra'})

# ==========================================
# 2. MEGA DATABASE GENERATOR (10,000+ Items)
# ==========================================
@st.cache_data
def generate_pan_india_dbs():
    if not os.path.exists(DB_CATALOG):
        with st.spinner("🚀 Building Pan-India Geo-Locked Servers..."):
            catalog_data = []
            categories = {
                "10-Min Groceries": ["Aashirvaad Atta 5kg", "Amul Milk 1L", "Onion 1kg", "Potato 1kg", "Refined Oil 1L", "Tata Salt", "Sugar 1kg", "Paneer 200g"],
                "Home Services": ["Plumber Visit", "Electrician Visit", "AC Service", "RO Repair", "Deep Cleaning", "Carpenter"],
                "Heavy Machinery": ["Tractor Rental", "JCB Booking", "Tata Ace Booking", "Water Tanker"],
                "IT & CSC Work": ["GST Filing", "PAN Card Apply", "Pension Form", "Excel Data Entry", "Video Editing"]
            }
            
            # Generate 10,000+ Catalog Items
            for i in range(10100):
                cat = random.choice(list(categories.keys()))
                item = random.choice(categories[cat])
                loc = random.choice(list(LOCATIONS.keys()))
                base_price = random.randint(50, 1500)
                final_price = int(base_price * LOCATIONS[loc]) # Dynamic Pricing applied
                
                catalog_data.append({
                    "Item_ID": f"ITM{10000+i}", "Name": f"{item}", "Category": cat,
                    "Price": final_price, "Location": loc
                })
            pd.DataFrame(catalog_data).to_csv(DB_CATALOG, index=False)

            # Generate 500+ Local Jobs
            job_data = []
            job_titles = ["Delivery Partner", "Shop Assistant", "Data Entry Operator", "Cook (Home)", "Mechanic", "Security Guard"]
            for i in range(500):
                loc = random.choice(list(LOCATIONS.keys()))
                title = random.choice(job_titles)
                sal_base = random.randint(7000, 20000)
                sal_final = int(sal_base * LOCATIONS[loc])
                job_data.append({
                    "Job_ID": f"JOB{1000+i}", "Title": title, "Employer": f"Local Biz {random.randint(1,100)}",
                    "Salary": f"₹{sal_final}/month", "Location": loc
                })
            pd.DataFrame(job_data).to_csv(DB_JOBS, index=False)

generate_pan_india_dbs()

# Helpers
def load_db(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    return pd.read_csv(file, dtype=str)

def save_db(df, file):
    df.to_csv(file, index=False)

# Load Mutable DBs
db_partners = load_db(DB_PARTNERS, ["Phone", "Password", "Name", "Role", "Location", "Status"])
db_orders = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date"])
db_job_apps = load_db(DB_JOB_APPS, ["Job_ID", "Job_Title", "Candidate_Name", "Candidate_Phone", "Employer"])

# ==========================================
# 3. HYPER-SIMPLE MOBILE UI CSS
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Top Header */
    .top-header { background: white; padding: 15px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 999;}
    
    /* Beautiful Emerald Cards */
    .product-card { background: white; border-radius: 12px; padding: 15px; border: 1px solid #e2e8f0; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;}
    .job-card { background: #ffffff; border-left: 5px solid #10b981; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    
    .item-title { font-size: 16px; font-weight: 800; color: #0f172a;}
    .item-price { font-size: 18px; font-weight: 900; color: #10b981;}
    .loc-tag { font-size: 11px; background: #f1f5f9; color: #64748b; padding: 2px 6px; border-radius: 4px; font-weight: bold;}
    
    /* Fallback Box */
    .fallback-box { background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. UNIVERSAL TOP HEADER
# ==========================================
col_loc, col_role = st.columns([2, 1])
with col_loc:
    st.session_state['city'] = st.selectbox("📍 Set Location", list(LOCATIONS.keys()), index=list(LOCATIONS.keys()).index(st.session_state['city']))
with col_role:
    st.session_state['user_role'] = st.selectbox("👤 Switch Role", ["Customer", "Partner", "Admin"])

st.write("---")

# ==========================================
# 5. CUSTOMER INTERFACE (Extremely Simple)
# ==========================================
if st.session_state['user_role'] == "Customer":
    
    # 5.1 THE IDIOT-PROOF AI SEARCH BAR
    search_query = st.text_input("🔍 What do you need today?", placeholder="Try typing 'palambar', 'atta', 'tretar'...")
    
    catalog = pd.read_csv(DB_CATALOG, dtype=str)
    # Geo-Locking Data
    local_catalog = catalog[catalog['Location'] == st.session_state['city']]
    
    results = pd.DataFrame()
    if search_query:
        query = str(search_query).lower()
        exact = local_catalog[local_catalog['Name'].str.lower().str.contains(query)]
        if not exact.empty:
            results = exact
        else:
            # Fuzzy AI Correction
            all_names = local_catalog['Name'].unique().tolist()
            matches = difflib.get_close_matches(query, [str(n).lower() for n in all_names], n=5, cutoff=0.3)
            if matches:
                pattern = '|'.join(matches)
                results = local_catalog[local_catalog['Name'].str.lower().str.contains(pattern, regex=True)]

    # 5.2 RENDER SEARCH OR HOME TABS
    if search_query and not results.empty:
        st.success(f"✅ Showing results for your search in {st.session_state['city']}")
        for _, row in results.head(15).iterrows():
            st.markdown(f"""
            <div class="product-card">
                <div>
                    <div class="item-title">{row['Name']}</div>
                    <div class="loc-tag">{row['Category']}</div>
                </div>
                <div style="text-align: right;">
                    <div class="item-price">₹{row['Price']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Book Now"):
                with st.form(f"bk_{row['Item_ID']}"):
                    c_ph = st.text_input("Enter Mobile Number")
                    if st.form_submit_button("Confirm Order Securely"):
                        if c_ph:
                            new_ord = pd.DataFrame([{"Order_ID": f"ORD{random.randint(10000,99999)}", "Customer": c_ph, "Item": row['Name'], "Price": row['Price'], "Location": row['Location'], "Partner": "Unassigned", "Status": "Pending", "OTP": str(random.randint(1000,9999)), "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                            save_db(pd.concat([db_orders, new_ord]), DB_ORDERS)
                            st.success("🎉 Order Placed! Go to 'My Orders' for tracking.")

    elif search_query and results.empty:
        # ZERO DEAD ENDS: Custom Request Box
        st.markdown("""
        <div class="fallback-box">
            <h3 style="margin:0; color:white;">🎙️ Not found in catalog?</h3>
            <p style="margin:0; font-size:14px;">Tell us exactly what you need. Local partners will arrange it.</p>
        </div>
        """, unsafe_allow_html=True)
        with st.form("custom_req"):
            st.text_area("Your Requirement", value=search_query)
            st.text_input("Mobile Number")
            if st.form_submit_button("Send Request to Partners 🚀"):
                st.success("✅ Broadcasted to local verified partners!")

    else:
        # DEFAULT MOBILE NAVIGATION TABS
        t_home, t_jobs, t_orders = st.tabs(["🛒 Grocery & Services", "💼 Local Jobs", "📦 My Orders"])
        
        with t_home:
            st.subheader(f"⚡ 10-Min Delivery in {st.session_state['city']}")
            home_items = local_catalog.sample(10)
            for _, row in home_items.iterrows():
                st.markdown(f"""
                <div class="product-card">
                    <div><div class="item-title">{row['Name']}</div><div class="loc-tag">{row['Category']}</div></div>
                    <div class="item-price">₹{row['Price']}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Order"):
                    with st.form(f"h_{row['Item_ID']}"):
                        c_ph = st.text_input("Mobile Number")
                        if st.form_submit_button("Order Now"):
                            new_ord = pd.DataFrame([{"Order_ID": f"ORD{random.randint(10000,99999)}", "Customer": c_ph, "Item": row['Name'], "Price": row['Price'], "Location": row['Location'], "Partner": "Unassigned", "Status": "Pending", "OTP": str(random.randint(1000,9999)), "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                            save_db(pd.concat([db_orders, new_ord]), DB_ORDERS)
                            st.success("✅ Order Placed!")

        with t_jobs:
            st.subheader(f"💼 Hiring in {st.session_state['city']}")
            st.info("Direct monthly salary jobs. No OTP required to apply.")
            jobs = pd.read_csv(DB_JOBS, dtype=str)
            local_jobs = jobs[jobs['Location'] == st.session_state['city']].head(10)
            
            for _, row in local_jobs.iterrows():
                st.markdown(f"""
                <div class="job-card">
                    <div class="item-title">{row['Title']}</div>
                    <div style="color: gray; font-size:13px; margin: 4px 0;">🏢 {row['Employer']}</div>
                    <div class="item-price" style="color: #ea580c;">{row['Salary']}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Apply Now"):
                    with st.form(f"app_{row['Job_ID']}"):
                        a_name = st.text_input("Full Name")
                        a_ph = st.text_input("Mobile Number")
                        if st.form_submit_button("Send Application"):
                            if a_name and a_ph:
                                new_app = pd.DataFrame([{"Job_ID": row['Job_ID'], "Job_Title": row['Title'], "Candidate_Name": a_name, "Candidate_Phone": a_ph, "Employer": row['Employer']}])
                                save_db(pd.concat([db_job_apps, new_app]), DB_JOB_APPS)
                                st.success("✅ Application sent to employer!")

        with t_orders:
            my_phone = st.text_input("Enter Phone No. to track orders:")
            if my_phone:
                my_ords = db_orders[db_orders['Customer'] == my_phone]
                for _, row in my_ords.iterrows():
                    color = "#10b981" if row['Status'] == "Completed" else "#ea580c"
                    st.markdown(f"""
                    <div class="product-card" style="border-left: 5px solid {color};">
                        <div><div class="item-title">{row['Item']}</div><div class="loc-tag">{row['Status']}</div></div>
                        <div style="text-align: right;">
                            <div style="font-size:12px;">Secret OTP</div>
                            <div style="font-size: 18px; font-weight: 900; color:#dc2626;">{row['OTP']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ==========================================
# 6. PARTNER / DELIVERY PORTAL (Ecosystem A)
# ==========================================
elif st.session_state['user_role'] == "Partner":
    if not st.session_state['logged_in']:
        t_log, t_reg = st.tabs(["Login", "Register Business"])
        with t_reg:
            with st.form("p_reg"):
                p_ph = st.text_input("Mobile No.")
                p_pw = st.text_input("Create Password", type="password")
                p_name = st.text_input("Full Name / Business Name")
                if st.form_submit_button("Register"):
                    new_p = pd.DataFrame([{"Phone": p_ph, "Password": p_pw, "Name": p_name, "Role": "Partner", "Location": st.session_state['city'], "Status": "Verified"}])
                    save_db(pd.concat([db_partners, new_p]), DB_PARTNERS)
                    st.success("✅ Registered Successfully!")
        with t_log:
            l_ph = st.text_input("Mobile No. ")
            l_pw = st.text_input("Password ", type="password")
            if st.button("Login"):
                user = db_partners[(db_partners['Phone'] == l_ph) & (db_partners['Password'] == l_pw)]
                if not user.empty:
                    st.session_state.update({'logged_in': True, 'phone': l_ph, 'name': user.iloc[0]['Name'], 'city': user.iloc[0]['Location']})
                    st.rerun()
                else:
                    st.error("Invalid Login.")
    else:
        st.success(f"💼 Partner Panel: {st.session_state['name']} (📍 {st.session_state['city']})")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
            
        t_leads, t_active = st.tabs(["🔔 New Leads", "📦 Active Deliveries"])
        
        with t_leads:
            pending = db_orders[(db_orders['Location'] == st.session_state['city']) & (db_orders['Status'] == 'Pending')]
            st.write(f"Found {len(pending)} open orders in your area:")
            for idx, row in pending.iterrows():
                st.markdown(f"<div class='product-card'><div><b>{row['Item']}</b><br>Customer: {row['Customer']}</div><div>₹{row['Price']}</div></div>", unsafe_allow_html=True)
                if st.button(f"Accept Order {row['Order_ID']}"):
                    db_orders.at[idx, 'Partner'] = st.session_state['phone']
                    db_orders.at[idx, 'Status'] = 'Accepted'
                    save_db(db_orders, DB_ORDERS)
                    st.rerun()
                    
        with t_active:
            active = db_orders[(db_orders['Partner'] == st.session_state['phone']) & (db_orders['Status'] == 'Accepted')]
            for idx, row in active.iterrows():
                st.markdown(f"<div class='job-card'><b>Deliver:</b> {row['Item']}<br>Customer Phone: {row['Customer']}</div>", unsafe_allow_html=True)
                with st.form(f"otp_{row['Order_ID']}"):
                    otp_in = st.text_input("Ask Customer for 4-Digit OTP to Complete:")
                    if st.form_submit_button("Verify & Complete Order"):
                        if otp_in == row['OTP']:
                            db_orders.at[idx, 'Status'] = 'Completed'
                            save_db(db_orders, DB_ORDERS)
                            st.success("✅ Delivery Successful!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Wrong OTP entered.")

# ==========================================
# 7. SUPER ADMIN CENTER
# ==========================================
elif st.session_state['user_role'] == "Admin":
    st.title("⚙️ Master Admin Control Room")
    t1, t2, t3 = st.tabs(["📦 Track All Orders", "📋 Job Applications (Leads)", "👥 Partners"])
    
    with t1:
        st.subheader("Global Service & Delivery Orders")
        st.dataframe(db_orders, use_container_width=True)
    with t2:
        st.subheader("Job Applications (Ecosystem B)")
        st.info("These are direct candidates applying for monthly jobs. No OTPs required here.")
        st.dataframe(db_job_apps, use_container_width=True)
    with t3:
        st.subheader("Registered Partners (Ecosystem A)")
        st.dataframe(db_partners, use_container_width=True)
