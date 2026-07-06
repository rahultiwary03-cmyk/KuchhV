import streamlit as st
import pandas as pd
import os
from datetime import datetime
import random

# ==========================================
# 1. SETUP & MASSIVE INDIAN MARKET DATABASE
# ==========================================
st.set_page_config(page_title="KuchhV | Har Zarurat, Ek Platform", layout="wide", page_icon="🛍️")

REQUIREMENTS_FILE = "req_v3.csv"
PARTNERS_FILE = "partners_v3.csv"
ORDERS_FILE = "orders_v3.csv"

# Comprehensive Indian Service & Product List for Autocomplete
INDIAN_SERVICES = [
    "Grocery & Daily Needs", "Fresh Vegetables & Fruits", "Dairy & Milk Delivery", 
    "Plumber", "Electrician", "Carpenter", "AC Repair & Servicing", 
    "RO Water Purifier Repair", "Home Deep Cleaning", "Pest Control",
    "IT Freelancer (Python/Excel)", "Web Developer", "Graphic Designer", "Video Editor",
    "Tractor Rental", "JCB & Crane Rental", "Mini Truck (Tata Ace) Booking", "Bike Taxi", "Car Rental (Self Drive)",
    "CA & GST Filing (Pragya Kendra)", "Lawyer & Notary", "Real Estate (Rent/Buy)", "PG & Hostel Booking",
    "Doctor Appointment", "Medicine Delivery", "Lab Test at Home",
    "Men's Salon", "Women's Parlour", "Bridal Makeup", "Mehndi Artist",
    "Tent House & Decorator", "Caterers (Halwai)", "Pandit Ji for Puja",
    "Labour Contractor (Daily Wage)", "Rajmistri (Mason)"
]

# Create Data Files
for file, cols in [
    (REQUIREMENTS_FILE, ["Timestamp", "Phone", "Category", "Requirement", "Location", "Status"]),
    (PARTNERS_FILE, ["Phone", "Password", "Business_Name", "Category", "Verification_Status", "Base_Price"]),
    (ORDERS_FILE, ["Timestamp", "Customer_Phone", "Partner", "Service", "Price", "Platform_Fee", "Partner_Earning", "Status"])
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)

def load_data(file_name):
    return pd.read_csv(file_name, dtype=str)

def save_data(file_name, new_data):
    df = pd.DataFrame([new_data])
    df.to_csv(file_name, mode='a', header=False, index=False)

