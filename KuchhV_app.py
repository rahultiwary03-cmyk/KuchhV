import streamlit as st
import pandas as pd
import os
import random
import difflib
from datetime import datetime

# ==========================================
# 1. SETUP & SESSION STATE
# ==========================================
st.set_page_config(page_title="KuchhV | Super App", layout="centered", initial_sidebar_state="collapsed")

DB_CATALOG = "v15_catalog.csv"
DB_JOBS = "v15_jobs.csv"
DB_PARTNERS = "v15_partners.csv"
DB_ORDERS = "v15_orders.csv"
DB_JOB_APPS = "v15_job_apps.csv"

LOCATIONS = {"Chatra": 1.0, "Hazaribagh": 1.0, "Ranchi": 1.1, "Delhi": 1.3}

if 'user_role' not in st.session_state:
    st.session_state.update({'user_role': 'Customer', 'logged_in': False, 'phone': '', 'name': '', 'city': 'Chatra'})

# ==========================================
# 2. REALISTIC DATABASE GENERATOR
# ==========================================
@st.cache_data
def generate_authentic_dbs():
    if not os.path.exists(DB_CATALOG):
        with st.spinner("🚀 Building Authentic Pan-India Database..."):
            catalog_data = []
            
            # 1. Real Items with Real Base Prices
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
                    # Minor price variation by location
                    final_price = int(item["Base_Price"] * multiplier)
                    catalog_data.append({
                        "Item_ID": f"ITM{item_id_counter}", "Name": item["Name"], "Category": item["Cat"],
                        "Price": final_price, "Location": loc
                    })
                    item_id_counter += 1
            pd.DataFrame(catalog_data).to_csv(DB_CATALOG, index=False)

            # 2. Real Jobs with Real Employers
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

def save_db(df, file): df.to_csv(file, index=False)

db_partners = load_db(DB_PARTNERS, ["Phone", "Password", "Name", "Role", "Location", "Status"])
db_orders = load_db(DB_ORDERS, ["Order_ID", "Customer", "Item", "Price", "Location", "Partner", "Status", "OTP", "Date"])
db_job_apps = load_db(DB_JOB_APPS, ["Job_ID", "Job_Title", "Candidate_Name", "Candidate_Phone", "Employer"])

# ==========================================
# 3. HELPER: STRICT PHONE VALIDATION
# ==========================================
def is_valid_phone(phone_str):
    return len(phone_str) == 10 and phone_str.isdigit()

