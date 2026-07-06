import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. SETUP & PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="KuchhV | Super App", layout="wide", page_icon="🚀")

REQUIREMENTS_FILE = "requirements_v2.csv"
PARTNERS_FILE = "partners_v2.csv"
ORDERS_FILE = "orders_v2.csv"

# Create CSV files if they don't exist
if not os.path.exists(REQUIREMENTS_FILE):
    pd.DataFrame(columns=["Timestamp", "Customer_Phone", "Category", "Description", "Location", "Status"]).to_csv(REQUIREMENTS_FILE, index=False)

if not os.path.exists(PARTNERS_FILE):
    pd.DataFrame(columns=["Phone", "Password", "Business_Name", "Category", "Verification_Status"]).to_csv(PARTNERS_FILE, index=False)

if not os.path.exists(ORDERS_FILE):
    pd.DataFrame(columns=["Timestamp", "Customer_Phone", "Category", "Requirement", "Status", "Partner_Assigned"]).to_csv(ORDERS_FILE, index=False)

def load_data(file_name):
    if file_name == PARTNERS_FILE:
        return pd.read_csv(file_name, dtype={"Phone": str, "Password": str})
    return pd.read_csv(file_name, dtype={"Customer_Phone": str})

def save_data(file_name, new_data):
    df = pd.DataFrame([new_data])
    df.to_csv(file_name, mode='a', header=False, index=False)

# Custom Colorful CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%); color: white !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .category-box { padding: 25px 15px; border-radius: 16px; background: #ffffff; text-align: center; margin-bottom: 20px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); transition: 0.3s; }
    .category-box:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3); border-color: #3b82f6; }
    .cat-icon { font-size: 40px; margin-bottom: 10px; display: block; }
    .cat-title { font-size: 15px; font-weight: 700; color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

if 'logged_in_partner' not in st.session_state:
    st.session_state['logged_in_partner'] = None

# ==========================================
# 2. APP NAVIGATION
# ==========================================
st.sidebar.title("📱 KuchhV Hub")
st.sidebar.write("---")
app_mode = st.sidebar.radio("Navigation Menu:", ["🏠 Customer App", "📢 Requirement Hub", "💼 Partner Portal", "⚙️ Admin Dashboard"])
st.sidebar.write("---")

# ==========================================
# 3. CUSTOMER APP (Categories & Direct Booking)
# ==========================================
if app_mode == "🏠 Customer App":
    st.title("🛒 KuchhV")
    st.markdown("### Har Zarurat, Ek Platform.")
    
    # Beautiful Category Grid
    st.write("---")
    st.subheader("🔥 Top Services Near You")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='category-box'><span class='cat-icon'>🍎</span><span class='cat-title'>Grocery & Retail</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='category-box'><span class='cat-icon'>🏠</span><span class='cat-title'>Real Estate</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='category-box'><span class='cat-icon'>🔧</span><span class='cat-title'>Home Repairs</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='category-box'><span class='cat-icon'>📄</span><span class='cat-title'>E-Gov & CSC</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='category-box'><span class='cat-icon'>💻</span><span class='cat-title'>IT Freelancers</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='category-box'><span class='cat-icon'>🏥</span><span class='cat-title'>Healthcare</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='category-box'><span class='cat-icon'>🚜</span><span class='cat-title'>Asset Rentals</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='category-box'><span class='cat-icon'>🛵</span><span class='cat-title'>Bike Taxi</span></div>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("⚡ Book a Direct Service")
    
    category_list = ["Grocery & Retail", "Home Repairs", "IT Freelancers", "Asset Rentals", "Bike Taxi", "Healthcare", "E-Gov & CSC", "Real Estate"]
    selected_category = st.selectbox("Category chunein:", category_list)
    
    partner_df = load_data(PARTNERS_FILE)
    available_partners = partner_df[(partner_df['Category'] == selected_category) & (partner_df['Verification_Status'] == 'Verified ✅')]
    
    if not available_partners.empty:
        st.success(f"✅ {len(available_partners)} Verified Partner(s) available!")
        st.dataframe(available_partners[['Business_Name', 'Category']], use_container_width=True)
        
        with st.form("book_service_form"):
            customer_phone = st.text_input("Enter your Mobile Number to Book:")
            requirement = st.text_area("Order Details:")
            if st.form_submit_button("Book Now"):
                new_order = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Customer_Phone": customer_phone,
                    "Category": selected_category,
                    "Requirement": requirement,
                    "Status": "Direct Order",
                    "Partner_Assigned": "Pending Acceptance"
                }
                save_data(ORDERS_FILE, new_order)
                st.success("Order Placed Successfully! Partner will contact you.")
    else:
        st.error("⚠️ Koi verified partner abhi is category me available nahi hai.")
        st.info("💡 **Tip:** Aap left menu se 'Requirement Hub' me jaakar apni demand post kar sakte hain.")