# Professional Colorful CSS
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    [data-testid="stSidebar"] { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    .search-box { font-size: 20px; font-weight: bold; }
    .price-card { background: white; padding: 20px; border-radius: 12px; border-left: 5px solid #10b981; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px;}
    .fee-text { color: #ef4444; font-size: 14px; font-weight: bold;}
    .earning-text { color: #10b981; font-size: 14px; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

if 'logged_in_partner' not in st.session_state:
    st.session_state['logged_in_partner'] = None

# ==========================================
# 2. APP NAVIGATION
# ==========================================
st.sidebar.title("📱 KuchhV Super App")
st.sidebar.write("---")
app_mode = st.sidebar.radio("Main Menu:", ["🏠 Customer Marketplace", "📢 Requirement Hub", "💼 Partner Portal", "⚙️ Admin Center"])
st.sidebar.write("---")
st.sidebar.caption("Platform Fee: 1% Only")

# ==========================================
# 3. CUSTOMER MARKETPLACE (Search, Compare & Book)
# ==========================================
if app_mode == "🏠 Customer Marketplace":
    st.title("🛍️ KuchhV Marketplace")
    st.markdown("### Search anything. Compare prices. Book the lowest.")
    
    # Universal Search Bar with Autocomplete
    selected_service = st.selectbox("🔍 What do you need today?", ["-- Select or Type Here --"] + INDIAN_SERVICES)
    
    if selected_service != "-- Select or Type Here --":
        st.write("---")
        st.subheader(f"Available Partners for '{selected_service}'")
        
        partner_df = load_data(PARTNERS_FILE)
        available = partner_df[(partner_df['Category'] == selected_service) & (partner_df['Verification_Status'] == 'Verified ✅')].copy()
        
        if not available.empty:
            # Convert Base_Price to numeric for sorting, handling any non-numeric gracefully
            available['Base_Price'] = pd.to_numeric(available['Base_Price'], errors='coerce').fillna(999)
            available = available.sort_values(by='Base_Price') # Lowest price first
            
            st.success(f"✅ Found {len(available)} verified partner(s). Showing lowest prices first.")
            
            for index, row in available.iterrows():
                partner_name = row['Business_Name']
                price = float(row['Base_Price'])
                platform_fee = price * 0.01  # 1% logic
                partner_earning = price - platform_fee
                
                st.markdown(f"""
                <div class='price-card'>
                    <h3>🏪 {partner_name}</h3>
                    <p style='font-size: 20px; font-weight: bold; color: #1e293b;'>Price: ₹{price:,.2f}</p>
                    <p class='fee-text'>KuchhV Platform Fee (1%): ₹{platform_fee:,.2f}</p>
                    <p class='earning-text'>Partner Earns: ₹{partner_earning:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"Book {partner_name} Now"):
                    with st.form(f"book_{index}"):
                        cust_phone = st.text_input("Your Mobile Number (e.g., for Chatra location)")
                        if st.form_submit_button("Confirm Booking"):
                            if cust_phone:
                                save_data(ORDERS_FILE, {
                                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Customer_Phone": cust_phone, "Partner": partner_name, "Service": selected_service,
                                    "Price": price, "Platform_Fee": platform_fee, "Partner_Earning": partner_earning, "Status": "Pending"
                                })
                                st.success("🎉 Booking Confirmed! The partner will contact you shortly.")
                            else:
                                st.error("Please enter your mobile number.")
        else:
            st.warning("No verified partners found for this service right now.")
            st.info("💡 Post this in the **Requirement Hub** (from the left menu) and partners will contact you!")

# ==========================================
# 4. REQUIREMENT HUB
# ==========================================
elif app_mode == "📢 Requirement Hub":
    st.title("📢 Custom Requirement Hub")
    st.write("Need bulk materials, a large workforce, or custom software? Post it here.")
    
    with st.form("req_form"):
        col1, col2 = st.columns(2)
        with col1:
            req_cat = st.selectbox("Category", INDIAN_SERVICES)
            loc = st.text_input("Pincode / City")
        with col2:
            phone = st.text_input("Mobile Number")
        
        desc = st.text_area("Detail your exact need:")
        
        if st.form_submit_button("Broadcast to Partners 🚀"):
            if phone and desc and loc:
                save_data(REQUIREMENTS_FILE, {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Phone": phone, "Category": req_cat, "Requirement": desc, "Location": loc, "Status": "Open"
                })
                st.success("✅ Broadcasted! Partners will bid on your requirement.")
                st.balloons()
            else:
                st.error("Please fill all details.")

# ==========================================
# 5. PARTNER PORTAL (Registration & Dashboard)
# ==========================================
elif app_mode == "💼 Partner Portal":
    st.title("💼 Partner Business Portal")
    
    if st.session_state['logged_in_partner'] is None:
        t1, t2 = st.tabs(["🔐 Login", "📝 Register Business"])
        
        with t2:
            st.subheader("Join KuchhV & Grow Your Business")
            st.markdown("*Platform charges only 1% fee on your total billing.*")
            with st.form("reg_form"):
                biz_name = st.text_input("Business / Freelancer Name")
                phone = st.text_input("Mobile Number")
                pwd = st.text_input("Create Password", type="password")
                cat = st.selectbox("Your Primary Category", INDIAN_SERVICES)
                base_price = st.number_input("Your Starting Price / Hourly Rate (₹)", min_value=10, value=100)
                
                if st.form_submit_button("Register"):
                    pdf = load_data(PARTNERS_FILE)
                    if phone in pdf['Phone'].values:
                        st.error("Mobile Number already registered!")
                    else:
                        save_data(PARTNERS_FILE, {
                            "Phone": phone, "Password": pwd, "Business_Name": biz_name, 
                            "Category": cat, "Verification_Status": "Pending", "Base_Price": base_price
                        })
                        st.success("✅ Registered! Please wait for Admin approval.")
                        
        with t1:
            st.subheader("Secure Login")
            l_phone = st.text_input("Mobile Number ")
            l_pwd = st.text_input("Password ", type="password")
            
            if st.button("Login Now"):
                pdf = load_data(PARTNERS_FILE)
                user = pdf[(pdf['Phone'] == l_phone) & (pdf['Password'] == l_pwd)]
                
                if not user.empty:
                    stat = user.iloc[0]['Verification_Status']
                    if stat == 'Verified ✅':
                        st.session_state['logged_in_partner'] = user.iloc[0]['Business_Name']
                        st.success("Login Successful!")
                        st.rerun()
                    else:
                        st.error(f"Account Status: {stat}. Admin approval is required.")
                else:
                    st.error("Invalid credentials.")
    else:
        st.success(f"👋 Welcome, {st.session_state['logged_in_partner']}!")
        if st.button("Logout"):
            st.session_state['logged_in_partner'] = None
            st.rerun()
            
        st.subheader("📦 Your Direct Orders")
        odf = load_data(ORDERS_FILE)
        my_orders = odf[odf['Partner'] == st.session_state['logged_in_partner']]
        st.dataframe(my_orders, use_container_width=True)

# ==========================================
# 6. ADMIN CENTER (1-Click Approval Fix)
# ==========================================
elif app_mode == "⚙️ Admin Center":
    st.title("⚙️ Super Admin Control Room")
    
    pdf = load_data(PARTNERS_FILE)
    
    st.subheader("Action Required: Pending Approvals")
    pending = pdf[pdf['Verification_Status'] == 'Pending']
    
    if not pending.empty:
        for idx, row in pending.iterrows():
            with st.container():
                st.markdown(f"**{row['Business_Name']}** | {row['Category']} | 📞 {row['Phone']}")
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1:
                    if st.button("Approve ✅", key=f"app_{idx}"):
                        pdf.at[idx, 'Verification_Status'] = 'Verified ✅'
                        pdf.to_csv(PARTNERS_FILE, index=False)
                        st.success(f"{row['Business_Name']} Approved!")
                        st.rerun()
                with col2:
                    if st.button("Reject ❌", key=f"rej_{idx}"):
                        pdf.at[idx, 'Verification_Status'] = 'Rejected ❌'
                        pdf.to_csv(PARTNERS_FILE, index=False)
                        st.error(f"{row['Business_Name']} Rejected!")
                        st.rerun()
                st.write("---")
    else:
        st.info("No pending approvals.")
        
    st.subheader("All Verified Partners")
    verified = pdf[pdf['Verification_Status'] == 'Verified ✅'].drop(columns=['Password'])
    st.dataframe(verified, use_container_width=True)
