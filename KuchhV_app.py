import streamlit as st
import pandas as pd
import os
import random
import difflib
from datetime import datetime

# ==========================================
# 1. SETUP & SESSION STATE
# ==========================================
st.set_page_config(
    page_title="KuchhV | Super App", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

DB_CATALOG = "v15_catalog.csv"
DB_JOBS = "v15_jobs.csv"
DB_PARTNERS = "v15_partners.csv"
DB_ORDERS = "v15_orders.csv"
DB_JOB_APPS = "v15_job_apps.csv"

LOCATIONS = {"Chatra": 1.0, "Hazaribagh": 1.0, "Ranchi": 1.1, "Delhi": 1.3}

if 'user_role' not in st.session_state:
    st.session_state.update({
        'user_role': 'Customer', 
        'logged_in': False, 
        'phone': '', 
        'name': '', 
        'city': 'Chatra'
    })

# ==========================================
# 2. REALISTIC DATABASE GENERATOR
# ==========================================
@st.cache_data
def generate_authentic_dbs():
    if not os.path.exists(DB_CATALOG):
        with st.spinner("🚀 Building Authentic Pan-India Database..."):
            catalog_data = []
            
            REAL_ITEMS = [
                {"Name": "Aashirvaad Shudh Chakki Atta 5kg", "Cat": "10-Min Groceries", "Base_Price": 220},
                {"Name": "Amul Taaza Toned Milk 1L", "Cat": "10-Min Groceries", "Base_Price": 68},
                {"Name": "Fortune Sunlite Refined Oil 1L", "Cat": "10-Min Groceries", "Base_Price": 135},
                {"Name": "Fresh Onion (Pyaz) 1kg", "Cat": "10-Min Groceries", "Base_Price": 35},
                {"Name": "Plumber Visit Charge", "Cat": "Home Services", "Base_Price": 149},
                {"Name": "Electrician Visit Charge", "Cat": "Home Services", "Base_Price": 129},
                {"Name": "AC Deep Cleaning Service", "Cat": "Home Services", "Base_Price": 499},
                {"Name": "Tata Ace (Chota Hathi) Booking", "Cat": "Heavy Machinery", "Base_Price": 800},
                {"Name": "Mahindra Tractor Rental", "Cat": "Heavy Machinery", "Base_Price": 1200},
                {"Name": "GST Registration (Complete)", "Cat": "IT & CSC Work", "Base_Price": 1499},
                {"Name": "Pension Form Application", "Cat": "IT & CSC Work", "Base_Price": 50},
            ]
            
            item_id_counter = 1000
            for loc, multiplier in LOCATIONS.items():
                for item in REAL_ITEMS:
                    final_price = int(item["Base_Price"] * multiplier)
                    catalog_data.append({
                        "Item_ID": f"ITM{item_id_counter}", "Name": item["Name"], "Category": item["Cat"],
                        "Price": final_price, "Location": loc
                    })
                    item_id_counter += 1
            pd.DataFrame(catalog_data).to_csv(DB_CATALOG, index=False)

            job_data = []
            REAL_EMPLOYERS = ["Sharma Ration Store", "KuchhV Logistics", "Gupta Kirana", "Verma Hardware", "TechNova Solutions"]
            REAL_JOBS = [
                {"Title": "Delivery Partner (Full Time)", "Base_Sal": 15000},
                {"Title": "Shop Assistant / Helper", "Base_Sal": 9000},
                {"Title": "Data Entry Operator", "Base_Sal": 12000},
                {"Title": "Two-Wheeler Mechanic", "Base_Sal": 14000}
            ]
            
            job_id_counter = 1000
            for loc, multiplier in LOCATIONS.items():
                for job in REAL_JOBS:
                    sal_final = int(job["Base_Sal"] * multiplier)
                    job_data.append({
                        "Job_ID": f"JOB{job_id_counter}", "Title": job["Title"], "Employer": random.choice(REAL_EMPLOYERS),
                        "Salary": f"₹{sal_final}/month", "Location": loc
                    })
                    job_id_counter += 1
            pd.DataFrame(job_data).to_csv(DB_JOBS, index=False)

generate_authentic_dbs()

def load_db(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)
    return pd.read_csv(file, dtype=str)

def save_db(df, file): 
    df.to_csv(file, index=False)

db_partners = load_db(DB_PARTNERS, ["Phone", "Password", "Name", "Role", "Location", "Status"])
db_orders = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date"])
db_job_apps = load_db(DB_JOB_APPS, ["Job_ID", "Job_Title", "Candidate_Name", "Candidate_Phone", "Employer"])

# ==========================================
# 3. HELPERS: STYLING & VALIDATION
# ==========================================
def is_valid_phone(phone_str):
    return len(phone_str) == 10 and phone_str.isdigit()

def get_category_color(cat):
    colors = {
        "10-Min Groceries": "#10b981",  # Emerald
        "Home Services": "#3b82f6",      # Blue
        "Heavy Machinery": "#f59e0b",   # Amber
        "IT & CSC Work": "#8b5cf6"       # Purple
    }
    return colors.get(cat, "#64748b")

def render_metric_card(title, value, description, bg_gradient):
    return f"""
    <div style="background: {bg_gradient}; padding: 20px; border-radius: 16px; color: white; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); margin-bottom: 15px;">
        <div style="font-size: 13px; opacity: 0.85; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">{title}</div>
        <div style="font-size: 32px; font-weight: 800; margin: 6px 0;">{value}</div>
        <div style="font-size: 12px; opacity: 0.75; font-weight: 400;">{description}</div>
    </div>
    """

# ==========================================
# 4. PREMIUM UI CSS OVERHAUL
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp { 
        background-color: #f8fafc; 
        font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif; 
    }
    #MainMenu, footer, header { visibility: hidden; }
    
    /* App Banner Header */
    .hero-banner {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        padding: 24px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.2);
    }
    
    /* Elegant Product Cards */
    .product-card { 
        background: white; 
        border-radius: 16px; 
        padding: 18px; 
        border: 1px solid #e2e8f0; 
        margin-bottom: 12px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.01); 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px -8px rgba(0,0,0,0.08);
        border-color: #cbd5e1;
    }
    
    /* Job Cards */
    .job-card { 
        background: #ffffff; 
        border-left: 6px solid #6366f1; 
        border-radius: 12px; 
        padding: 18px; 
        margin-bottom: 12px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s ease;
    }
    .job-card:hover {
        transform: translateY(-2px);
    }
    
    /* Typography Styles */
    .item-title { font-size: 16px; font-weight: 700; color: #0f172a; line-height: 1.4; }
    .item-price { font-size: 20px; font-weight: 800; color: #059669; text-align: right; }
    
    /* Custom Modern Badges */
    .cat-badge {
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 30px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .loc-tag { 
        font-size: 11px; 
        background: #f1f5f9; 
        color: #475569; 
        padding: 3px 10px; 
        border-radius: 30px; 
        font-weight: 600;
    }
    
    /* Fallback Box style */
    .fallback-box { 
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); 
        padding: 24px; 
        border-radius: 16px; 
        color: white; 
        margin-bottom: 20px;
        box-shadow: 0 10px 20px -5px rgba(29, 78, 216, 0.15);
    }
    
    /* Input Elements Adjustments */
    div Reinforce { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 5. TOP BRAND HEADER & ROUTER
# ==========================================
st.markdown("""
    <div class='hero-banner'>
        <h1 style='margin:0; font-size: 30px; font-weight:800; letter-spacing:-0.5px;'>KuchhV SuperApp</h1>
        <p style='margin:5px 0 0 0; opacity:0.9; font-size:14px; font-weight:500;'>Your instant gateway to hyper-local products, services & jobs.</p>
    </div>
""", unsafe_allow_html=True)

col_loc, col_role = st.columns([2, 1])
with col_loc:
    st.session_state['city'] = st.selectbox("📍 Current Active Market", list(LOCATIONS.keys()), index=list(LOCATIONS.keys()).index(st.session_state['city']))
with col_role:
    st.session_state['user_role'] = st.selectbox("👤 Ecosystem Space", ["Customer", "Partner", "Admin"])
st.write("---")

# ==========================================
# 6. CUSTOMER INTERFACE
# ==========================================
if st.session_state['user_role'] == "Customer":
    
    search_query = st.text_input("🔍 What can we help you find today?", placeholder="Try searching 'atta', 'plumber', 'tractor'...")
    
    local_catalog = pd.read_csv(DB_CATALOG, dtype=str)
    local_catalog = local_catalog[local_catalog['Location'] == st.session_state['city']]
    
    results = pd.DataFrame()
    if search_query:
        query = str(search_query).lower()
        exact = local_catalog[local_catalog['Name'].str.lower().str.contains(query)]
        if not exact.empty:
            results = exact
        else:
            all_names = local_catalog['Name'].unique().tolist()
            matches = difflib.get_close_matches(query, [str(n).lower() for n in all_names], n=3, cutoff=0.3)
            if matches:
                pattern = '|'.join(matches)
                results = local_catalog[local_catalog['Name'].str.lower().str.contains(pattern, regex=True)]

    # Search Results Mode
    if search_query and not results.empty:
        st.success(f"⚡ Found match configurations inside {st.session_state['city']}")
        for _, row in results.iterrows():
            cat_color = get_category_color(row['Category'])
            st.markdown(f"""
                <div class='product-card'>
                    <div>
                        <div class='item-title'>{row['Name']}</div>
                        <div style='display: flex; gap: 8px; margin-top: 8px;'>
                            <span class='cat-badge' style='background: {cat_color}20; color: {cat_color};'>{row['Category']}</span>
                            <span class='loc-tag'>✨ KuchhV Verified</span>
                        </div>
                    </div>
                    <div class='item-price'>₹{row['Price']}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("⚡ Secure Checkout"):
                with st.form(f"bk_{row['Item_ID']}"):
                    c_ph = st.text_input("10-Digit Mobile Number", max_chars=10)
                    if st.form_submit_button("Confirm Order Securely"):
                        if is_valid_phone(c_ph):
                            new_ord = pd.DataFrame([{"Order_ID": f"ORD{random.randint(10000,99999)}", "Customer": c_ph, "Item": row['Name'], "Price": row['Price'], "Location": row['Location'], "Partner": "Unassigned", "Status": "Pending", "OTP": str(random.randint(1000,9999)), "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                            save_db(pd.concat([db_orders, new_ord]), DB_ORDERS)
                            st.success("🎉 Order Registered successfully! Navigate to 'My Orders' to track dispatch status.")
                        else:
                            st.error("⚠️ Phone length constraint invalid. Enter a valid 10-digit number.")

    elif search_query and results.empty:
        st.markdown("<div class='fallback-box'><h3 style='margin:0; color:white;'>🎙️ Custom Concierge Request</h3><p style='margin:4px 0 0 0; font-size:14px; opacity:0.95;'>We couldn't match this exact item in our catalogs, but our local partner pool can arrange it immediately!</p></div>", unsafe_allow_html=True)
        with st.form("custom_req"):
            st.text_area("Specify requirements cleanly (Size, Quantity, Urgency)", value=search_query)
            c_ph = st.text_input("10-Digit Contact Mobile", max_chars=10)
            if st.form_submit_button("Broadcast Request to On-Field Partners 🚀"):
                if is_valid_phone(c_ph):
                    st.success("✅ Broadcasted to local verified partners matching your marketplace area!")
                else:
                    st.error("⚠️ Invalid contact formatting configuration.")

    # Browse/Standard Discovery Mode
    else:
        t_home, t_jobs, t_orders = st.tabs(["🛒 Marketplace & Hub", "💼 Hyper-Local Jobs", "📦 Order Center"])
        
        with t_home:
            st.subheader(f"⚡ Available Ecosystem Options inside {st.session_state['city']}")
            for _, row in local_catalog.iterrows():
                cat_color = get_category_color(row['Category'])
                st.markdown(f"""
                    <div class='product-card'>
                        <div>
                            <div class='item-title'>{row['Name']}</div>
                            <div style='display: flex; gap: 8px; margin-top: 8px;'>
                                <span class='cat-badge' style='background: {cat_color}20; color: {cat_color};'>{row['Category']}</span>
                                <span class='loc-tag'>Assured Partner Fulfillment</span>
                            </div>
                        </div>
                        <div class='item-price'>₹{row['Price']}</div>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("Configure Instant Booking"):
                    with st.form(f"h_{row['Item_ID']}"):
                        c_ph = st.text_input("10-Digit Mobile Number", max_chars=10)
                        if st.form_submit_button("Place Instant Fulfillment Order"):
                            if is_valid_phone(c_ph):
                                new_ord = pd.DataFrame([{"Order_ID": f"ORD{random.randint(10000,99999)}", "Customer": c_ph, "Item": row['Name'], "Price": row['Price'], "Location": row['Location'], "Partner": "Unassigned", "Status": "Pending", "OTP": str(random.randint(1000,9999)), "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                                save_db(pd.concat([db_orders, new_ord]), DB_ORDERS)
                                st.success("✅ Dispatch sequence initiated successfully!")
                            else:
                                st.error("⚠️ Please verify mobile specifications.")

        with t_jobs:
            st.subheader(f"💼 verified Job Openings: {st.session_state['city']}")
            jobs = pd.read_csv(DB_JOBS, dtype=str)
            local_jobs = jobs[jobs['Location'] == st.session_state['city']]
            for _, row in local_jobs.iterrows():
                st.markdown(f"""
                    <div class='job-card'>
                        <div>
                            <div class='item-title'>{row['Title']}</div>
                            <div style='color: #64748b; font-size:13px; margin: 4px 0; font-weight:500;'>🏢 Employer: {row['Employer']}</div>
                            <span class='loc-tag' style='background:#eef2ff; color:#4f46e5;'>📍 {row['Location']} Base</span>
                        </div>
                        <div class='item-price' style='color: #4f46e5;'>{row['Salary']}</div>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("Apply in One-Click"):
                    with st.form(f"app_{row['Job_ID']}"):
                        a_name = st.text_input("Full Applicant Name")
                        a_ph = st.text_input("10-Digit Mobile Number", max_chars=10)
                        if st.form_submit_button("Transmit Verified Profile"):
                            if a_name and is_valid_phone(a_ph):
                                new_app = pd.DataFrame([{"Job_ID": row['Job_ID'], "Job_Title": row['Title'], "Candidate_Name": a_name, "Candidate_Phone": a_ph, "Employer": row['Employer']}])
                                save_db(pd.concat([db_job_apps, new_app]), DB_JOB_APPS)
                                st.success("✅ Recruiter workspace telemetry sent! They will dial you shortly.")
                            else:
                                st.error("⚠️ Core constraints error: Check structural values entered.")

        with t_orders:
            st.subheader("📦 Real-Time Order Telemetry Tracker")
            my_phone = st.text_input("Provide registered mobile number to request status:", max_chars=10)
            if is_valid_phone(my_phone):
                my_ords = db_orders[db_orders['Customer'] == my_phone]
                if my_ords.empty:
                    st.info("No active operations tracked under this entry line.")
                for _, row in my_ords.iterrows():
                    color = "#10b981" if row['Status'] == "Completed" else ("#ef4444" if row['Status'] == "Pending" else "#3b82f6")
                    st.markdown(f"""
                        <div class='product-card' style='border-left: 6px solid {color};'>
                            <div>
                                <div class='item-title'>{row['Item']}</div>
                                <span class='cat-badge' style='background: {color}15; color: {color}; margin-top: 4px; display:inline-block;'>{row['Status']}</span>
                            </div>
                            <div style='text-align: right;'>
                                <div style='font-size:11px; color:#64748b; font-weight:600;'>DELIVERY VERIFICATION OTP</div>
                                <div style='font-size: 20px; font-weight: 900; color:#4f46e5;'>{row['OTP']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# ==========================================
# 7. PARTNER PORTAL
# ==========================================
elif st.session_state['user_role'] == "Partner":
    if not st.session_state['logged_in']:
        t_log, t_reg = st.tabs(["🔑 Access Dashboard", "🤝 Register Fleet/Business"])
        with t_reg:
            with st.form("p_reg"):
                p_ph = st.text_input("10-Digit Mobile No.", max_chars=10)
                p_pw = st.text_input("Secure Entry Password", type="password")
                p_name = st.text_input("Full Merchant / Driver Name")
                if st.form_submit_button("Finalize Verification Enrollment"):
                    if is_valid_phone(p_ph):
                        new_p = pd.DataFrame([{"Phone": p_ph, "Password": p_pw, "Name": p_name, "Role": "Partner", "Location": st.session_state['city'], "Status": "Verified"}])
                        save_db(pd.concat([db_partners, new_p]), DB_PARTNERS)
                        st.success("✅ System node entry created successfully! Switch over to login tab.")
                    else:
                        st.error("⚠️ Configuration logic criteria failed.")
        with t_log:
            l_ph = st.text_input("Registered Phone ID", max_chars=10)
            l_pw = st.text_input("Merchant Password", type="password")
            if st.button("Authenticate Identity Securely"):
                user = db_partners[(db_partners['Phone'] == l_ph) & (db_partners['Password'] == l_pw)]
                if not user.empty:
                    st.session_state.update({'logged_in': True, 'phone': l_ph, 'name': user.iloc[0]['Name'], 'city': user.iloc[0]['Location']})
                    st.rerun()
                else:
                    st.error("Credential database match failure.")
    else:
        # Styled Partner Profile Header
        st.markdown(f"""
            <div style='background:#ffffff; border:1px solid #e2e8f0; padding:18px; border-radius:16px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <div style='font-size:13px; color:#64748b; font-weight:600;'>ON-FIELD LOGGED AGENT</div>
                    <div style='font-size:18px; font-weight:800; color:#0f172a;'>{st.session_state['name']}</div>
                    <div style='margin-top:4px;'><span class='loc-tag'>📍 {st.session_state['city']} Hub Node</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Disconnect Session 🔓"):
            st.session_state['logged_in'] = False
            st.rerun()
            
        t_leads, t_active = st.tabs(["🔔 Open Marketplace Request Leads", "📦 In-Flight Active Deliveries"])
        
        with t_leads:
            pending = db_orders[(db_orders['Location'] == st.session_state['city']) & (db_orders['Status'] == 'Pending')]
            
            # Quick metric view
            st.markdown(render_metric_card("Available Leads Pool", f"{len(pending)} Tasks", "Open for instant acceptance in your city", "linear-gradient(135deg, #059669 0%, #10b981 100%)"), unsafe_allow_html=True)
            
            for idx, row in pending.iterrows():
                st.markdown(f"""
                    <div class='product-card'>
                        <div>
                            <div class='item-title' style='color:#4f46e5;'>{row['Item']}</div>
                            <div style='font-size:13px; margin-top:4px; color:#475569;'><b>User Entry:</b> {row['Customer']}</div>
                        </div>
                        <div class='item-price'>₹{row['Price']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Accept Assignment {row['Order_ID']}", key=f"btn_{row['Order_ID']}"):
                    db_orders.at[idx, 'Partner'] = st.session_state['phone']
                    db_orders.at[idx, 'Status'] = 'Accepted'
                    save_db(db_orders, DB_ORDERS)
                    st.rerun()
                    
        with t_active:
            active = db_orders[(db_orders['Partner'] == st.session_state['phone']) & (db_orders['Status'] == 'Accepted')]
            st.write(f"In-Flight Container Count: **{len(active)} active item runs**")
            for idx, row in active.iterrows():
                st.markdown(f"""
                    <div class='job-card' style='border-left-color: #3b82f6;'>
                        <div>
                            <div class='item-title'>{row['Item']}</div>
                            <div style='font-size:13px; color:#475569;'>Fulfillment Contact: <b>{row['Customer']}</b></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                with st.form(f"otp_{row['Order_ID']}"):
                    otp_in = st.text_input("Enter secure validation code from customer profile:", placeholder="4-Digit Code")
                    if st.form_submit_button("Verify & Execute System Release"):
                        if otp_in == row['OTP']:
                            db_orders.at[idx, 'Status'] = 'Completed'
                            save_db(db_orders, DB_ORDERS)
                            st.success("✅ Node transaction complete! Escrow token payload cleared.")
                            st.rerun()
                        else:
                            st.error("Verification mismatch check rejected.")

# ==========================================
# 8. SUPER ADMIN CENTER
# ==========================================
elif st.session_state['user_role'] == "Admin":
    st.title("⚙️ Operations Control Center")
    
    # Global System Metrics Panel
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(render_metric_card("Total Hub Volume", f"{len(db_orders)} Units", "Gross overall order inputs", "linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)"), unsafe_allow_html=True)
    with m2:
        st.markdown(render_metric_card("Active Pipeline", f"{len(db_job_apps)} Profiles", "Total job application logs", "linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%)"), unsafe_allow_html=True)
    with m3:
        st.markdown(render_metric_card("Fleet Capacity", f"{len(db_partners)} Nodes", "Verified on-field businesses", "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"), unsafe_allow_html=True)
        
    t1, t2, t3 = st.tabs(["📦 Operational Ledgers", "📋 Candidate Streams", "👥 Merchant Clusters"])
    
    with t1:
        st.subheader("Global Service & Delivery Orders Ledger")
        st.dataframe(db_orders, use_container_width=True)
    with t2:
        st.subheader("Job Applications Stream Matrix")
        st.dataframe(db_job_apps, use_container_width=True)
    with t3:
        st.subheader("Ecosystem Partner Node Cluster Registry")
        st.dataframe(db_partners, use_container_width=True)