# ==========================================
# 4. REQUIREMENT HUB
# ==========================================
elif app_mode == "📢 Requirement Hub":
    st.title("📢 The Requirement Hub")
    st.info("💡 **Can't find a direct partner?** Post your custom requirement here and let local verified partners contact you.")
    
    with st.form("requirement_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            req_type = st.selectbox("Select Category", ["Bulk Labour/Manpower", "IT/Developer", "Event & Catering", "Logistics/Truck", "Other"])
            location = st.text_input("Pincode / City Area (e.g. 825401)")
        with col_b:
            phone = st.text_input("Your Mobile Number")
            
        description = st.text_area("Detail your exact requirement here:")
        
        submitted = st.form_submit_button("🚀 Broadcast to Local Partners")
        if submitted and description and location and phone:
            new_req = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Customer_Phone": phone,
                "Category": req_type,
                "Description": description,
                "Location": location,
                "Status": "Open"
            }
            save_data(REQUIREMENTS_FILE, new_req)
            st.success("✅ Request Broadcasted Successfully! Partners will contact you soon.")
            st.balloons()
        elif submitted:
            st.error("⚠️ Please fill in all details (Phone, Description, Location).")

# ==========================================
# 5. PARTNER PORTAL
# ==========================================
elif app_mode == "💼 Partner Portal":
    st.title("💼 Partner Business Portal")
    
    if st.session_state['logged_in_partner'] is None:
        tab_login, tab_signup = st.tabs(["🔐 Login", "📝 New Registration"])
        
        with tab_signup:
            st.subheader("Join the KuchhV Network")
            with st.form("signup_form"):
                phone = st.text_input("Mobile Number")
                password = st.text_input("Create Password", type="password")
                business_name = st.text_input("Business / Shop Name")
                category = st.selectbox("Category", ["Grocery & Retail", "Home Repairs", "IT Freelancers", "Asset Rentals", "Bike Taxi", "Healthcare", "E-Gov & CSC", "Real Estate"])
                
                if st.form_submit_button("Register"):
                    partner_df = load_data(PARTNERS_FILE)
                    if phone in partner_df['Phone'].values:
                        st.error("Yeh number pehle se registered hai! Login karein.")
                    else:
                        new_partner = {"Phone": phone, "Password": password, "Business_Name": business_name, "Category": category, "Verification_Status": "Pending"}
                        save_data(PARTNERS_FILE, new_partner)
                        st.success("Registration Successful! Awaiting Admin Approval.")
                        
        with tab_login:
            st.subheader("Partner Login")
            phone_login = st.text_input("Enter Mobile Number ")
            pass_login = st.text_input("Enter Password ", type="password")
            
            if st.button("Login"):
                partner_df = load_data(PARTNERS_FILE)
                user = partner_df[(partner_df['Phone'] == phone_login) & (partner_df['Password'] == pass_login)]
                
                if not user.empty:
                    status = user.iloc[0]['Verification_Status']
                    if status == 'Verified ✅':
                        st.session_state['logged_in_partner'] = user.iloc[0]['Business_Name']
                        st.success("Login Successful!")
                        st.rerun()
                    else:
                        st.error(f"Account Status: {status}. Admin approval pending.")
                else:
                    st.error("Galat Mobile Number ya Password.")
    else:
        st.success(f"Welcome, {st.session_state['logged_in_partner']}!")
        if st.button("Logout"):
            st.session_state['logged_in_partner'] = None
            st.rerun()
            
        st.subheader("Direct Orders for You")
        orders_df = load_data(ORDERS_FILE)
        st.dataframe(orders_df, use_container_width=True)
        
        st.subheader("Live Requirements (Hub)")
        req_df = load_data(REQUIREMENTS_FILE)
        st.dataframe(req_df, use_container_width=True)

# ==========================================
# 6. ADMIN DASHBOARD
# ==========================================
elif app_mode == "⚙️ Admin Dashboard":
    st.title("⚙️ Super Admin Center")
    
    partner_df = load_data(PARTNERS_FILE)
    
    st.subheader("Partner KYC & Verification")
    if not partner_df.empty:
        st.warning("⚠️ Action Required: Click on 'Verification_Status' below to approve or reject.")
        
        # Hide password column for admin view
        display_df = partner_df.drop(columns=['Password'])
        
        edited_partner_df = st.data_editor(
            display_df,
            column_config={
                "Verification_Status": st.column_config.SelectboxColumn(
                    "Status", options=["Pending", "Verified ✅", "Rejected ❌"], required=True
                )
            },
            use_container_width=True
        )
        if st.button("💾 Save Verification Status"):
            partner_df['Verification_Status'] = edited_partner_df['Verification_Status']
            partner_df.to_csv(PARTNERS_FILE, index=False)
            st.success("Status Updated Successfully!")
    else:
        st.info("No partners registered yet.")
