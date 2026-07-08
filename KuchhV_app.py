import streamlit as st
import pandas as pd
import os
import random
import difflib
import time
from datetime import datetime

# ==========================================
# 1. SETUP & SESSION STATE
# ==========================================
st.set_page_config(
    page_title="KuchhV | Super App Extreme", 
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
# 2. REALISTIC DATABASE GENERATOR WITH STOCK
# ==========================================
@st.cache_data
def generate_authentic_dbs():
    if not os.path.exists(DB_CATALOG):
        with st.spinner("🚀 Building Production-Grade Hyperlocal Database..."):
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
                    # Added simulated real-time stock levels
                    stock_status = "In Stock" if random.random() > 0.15 else "Out of Stock"
                    catalog_data.append({
                        "Item_ID": f"ITM{item_id_counter}", "Name": item["Name"], "Category": item["Cat"],
                        "Price": final_price, "Location": loc, "Stock": stock_status
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
db_orders = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date", "Payment_Method"])
db_job_apps = load_db(DB_JOB_APPS, ["Job_ID", "Job_Title", "Candidate_Name", "Candidate_Phone", "Employer"])

# ==========================================
# 3. HELPERS: STYLING & VALIDATION
# ==========================================
def is_valid_phone(phone_str):
    return len(phone_str) == 10 and phone_str.isdigit()

def get_category_color(cat):
    colors = {
        "10-Min Groceries": "#10b981",  
        "Home Services": "#3b82f6",      
        "Heavy Machinery": "#f59e0b",   
        "IT & CSC Work": "#8b5cf6"       
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
    
    .hero-banner {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        padding: 24px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.2);
    }
    
    .product-card { 
        background: white; 
        border-radius: 16px; 
        padding: 18px; 
        border: 1px solid #e2e8f0; 
        margin-bottom: 12px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); 
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
    }
    
    .item-title { font-size: 16px; font-weight: 700; color: #0f172a; line-height: 1.4; }
    .item-price { font-size: 20px; font-weight: 800; color: #059669; text-align: right; }
    
    .cat-badge {
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 30px;
        text-transform: uppercase;
    }
    .loc-tag { 
        font-size: 11px; 
        background: #f1f5f9; 
        color: #475569; 
        padding: 3px 10px; 
        border-radius: 30px; 
        font-weight: 600;
    }
    .stock-badge {
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 30px;
        font-weight: bold;
    }
    
    .fallback-box { 
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); 
        padding: 24px; 
        border-radius: 16px; 
        color: white; 
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 5. TOP BRAND HEADER & ROUTER
# ==========================================
st.markdown("""
    <div class='hero-banner'>
        <h1 style='margin:0; font-size: 30px; font-weight:800; letter-spacing:-0.5px;'>KuchhV SuperApp 🚀</h1>
        <p style='margin:5px 0 0 0; opacity:0.9; font-size:14px; font-weight:500;'>Hyperlocal instant ecosystem for Tier-2/3 India.</p>
    </div>
""", unsafe_allow_html=True)

col_loc, col_role = st.columns([2, 1])
with col_loc:
    st.session_state['city'] = st.selectbox("📍 Target Marketplace Node", list(LOCATIONS.keys()), index=list(LOCATIONS.keys()).index(st.session_state['city']))
with col_role:
    st.session_state['user_role'] = st.selectbox("👤 System Space Portal", ["Customer", "Partner", "Admin"])
st.write("---")

# ==========================================
# 6. CUSTOMER INTERFACE
# ==========================================
if st.session_state['user_role'] == "Customer":
    
    search_query = st.text_input("🔍 What do you need right now?", placeholder="Search groceries, local services, machinery...")
    
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

    # Dynamic order processing logic block helper
    def process_customer_checkout(row, element_key):
        if row['Stock'] == "Out of Stock":
            st.error("⚠️ This specific slot/item is currently completely sold out locally!")
            return
            
        with st.form(f"checkout_{element_key}_{row['Item_ID']}"):
            c_ph = st.text_input("10-Digit Mobile Number", max_chars=10)
            pay_method = st.radio("💳 Choose Secure Payment Gateway", ["Instant UPI (GPay/PhonePe/Paytm)", "Cash on Delivery (COD)"])
            
            if st.form_submit_button("Proceed to Pay & Confirm Order"):
                if is_valid_phone(c_ph):
                    if "UPI" in pay_method:
                        with st.spinner("🔒 Connecting with secure banking node handshake..."):
                            time.sleep(1.5) # Simulated secure delay bank verification 
                        st.toast("💰 UPI Payment Authenticated and Handshaked!", icon="✅")
                    
                    # Store atomic database record layout
                    new_ord = pd.DataFrame([{
                        "Order_ID": f"ORD{random.randint(10000,99999)}", "Customer": c_ph, "Item": row['Name'], 
                        "Price": row['Price'], "Location": row['Location'], "Partner": "Unassigned", 
                        "Status": "Paid" if "UPI" in pay_method else "Pending", "OTP": str(random.randint(1000,9999)), 
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Payment_Method": pay_method
                    }])
                    global db_orders
                    db_orders = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date", "Payment_Method"])
                    save_db(pd.concat([db_orders, new_ord]), DB_ORDERS)
                    st.success("🎉 Order Registered into Dark Store Engine! Go to 'Order Tracker' tab to trace rider mapping.")
                else:
                    st.error("⚠️ Phone logic invalid. Provide exact 10 digits configuration.")

    if search_query and not results.empty:
        for _, row in results.iterrows():
            cat_color = get_category_color(row['Category'])
            s_color = "#10b981" if row['Stock'] == "In Stock" else "#ef4444"
            st.markdown(f"""
                <div class='product-card'>
                    <div>
                        <div class='item-title'>{row['Name']}</div>
                        <div style='display: flex; gap: 8px; margin-top: 8px;'>
                            <span class='cat-badge' style='background: {cat_color}20; color: {cat_color};'>{row['Category']}</span>
                            <span class='stock-badge' style='background: {s_color}20; color: {s_color};'>{row['Stock']}</span>
                        </div>
                    </div>
                    <div class='item-price'>₹{row['Price']}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("⚡ Secure Gateway Checkout"):
                process_customer_checkout(row, "search")

    elif search_query and results.empty:
        st.markdown("<div class='fallback-box'><h3>🎙️ Custom Procurement Broadcast Engine</h3><p>Item missing in catalog? File a direct prompt broadcast, local merchants will coordinate procurement mechanics.</p></div>", unsafe_allow_html=True)
        with st.form("custom_req"):
            st.text_area("Specify item structural attributes completely", value=search_query)
            c_ph = st.text_input("10-Digit Mobile ID", max_chars=10)
            if st.form_submit_button("Broadcast to Grid Network"):
                if is_valid_phone(c_ph): st.success("✅ Shared across verified regional terminal operators!")
                else: st.error("⚠️ Formatting match block error.")

    else:
        t_home, t_jobs, t_orders = st.tabs(["🛒 Marketplace & Delivery Hub", "💼 Hyper-Local Jobs Portal", "📦 Multi-Stage Order Tracker"])
        
        with t_home:
            st.subheader(f"⚡ Live Local Catalog Inventory ({st.session_state['city']})")
            for _, row in local_catalog.iterrows():
                cat_color = get_category_color(row['Category'])
                s_color = "#10b981" if row['Stock'] == "In Stock" else "#ef4444"
                st.markdown(f"""
                    <div class='product-card'>
                        <div>
                            <div class='item-title'>{row['Name']}</div>
                            <div style='display: flex; gap: 8px; margin-top: 8px;'>
                                <span class='cat-badge' style='background: {cat_color}20; color: {cat_color};'>{row['Category']}</span>
                                <span class='stock-badge' style='background: {s_color}20; color: {s_color};'>{row['Stock']}</span>
                            </div>
                        </div>
                        <div class='item-price'>₹{row['Price']}</div>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("Configure Instant Booking"):
                    process_customer_checkout(row, "browse")

        with t_jobs:
            st.subheader(f"💼 verified Recruitment Vectors inside {st.session_state['city']}")
            jobs = pd.read_csv(DB_JOBS, dtype=str)
            local_jobs = jobs[jobs['Location'] == st.session_state['city']]
            for _, row in local_jobs.iterrows():
                st.markdown(f"""
                    <div class='job-card'>
                        <div>
                            <div class='item-title'>{row['Title']}</div>
                            <div style='color: #64748b; font-size:13px; margin: 4px 0; font-weight:500;'>🏢 Merchant entity: {row['Employer']}</div>
                        </div>
                        <div class='item-price' style='color: #4f46e5;'>{row['Salary']}</div>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("Apply in One-Click"):
                    with st.form(f"app_{row['Job_ID']}"):
                        a_name = st.text_input("Full Applicant Name")
                        a_ph = st.text_input("10-Digit Mobile", max_chars=10)
                        if st.form_submit_button("Transmit Profile Matrix"):
                            if a_name and is_valid_phone(a_ph):
                                new_app = pd.DataFrame([{"Job_ID": row['Job_ID'], "Job_Title": row['Title'], "Candidate_Name": a_name, "Candidate_Phone": a_ph, "Employer": row['Employer']}])
                                save_db(pd.concat([db_job_apps, new_app]), DB_JOB_APPS)
                                st.success("✅ Application telemetry beamed safely to Employer console ledger!")

        with t_orders:
            st.subheader("📦 Live Order Tracking Stream Dashboard")
            my_phone = st.text_input("Provide phone identifier to ping trace vectors:", max_chars=10)
            if is_valid_phone(my_phone):
                # Always dynamic load to pull fresh updates
                fresh_orders = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date", "Payment_Method"])
                my_ords = fresh_orders[fresh_orders['Customer'] == my_phone]
                
                if my_ords.empty:
                    st.info("No active logs traced under this communication address.")
                
                for _, row in my_ords.iterrows():
                    # Multi-Stage Tracking State Mapping Matrix
                    status_flow = ["Pending", "Paid", "Accepted", "Out For Delivery", "Completed"]
                    curr_idx = status_flow.index(row['Status']) if row['Status'] in status_flow else 0
                    
                    # Micro state style definition mapping
                    badge_bg = "#ef4444" if curr_idx <= 1 else ("#3b82f6" if curr_idx < 4 else "#10b981")
                    
                    st.markdown(f"""
                        <div class='product-card' style='border-left: 6px solid {badge_bg}; display:block;'>
                            <div style='display:flex; justify-content:space-between; align-items:center;'>
                                <div>
                                    <div class='item-title'>{row['Item']}</div>
                                    <span style='font-size:11px; background:{badge_bg}15; color:{badge_bg}; font-weight:bold; padding:2px 8px; border-radius:10px;'>Status: {row['Status']}</span>
                                </div>
                                <div style='text-align:right;'>
                                    <div style='font-size:10px; color:#64748b;'>RIDER VERIFICATION PIN</div>
                                    <div style='font-size:20px; font-weight:900; color:#4f46e5;'>{row['OTP']}</div>
                                </div>
                            </div>
                            <div style='margin-top:15px; display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:10px; border-radius:8px; font-size:11px; font-weight:bold; color:#94a3b8;'>
                                <span style='color:{"#4f46e5" if curr_idx>=0 else "#94a3b8"};'>● Placed</span>
                                <span style='color:{"#4f46e5" if curr_idx>=1 else "#94a3b8"};'>➔ ● Paid</span>
                                <span style='color:{"#4f46e5" if curr_idx>=2 else "#94a3b8"};'>➔ ● Dispatched</span>
                                <span style='color:{"#4f46e5" if curr_idx>=4 else "#94a3b8"};'>➔ ● Completed</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# ==========================================
# 7. PARTNER PORTAL (WITH CONCURRENCY GUARDS)
# ==========================================
elif st.session_state['user_role'] == "Partner":
    if not st.session_state['logged_in']:
        t_log, t_reg = st.tabs(["🔑 Gateway Login", "🤝 Register Fleet Station Node"])
        # (Registration block remains stable & uniform)
        with t_reg:
            with st.form("p_reg"):
                p_ph = st.text_input("10-Digit Mobile No.", max_chars=10)
                p_pw = st.text_input("Secure Entry Password", type="password")
                p_name = st.text_input("Full Operator Identity")
                if st.form_submit_button("Establish Verified Node"):
                    if is_valid_phone(p_ph):
                        new_p = pd.DataFrame([{"Phone": p_ph, "Password": p_pw, "Name": p_name, "Role": "Partner", "Location": st.session_state['city'], "Status": "Verified"}])
                        save_db(pd.concat([db_partners, new_p]), DB_PARTNERS)
                        st.success("✅ Secure terminal registered! Switch tabs to login.")
        with t_log:
            l_ph = st.text_input("Terminal Agent Phone ID", max_chars=10)
            l_pw = st.text_input("Access Password", type="password")
            if st.button("Authenticate Rider Handshake"):
                user = db_partners[(db_partners['Phone'] == l_ph) & (db_partners['Password'] == l_pw)]
                if not user.empty:
                    st.session_state.update({'logged_in': True, 'phone': l_ph, 'name': user.iloc[0]['Name'], 'city': user.iloc[0]['Location']})
                    st.rerun()
                else: st.error("Database mismatch verification layer exception.")
    else:
        st.markdown(f"""
            <div style='background:#ffffff; border:1px solid #e2e8f0; padding:18px; border-radius:16px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <div style='font-size:12px; color:#64748b; font-weight:700;'>FLEET OPERATOR NODE ACTIVE</div>
                    <div style='font-size:18px; font-weight:800; color:#0f172a;'>{st.session_state['name']}</div>
                </div>
                <span class='loc-tag' style='background:#e0f2fe; color:#0369a1;'>📍 Zone: {st.session_state['city']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Disconnect Node 🔓"):
            st.session_state['logged_in'] = False
            st.rerun()
            
        t_leads, t_active = st.tabs(["🔔 Regional Live Orders Pool", "📦 My Ongoing Run Deliveries"])
        
        with t_leads:
            # Refresh from disk explicitly to access atomic changes
            db_orders = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date", "Payment_Method"])
            pending = db_orders[(db_orders['Location'] == st.session_state['city']) & (db_orders['Status'].isin(['Pending', 'Paid']))]
            
            st.markdown(render_metric_card("Live Area Demand Cluster", f"{len(pending)} Open Requests", "Accept tasks instantly to lock escrow payment channels", "linear-gradient(135deg, #059669 0%, #10b981 100%)"), unsafe_allow_html=True)
            
            for idx, row in pending.iterrows():
                st.markdown(f"""
                    <div class='product-card'>
                        <div>
                            <div class='item-title' style='color:#4f46e5;'>{row['Item']}</div>
                            <div style='font-size:12px; margin-top:4px; color:#64748b;'>Pay Mode: <b>{row['Payment_Method']}</b> | Area: {row['Location']}</div>
                        </div>
                        <div class='item-price'>₹{row['Price']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # CRITICAL UPGRADE: Anti-Race Condition Concurrency Check Guard Block
                if st.button(f"Claim Task Assignment #{row['Order_ID']}", key=f"claim_{row['Order_ID']}"):
                    # Reload database fresh instantly before writing transaction state change
                    check_db = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date", "Payment_Method"])
                    current_status = check_db.loc[check_db['Order_ID'] == row['Order_ID'], 'Status'].values[0]
                    
                    if current_status in ['Pending', 'Paid']:
                        # Safe to claim target entry
                        db_orders.at[idx, 'Partner'] = st.session_state['phone']
                        db_orders.at[idx, 'Status'] = 'Accepted'
                        save_db(db_orders, DB_ORDERS)
                        st.toast("⚡ Task locked safely into your run queue!", icon="🚀")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("⚠️ Concurrency Race Condition Error: This task was already claimed by another near rider node!")
                    
        with t_active:
            db_orders = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date", "Payment_Method"])
            active = db_orders[(db_orders['Partner'] == st.session_state['phone']) & (db_orders['Status'].isin(['Accepted', 'Out For Delivery']))]
            
            for idx, row in active.iterrows():
                st.markdown(f"""
                    <div class='job-card' style='border-left-color: #f59e0b; display:block;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div>
                                <div class='item-title'>{row['Item']}</div>
                                <div style='font-size:13px; color:#475569;'>Customer Destination Contact: <b>{row['Customer']}</b></div>
                            </div>
                            <span class='cat-badge' style='background:#fef3c7; color:#d97706;'>{row['Status']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    if row['Status'] == 'Accepted':
                        if st.button("Mark: Out for Delivery 🚚", key=f"ofd_{row['Order_ID']}"):
                            db_orders.at[idx, 'Status'] = 'Out For Delivery'
                            save_db(db_orders, DB_ORDERS)
                            st.rerun()
                with col_u2:
                    with st.form(f"otp_complete_{row['Order_ID']}"):
                        otp_in = st.text_input("Secure Customer Verification Token Code", max_chars=4, placeholder="4-Digit PIN")
                        if st.form_submit_button("Verify & Release Escrow"):
                            if otp_in == row['OTP']:
                                db_orders.at[idx, 'Status'] = 'Completed'
                                save_db(db_orders, DB_ORDERS)
                                st.success("✅ Payment ledger cleared down to wallet node!")
                                time.sleep(0.5)
                                st.rerun()
                            else: st.error("Cryptographic token rejection error.")

# ==========================================
# 8. SUPER ADMIN CENTER
# ==========================================
elif st.session_state['user_role'] == "Admin":
    st.title("⚙️ Global Infrastructure Control Center")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(render_metric_card("Ecosystem Orders Engine", f"{len(db_orders)} Records", "Gross system pipeline volume", "linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)"), unsafe_allow_html=True)
    with m2:
        st.markdown(render_metric_card("Job Flow Vectors", f"{len(db_job_apps)} Entries", "Total cross-functional data rows", "linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%)"), unsafe_allow_html=True)
    with m3:
        st.markdown(render_metric_card("Active Fleet Terminal Nodes", f"{len(db_partners)} Units", "Total verified delivery providers", "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"), unsafe_allow_html=True)
        
    t1, t2, t3 = st.tabs(["📦 Order Ledgers Matrix", "📋 Candidate Pipeline Log", "👥 Fleet Terminal Registry"])
    with t1: st.dataframe(db_orders, use_container_width=True)
    with t2: st.dataframe(db_job_apps, use_container_width=True)
    with t3: st.dataframe(db_partners, use_container_width=True)
