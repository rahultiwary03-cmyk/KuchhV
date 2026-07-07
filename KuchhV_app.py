import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime

# ==========================================
# 1. SETUP & SESSION STATE
# ==========================================
st.set_page_config(page_title="KuchhV | Super App", layout="centered", initial_sidebar_state="collapsed")

DB_CATALOG = "db_catalog.csv"
DB_PARTNERS = "db_partners.csv"
DB_ORDERS = "db_orders.csv"
DB_REQS = "db_reqs.csv"

# Initialize Session State
if 'user_type' not in st.session_state:
    st.session_state.update({'user_type': 'Customer', 'logged_in': False, 'phone': '', 'name': '', 'location': 'Chatra'})

# ==========================================
# 2. MEGA DATABASE & GEO-LOCATION ENGINE
# ==========================================
DISTRICTS = ["Chatra", "Ranchi", "Patna", "Gaya", "Delhi", "Pune", "Hazaribagh"]
CATEGORIES = ["Grocery & Essentials", "Home Services (Plumber/AC)", "Local Jobs", "Heavy Machinery/Tractor", "IT & CSC Forms", "Medical & Lab"]

@st.cache_data
def initialize_mega_database():
    if os.path.exists(DB_CATALOG):
        return pd.read_csv(DB_CATALOG, dtype=str)
    
    with st.spinner("🚀 Booting Pan-India Geo-Locked Servers..."):
        data = []
        items_map = {
            "Grocery & Essentials": ["Aashirvaad Atta", "Amul Milk", "Fresh Onion", "Basmati Rice", "Paneer"],
            "Home Services (Plumber/AC)": ["Plumber Visit", "AC Service", "Electrician", "Deep Cleaning", "RO Repair"],
            "Local Jobs": ["Delivery Boy", "Shop Assistant", "Cook", "Data Entry", "Security Guard"],
            "Heavy Machinery/Tractor": ["Tractor Rental", "JCB Booking", "Tata Ace", "Water Tanker"],
            "IT & CSC Forms": ["GST Filing", "Pension Form", "Excel Work", "Website Design"],
            "Medical & Lab": ["Lab Test (Home)", "Medicine Delivery", "Doctor Appt"]
        }
        
        for i in range(10050):
            cat = random.choice(CATEGORIES)
            item = random.choice(items_map[cat])
            loc = random.choice(DISTRICTS)
            
            # Dynamic Tier Pricing (Tier 3 like Chatra is cheaper)
            base = random.randint(100, 2000)
            if loc in ["Chatra", "Hazaribagh", "Gaya"]:
                price = int(base * 0.7) # 30% cheaper
            else:
                price = base
                
            data.append({
                "ID": f"ITM{10000+i}", "Item_Name": f"{item} ({loc} Special)", "Category": cat, 
                "Price": str(price), "Location": loc, "Partner_ID": "Unassigned"
            })
        
        df = pd.DataFrame(data)
        df.to_csv(DB_CATALOG, index=False)
        return df

mega_catalog = initialize_mega_database()

# Init other tables
for file, cols in [
    (DB_PARTNERS, ["Phone", "Password", "Name", "Category", "Location", "Status"]),
    (DB_ORDERS, ["Order_ID", "Timestamp", "Customer_Phone", "Item_Name", "Price", "Location", "Partner_Phone", "Status", "OTP"]),
    (DB_REQS, ["Req_ID", "Timestamp", "Customer_Phone", "Category", "Location", "Requirement", "Status"])
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)

def read_db(file): return pd.read_csv(file, dtype=str)
def save_db(file, df): df.to_csv(file, index=False)