# ==========================================
# 4. UI CSS
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    .product-card { background: white; border-radius: 12px; padding: 15px; border: 1px solid #e2e8f0; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;}
    .job-card { background: #ffffff; border-left: 5px solid #10b981; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .item-title { font-size: 16px; font-weight: 800; color: #0f172a;}
    .item-price { font-size: 18px; font-weight: 900; color: #10b981;}
    .loc-tag { font-size: 11px; background: #f1f5f9; color: #64748b; padding: 2px 6px; border-radius: 4px; font-weight: bold;}
    .fallback-box { background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 5. TOP HEADER
# ==========================================
col_loc, col_role = st.columns([2, 1])
with col_loc:
    st.session_state['city'] = st.selectbox("📍 Set Location", list(LOCATIONS.keys()), index=list(LOCATIONS.keys()).index(st.session_state['city']))
with col_role:
    st.session_state['user_role'] = st.selectbox("👤 Switch Role", ["Customer", "Partner", "Admin"])
st.write("---")

# ==========================================
# 6. CUSTOMER INTERFACE
# ==========================================
if st.session_state['user_role'] == "Customer":
    
    search_query = st.text_input("🔍 What do you need today?", placeholder="Try typing 'plumber', 'atta', 'tractor'...")
    
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

    if search_query and not results.empty:
        st.success(f"✅ Showing results in {st.session_state['city']}")
        for _, row in results.iterrows():
            st.markdown(f"<div class='product-card'><div><div class='item-title'>{row['Name']}</div><div class='loc-tag'>KuchhV Assured</div></div><div class='item-price'>₹{row['Price']}</div></div>", unsafe_allow_html=True)
            with st.expander("Book Now"):
                with st.form(f"bk_{row['Item_ID']}"):
                    c_ph = st.text_input("Enter 10-Digit Mobile Number", max_chars=10)
                    if st.form_submit_button("Confirm Order Securely"):
                        if is_valid_phone(c_ph):
                            new_ord = pd.DataFrame([{"Order_ID": f"ORD{random.randint(10000,99999)}", "Customer": c_ph, "Item": row['Name'], "Price": row['Price'], "Location": row['Location'], "Partner": "Unassigned", "Status": "Pending", "OTP": str(random.randint(1000,9999)), "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                            save_db(pd.concat([db_orders, new_ord]), DB_ORDERS)
                            st.success("🎉 Order Placed! Go to 'My Orders' for tracking.")
                        else:
                            st.error("⚠️ Please enter a valid 10-digit mobile number.")

    elif search_query and results.empty:
        st.markdown("<div class='fallback-box'><h3 style='margin:0; color:white;'>🎙️ Not found in catalog?</h3><p style='margin:0; font-size:14px;'>Tell us exactly what you need. Local partners will arrange it.</p></div>", unsafe_allow_html=True)
        with st.form("custom_req"):
            st.text_area("Your Requirement", value=search_query)
            c_ph = st.text_input("10-Digit Mobile Number", max_chars=10)
            if st.form_submit_button("Send Request to Partners 🚀"):
                if is_valid_phone(c_ph):
                    st.success("✅ Broadcasted to local verified partners!")
                else:
                    st.error("⚠️ Please enter a valid 10-digit mobile number.")

    else:
        t_home, t_jobs, t_orders = st.tabs(["🛒 Grocery & Services", "💼 Local Jobs", "📦 My Orders"])
        
        with t_home:
            st.subheader(f"⚡ Top Categories in {st.session_state['city']}")
            for _, row in local_catalog.iterrows():
                st.markdown(f"<div class='product-card'><div><div class='item-title'>{row['Name']}</div><div class='loc-tag'>KuchhV Assured</div></div><div class='item-price'>₹{row['Price']}</div></div>", unsafe_allow_html=True)
                with st.expander("Order"):
                    with st.form(f"h_{row['Item_ID']}"):
                        c_ph = st.text_input("10-Digit Mobile Number", max_chars=10)
                        if st.form_submit_button("Order Now"):
                            if is_valid_phone(c_ph):
                                new_ord = pd.DataFrame([{"Order_ID": f"ORD{random.randint(10000,99999)}", "Customer": c_ph, "Item": row['Name'], "Price": row['Price'], "Location": row['Location'], "Partner": "Unassigned", "Status": "Pending", "OTP": str(random.randint(1000,9999)), "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                                save_db(pd.concat([db_orders, new_ord]), DB_ORDERS)
                                st.success("✅ Order Placed!")
                            else:
                                st.error("⚠️ Please enter a valid 10-digit mobile number.")

        with t_jobs:
            st.subheader(f"💼 Hiring in {st.session_state['city']}")
            jobs = pd.read_csv(DB_JOBS, dtype=str)
            local_jobs = jobs[jobs['Location'] == st.session_state['city']]
            for _, row in local_jobs.iterrows():
                st.markdown(f"<div class='job-card'><div class='item-title'>{row['Title']}</div><div style='color: gray; font-size:13px; margin: 4px 0;'>🏢 {row['Employer']}</div><div class='item-price' style='color: #ea580c;'>{row['Salary']}</div></div>", unsafe_allow_html=True)
                with st.expander("Apply Now"):
                    with st.form(f"app_{row['Job_ID']}"):
                        a_name = st.text_input("Full Name")
                        a_ph = st.text_input("10-Digit Mobile Number", max_chars=10)
                        if st.form_submit_button("Send Application"):
                            if a_name and is_valid_phone(a_ph):
                                new_app = pd.DataFrame([{"Job_ID": row['Job_ID'], "Job_Title": row['Title'], "Candidate_Name": a_name, "Candidate_Phone": a_ph, "Employer": row['Employer']}])
                                save_db(pd.concat([db_job_apps, new_app]), DB_JOB_APPS)
                                st.success("✅ Application sent to employer!")
                            else:
                                st.error("⚠️ Invalid Name or 10-digit Phone.")

        with t_orders:
            my_phone = st.text_input("Enter 10-Digit Phone No. to track orders:", max_chars=10)
            if is_valid_phone(my_phone):
                my_ords = db_orders[db_orders['Customer'] == my_phone]
                if my_ords.empty:
                    st.info("No active orders found.")
                for _, row in my_ords.iterrows():
                    color = "#10b981" if row['Status'] == "Completed" else "#ea580c"
                    st.markdown(f"<div class='product-card' style='border-left: 5px solid {color};'><div><div class='item-title'>{row['Item']}</div><div class='loc-tag'>{row['Status']}</div></div><div style='text-align: right;'><div style='font-size:12px;'>Secret OTP</div><div style='font-size: 18px; font-weight: 900; color:#dc2626;'>{row['OTP']}</div></div></div>", unsafe_allow_html=True)

# ==========================================
# 7. PARTNER PORTAL
# ==========================================
elif st.session_state['user_role'] == "Partner":
    if not st.session_state['logged_in']:
        t_log, t_reg = st.tabs(["Login", "Register Business"])
        with t_reg:
            with st.form("p_reg"):
                p_ph = st.text_input("10-Digit Mobile No.", max_chars=10)
                p_pw = st.text_input("Create Password", type="password")
                p_name = st.text_input("Full Name / Business Name")
                if st.form_submit_button("Register"):
                    if is_valid_phone(p_ph):
                        new_p = pd.DataFrame([{"Phone": p_ph, "Password": p_pw, "Name": p_name, "Role": "Partner", "Location": st.session_state['city'], "Status": "Verified"}])
                        save_db(pd.concat([db_partners, new_p]), DB_PARTNERS)
                        st.success("✅ Registered Successfully!")
                    else:
                        st.error("⚠️ Please enter a valid 10-digit mobile number.")
        with t_log:
            l_ph = st.text_input("10-Digit Mobile No. ", max_chars=10)
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
                            st.rerun()
                        else:
                            st.error("Wrong OTP entered.")

# ==========================================
# 8. SUPER ADMIN CENTER
# ==========================================
elif st.session_state['user_role'] == "Admin":
    st.title("⚙️ Master Admin Control Room")
    t1, t2, t3 = st.tabs(["📦 Track All Orders", "📋 Job Applications (Leads)", "👥 Partners"])
    
    with t1:
        st.subheader("Global Service & Delivery Orders")
        st.dataframe(db_orders, use_container_width=True)
    with t2:
        st.subheader("Job Applications (Ecosystem B)")
        st.dataframe(db_job_apps, use_container_width=True)
    with t3:
        st.subheader("Registered Partners (Ecosystem A)")
        st.dataframe(db_partners, use_container_width=True)