# ==========================================
# 3. NATIVE MOBILE APP CSS
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f3f4f6; font-family: 'Segoe UI', sans-serif; }
    .header { background: white; padding: 15px; border-bottom: 1px solid #e5e7eb; position: sticky; top: 0; z-index: 100;}
    .card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e5e7eb;}
    .title { font-size: 16px; font-weight: bold; color: #111827;}
    .price { font-size: 18px; font-weight: 900; color: #059669;}
    .loc-badge { background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;}
    .status-badge { background: #fef3c7; color: #d97706; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: bold;}
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. APP NAVIGATION & HEADER
# ==========================================
col1, col2 = st.columns([3, 1])
with col1:
    st.session_state['location'] = st.selectbox("📍 Your Location", DISTRICTS, index=DISTRICTS.index(st.session_state['location']))
with col2:
    st.session_state['user_type'] = st.selectbox("👤 Profile", ["Customer", "Partner", "Admin"])

st.write("---")

# ==========================================
# 5. CUSTOMER INTERFACE (Geo-Locked)
# ==========================================
if st.session_state['user_type'] == "Customer":
    tab1, tab2, tab3 = st.tabs(["🛒 Local Shops", "📢 Custom Request", "📦 My Orders"])
    
    with tab1:
        st.markdown(f"### Available in {st.session_state['location']}")
        local_catalog = mega_catalog[mega_catalog['Location'] == st.session_state['location']]
        
        search = st.text_input("🔍 Search local items, shops, jobs...")
        if search:
            local_catalog = local_catalog[local_catalog['Item_Name'].str.contains(search, case=False, na=False)]
        else:
            local_catalog = local_catalog.sample(min(10, len(local_catalog))) # Show 10 random
            
        for _, row in local_catalog.iterrows():
            st.markdown(f"""
            <div class="card">
                <span class="loc-badge">📍 {row['Location']}</span>
                <div class="title" style="margin-top: 8px;">{row['Item_Name']}</div>
                <div style="font-size: 13px; color: #6b7280;">{row['Category']}</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div class="price">₹{row['Price']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Book Now"):
                with st.form(f"book_{row['ID']}"):
                    c_phone = st.text_input("Mobile No.")
                    if st.form_submit_button("Confirm Order"):
                        if c_phone:
                            orders = read_db(DB_ORDERS)
                            new_order = pd.DataFrame([{
                                "Order_ID": f"ORD{random.randint(1000,9999)}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "Customer_Phone": c_phone, "Item_Name": row['Item_Name'], "Price": row['Price'], 
                                "Location": row['Location'], "Partner_Phone": "Unassigned", "Status": "Pending", "OTP": str(random.randint(1000,9999))
                            }])
                            save_db(DB_ORDERS, pd.concat([orders, new_order]))
                            st.success("✅ Order placed successfully! Local partners are being notified.")
                        else:
                            st.error("Phone required.")

    with tab2:
        st.markdown("### Reverse Bidding Engine")
        st.info(f"Can't find what you need in {st.session_state['location']}? Post it here!")
        with st.form("req_form"):
            c_phone = st.text_input("Your Phone Number")
            c_cat = st.selectbox("Category", CATEGORIES)
            c_req = st.text_area("Describe your exact requirement")
            if st.form_submit_button("Broadcast to Partners 🚀"):
                if c_phone and c_req:
                    reqs = read_db(DB_REQS)
                    new_req = pd.DataFrame([{
                        "Req_ID": f"REQ{random.randint(1000,9999)}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Customer_Phone": c_phone, "Category": c_cat, "Location": st.session_state['location'], 
                        "Requirement": c_req, "Status": "Open"
                    }])
                    save_db(DB_REQS, pd.concat([reqs, new_req]))
                    st.success("✅ Requirement broadcasted to local partners!")

    with tab3:
        st.markdown("### Active Orders & OTPs")
        phone = st.text_input("Enter your phone number to track orders:")
        if phone:
            orders = read_db(DB_ORDERS)
            my_orders = orders[orders['Customer_Phone'] == phone]
            for _, row in my_orders.iterrows():
                st.markdown(f"""
                <div class="card">
                    <div class="title">{row['Item_Name']}</div>
                    <div style="margin: 8px 0;"><span class="status-badge">{row['Status']}</span></div>
                    <div style="font-size: 14px;">Price: ₹{row['Price']}</div>
                    <div style="font-size: 14px; font-weight:bold; color:#dc2626; margin-top:5px;">Your Secret OTP: {row['OTP']}</div>
                    <div style="font-size: 11px; color: gray;">Give this OTP to partner to complete the order.</div>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 6. PARTNER INTERFACE (Lifecycle & OTP)
# ==========================================
elif st.session_state['user_type'] == "Partner":
    if not st.session_state['logged_in']:
        t1, t2 = st.tabs(["Login", "Register Business"])
        with t2:
            with st.form("preg"):
                p_ph = st.text_input("Mobile No.")
                p_pw = st.text_input("Password", type="password")
                p_name = st.text_input("Business Name")
                p_cat = st.selectbox("Category", CATEGORIES)
                p_loc = st.selectbox("City/District", DISTRICTS)
                if st.form_submit_button("Apply for KYC"):
                    partners = read_db(DB_PARTNERS)
                    if p_ph in partners['Phone'].values:
                        st.error("Already registered.")
                    else:
                        new_p = pd.DataFrame([{"Phone": p_ph, "Password": p_pw, "Name": p_name, "Category": p_cat, "Location": p_loc, "Status": "Pending"}])
                        save_db(DB_PARTNERS, pd.concat([partners, new_p]))
                        st.success("✅ Application sent to Admin.")
        with t1:
            p_ph = st.text_input("Mobile ")
            p_pw = st.text_input("Password ", type="password")
            if st.button("Secure Login"):
                partners = read_db(DB_PARTNERS)
                user = partners[(partners['Phone'] == p_ph) & (partners['Password'] == p_pw)]
                if not user.empty:
                    if user.iloc[0]['Status'] == 'Verified':
                        st.session_state.update({'logged_in': True, 'phone': p_ph, 'name': user.iloc[0]['Name'], 'location': user.iloc[0]['Location']})
                        st.rerun()
                    else:
                        st.error("Admin approval pending.")
                else:
                    st.error("Invalid credentials.")
    else:
        st.success(f"💼 Welcome {st.session_state['name']} | 📍 {st.session_state['location']}")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
            
        tab_new, tab_act = st.tabs(["🔔 New Leads", "📦 Active Orders"])
        
        with tab_new:
            st.write("Orders waiting for a partner in your area:")
            orders = read_db(DB_ORDERS)
            # Find Unassigned orders in Partner's Location
            open_orders = orders[(orders['Location'] == st.session_state['location']) & (orders['Status'] == 'Pending')]
            for idx, row in open_orders.iterrows():
                st.markdown(f"<div class='card'><b>{row['Item_Name']}</b><br>Price: ₹{row['Price']} | Customer: {row['Customer_Phone']}</div>", unsafe_allow_html=True)
                if st.button(f"Accept Order {row['Order_ID']}"):
                    orders.at[idx, 'Partner_Phone'] = st.session_state['phone']
                    orders.at[idx, 'Status'] = 'Accepted'
                    save_db(DB_ORDERS, orders)
                    st.success("Order Accepted! Go to Active Orders to complete it.")
                    st.rerun()

        with tab_act:
            st.write("Orders you have accepted:")
            orders = read_db(DB_ORDERS)
            my_active = orders[(orders['Partner_Phone'] == st.session_state['phone']) & (orders['Status'] == 'Accepted')]
            for idx, row in my_active.iterrows():
                st.markdown(f"<div class='card' style='border-color:#10b981;'><b>{row['Item_Name']}</b><br>Customer: {row['Customer_Phone']}</div>", unsafe_allow_html=True)
                with st.form(f"otp_{row['Order_ID']}"):
                    entered_otp = st.text_input("Ask Customer for 4-digit OTP to complete:")
                    if st.form_submit_button("Verify & Complete"):
                        if entered_otp == row['OTP']:
                            orders.at[idx, 'Status'] = 'Completed ✅'
                            save_db(DB_ORDERS, orders)
                            st.success("Service Completed Successfully!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Invalid OTP.")

# ==========================================
# 7. SUPER ADMIN INTERFACE
# ==========================================
elif st.session_state['user_type'] == "Admin":
    st.title("⚙️ Operations Control Room")
    t1, t2 = st.tabs(["👥 Partner Verifications", "📊 Live Orders Oversight"])
    
    with t1:
        st.write("Approve or Reject Partners (KYC)")
        partners = read_db(DB_PARTNERS)
        edited_p = st.data_editor(partners, key="admin_p", use_container_width=True)
        if st.button("Save Partner Status"):
            save_db(DB_PARTNERS, edited_p)
            st.success("Database Updated!")
            
    with t2:
        st.write("Global Order Tracking")
        orders = read_db(DB_ORDERS)
        st.dataframe(orders, use_container_width=True)
