import streamlit as st
import pandas as pd
import queries as q
from crud import *

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("🍽 Local Food Wastage Management System")
page = st.sidebar.radio("Pages: ", ["Home", "Providers", "Receivers", "Food Listings", "Claims", "Analysis"])

# -------------------------
# Home Page
# -------------------------
if page == "Home":
    st.title("🍽 Local Food Wastage Management System")
    st.write("""
    This app connects surplus food providers (restaurants, grocery stores, etc.) 
    with NGOs and individuals in need.  
    Built with **Python, SQL, and Streamlit**.
    """)
    st.success("✅ Use the sidebar to navigate to Providers, Receivers, Food Listings, Claims, or Analysis.")

# -------------------------
# Providers Page
# -------------------------
elif page == "Providers":
    st.title("📦 Manage Providers")

    # Add Provider
    with st.expander("➕ Add Provider"):
        with st.form("add_provider_form"):
            pid = st.number_input("Provider ID", min_value=1, step=1)
            name = st.text_input("Name")
            type_ = st.selectbox("Type", ["Restaurant", "Grocery Store", "Supermarket"])
            address = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submit = st.form_submit_button("Add Provider")

            if submit:
                add_provider(pid, name, type_, address, city, contact)
                st.success(f"✅ Provider {name} added successfully!")

    # Get Provider by ID
    with st.expander("🔍 Get Provider by ID"):
        provider_id_input = st.text_input("Enter Provider ID:")
        if st.button("Get Provider"):
            if provider_id_input:
                provider = get_provider_by_id(provider_id_input)
                if provider:
                    df = pd.DataFrame([provider], columns=["Provider_ID", "Name", "Type", "Address", "City", "Contact"])
                     # Make contact clickable (email or phone)
                    df["Contact"] = df["Contact"].apply(
                    lambda x: f"[{x}](mailto:{x})" if "@" in str(x) else f"[{x}](tel:{x})")
                    st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)
            else:
                st.error("❌ No provider found with that ID")

    # View All Providers
    with st.expander("📋 All Providers"):
        providers = get_providers()
        df = pd.DataFrame(providers, columns=["Provider_ID", "Name", "Type", "Address", "City", "Contact"])
        st.dataframe(df)
    
    # Update Provider
    with st.expander("✏️ Update Provider"):
        with st.form("update_provider_form"):
            u_pid = st.number_input("Provider ID to Update", min_value=1, step=1)
            new_city = st.text_input("New City")
            new_contact = st.text_input("New Contact")
            update_submit = st.form_submit_button("Update")

            if update_submit:
                update_provider(u_pid, City=new_city, Contact=new_contact)
                st.success(f"✅ Provider {u_pid} updated successfully!")

    # Delete Provider
    with st.expander("🗑️ Delete Provider"):
        with st.form("delete_provider_form"):
            d_pid = st.number_input("Provider ID to Delete", min_value=1, step=1)
            delete_submit = st.form_submit_button("Delete")

            if delete_submit:
                delete_provider(d_pid)
                st.warning(f"⚠️ Provider {d_pid} deleted!")

# -------------------------
# Receivers Page
# -------------------------
elif page == "Receivers":
    st.title("👥 Manage Receivers")

    # Add Receiver
    with st.expander("➕ Add Receiver"):

        with st.form("add_receiver_form"):
            rid = st.number_input("Receiver ID", min_value=1, step=1)
            name = st.text_input("Name")
            type_ = st.text_input("Type")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submit = st.form_submit_button("Add Receiver")

            if submit:
                add_receiver(rid, name, type_, city, contact)
                st.success(f"✅ Receiver {name} added successfully!")

    # Get Receiver by ID
    with st.expander("🔍 Get Receiver by ID"):
        receiver_id_input = st.text_input("Enter Receiver ID:")
        if st.button("Get Receiver"):
            if receiver_id_input:
                receiver = get_receiver_by_id(receiver_id_input)
                if receiver:
                    df = pd.DataFrame([receiver], columns=["Receiver_ID", "Name", "Type", "City", "Contact"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("❌ No receiver found with that ID")

    # View All Receivers
    with st.expander("📋 All Receivers"):
        receivers = get_receivers()
        if receivers:
            df = pd.DataFrame(receivers, columns=["Receiver_ID", "Name", "Type", "City", "Contact"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No receivers found.")

    # Update Receiver
    with st.expander("✏️ Update Receiver"):
        with st.form("update_receiver_form"):
            u_rid = st.number_input("Receiver ID to Update", min_value=1, step=1)
            new_city = st.text_input("New City")
            new_contact = st.text_input("New Contact")
            update_submit = st.form_submit_button("Update")

            if update_submit:
                update_receiver(u_rid, City=new_city, Contact=new_contact)
                st.success(f"✅ Receiver {u_rid} updated successfully!")

    # Delete Receiver
    with st.expander("🗑️ Delete Receiver"):
        with st.form("delete_receiver_form"):
            d_rid = st.number_input("Receiver ID to Delete", min_value=1, step=1)
            delete_submit = st.form_submit_button("Delete")

            if delete_submit:
                delete_receiver(d_rid)
                st.warning(f"⚠️ Receiver {d_rid} deleted!")

# -------------------------
# Food Listings Page
# -------------------------
elif page == "Food Listings":
    st.title("🍽 Manage Food Listings")
    # View All Food Listings with Filters

    with st.expander("📋 All Food Listings (with Filters)"):
        foods = get_food_listings()
        if foods:
            df = pd.DataFrame(foods, columns=[
                "Food_ID", "Food_Name", "Quantity", "Expiry_Date",
                "Provider_ID", "Provider_Type", "Location", "Food_Type", "Meal_Type"
            ])
    
            # --- Filters ---
            col1, col2, col3 = st.columns(3)
    
            with col1:
                   location_filter = st.selectbox("Filter by Location", ["All"] + sorted(df["Location"].unique().tolist()))
    
            with col2:
               provider_filter = st.number_input("Enter Provider ID (leave 0 for All)", min_value=0, step=1, value=0)
           
            with col3:
                food_type_filter = st.selectbox("Filter by Food Type", ["All"] + sorted(df["Food_Type"].unique().tolist()))
    
            # --- Apply filters ---
            if location_filter != "All":
                df = df[df["Location"] == location_filter]
            if provider_filter != 0:
                df = df[df["Provider_ID"] == provider_filter]
            if food_type_filter != "All":
                df = df[df["Food_Type"] == food_type_filter]
    
            st.dataframe(df, use_container_width=True)
    
        else:
            st.info("No food listings found.")
    
    # Add Food Listing
    with st.expander("➕ Add Food Listing"):
        with st.form("add_food_form"):
            fid = st.number_input("Food ID", min_value=1, step=1)
            provider_id = st.number_input("Provider ID", min_value=1, step=1)
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity (kg)", min_value=1, step=1)
            expiry = st.date_input("Expiry Date")
            submit = st.form_submit_button("Add Food Listing")

            if submit:
                add_food(fid, food_name, quantity, expiry, provider_id, "Unknown", "Unknown", "Unknown", "Unknown")
                st.success(f"✅ Food '{food_name}' added successfully!")

    # Get Food by ID
    with st.expander("🔍 Get Food by ID"):
        food_id_input = st.text_input("Enter Food ID:")
        if st.button("Get Food"):
            if food_id_input:
                food = get_food_by_id(food_id_input)
                if food:
                    df = pd.DataFrame([food], columns=[
                        "Food_ID", "Food_Name", "Quantity", "Expiry_Date",
                        "Provider_ID", "Provider_Type", "Location", "Food_Type", "Meal_Type"
                    ])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("❌ No food found with that ID")

    # View All Food Listings
    with st.expander("📋 All Food Listings"):
        foods = get_food_listings()
        if foods:
            df = pd.DataFrame(foods, columns=[
                "Food_ID", "Food_Name", "Quantity", "Expiry_Date",
                "Provider_ID", "Provider_Type", "Location", "Food_Type", "Meal_Type"
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No food listings found.")

    # Update Food Listing
    with st.expander("✏️ Update Food Listing"):        
        with st.form("update_food_form"):
            u_fid = st.number_input("Food ID to Update", min_value=1, step=1)
            new_quantity = st.number_input("New Quantity (kg)", min_value=1, step=1)
            new_expiry = st.date_input("New Expiry Date")
            update_submit = st.form_submit_button("Update")

            if update_submit:
                update_food(u_fid, Quantity=new_quantity, Expiry_Date=new_expiry)
                st.success(f"✅ Food Listing {u_fid} updated successfully!")

    # Delete Food Listing
    with st.expander("🗑️ Delete Food Listing"):           
        with st.form("delete_food_form"):
            d_fid = st.number_input("Food ID to Delete", min_value=1, step=1)
            delete_submit = st.form_submit_button("Delete")
            if delete_submit:
                delete_food(d_fid)
                st.warning(f"⚠️ Food Listing {d_fid} deleted!")

# -------------------------
# Claims Page
# -------------------------
elif page == "Claims":
    st.title("📜 Manage Claims")

    # Add Claim
    with st.expander("➕ Add Claim"):        
        with st.form("add_claim_form"):
            cid = st.number_input("Claim ID", min_value=1, step=1)
            rid = st.number_input("Receiver ID", min_value=1, step=1)
            fid = st.number_input("Food ID", min_value=1, step=1)
            status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
            submit = st.form_submit_button("Add Claim")

            if submit:
                add_claim(cid, fid, rid, status, "2025-01-01")  # Example timestamp
                st.success(f"✅ Claim {cid} added successfully!")

    # Get Claim by ID
    with st.expander("🔍 Get Claim by ID"):        
        claim_id_input = st.text_input("Enter Claim ID:")
        if st.button("Get Claim"):
            if claim_id_input:
                claim = get_claim_by_id(claim_id_input)
                if claim:
                    df = pd.DataFrame([claim], columns=["Claim_ID", "Food_ID", "Receiver_ID", "Status", "Timestamp"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("❌ No claim found with that ID")

    # View All Claims
    with st.expander("📋 All Claims"):          
        claims = get_claims()
        if claims:
            df = pd.DataFrame(claims, columns=["Claim_ID", "Food_ID", "Receiver_ID", "Status", "Timestamp"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No claims found.")

    # Update Claim
    with st.expander("✏️ Update Claim"):                  
        with st.form("update_claim_form"):
            u_cid = st.number_input("Claim ID to Update", min_value=1, step=1)
            new_status = st.selectbox("New Status", ["Pending", "Approved", "Rejected"])
            update_submit = st.form_submit_button("Update")

            if update_submit:
                update_claim(u_cid, Status=new_status)
                st.success(f"✅ Claim {u_cid} updated successfully!")

    # Delete Claim
    with st.expander("🗑️ Delete Claim"):                  
        with st.form("delete_claim_form"):
            d_cid = st.number_input("Claim ID to Delete", min_value=1, step=1)
            delete_submit = st.form_submit_button("Delete")

            if delete_submit:
                delete_claim(d_cid)
                st.warning(f"⚠️ Claim {d_cid} deleted!")

# -------------------------
# Analysis Page (Queries)
# -------------------------
elif page == "Analysis":
    st.title("📊 Food Wastage Analysis")

    with st.expander(" 1️⃣. Providers per City"):
        st.dataframe(q.providers_per_city())

    with st.expander(" 2️⃣. Receivers per City"):
        st.dataframe(q.receivers_per_city())

    with st.expander(" 3️⃣. Top Provider Types (by Total Quantity Donated)"):
        st.dataframe(q.top_provider_types())

    with st.expander(" 4️⃣. Provider Contacts by City"):
        city_input = st.text_input("Enter city for provider contacts:")
        if city_input:
            st.dataframe(q.provider_contacts_by_city(city_input))

    with st.expander(" 5️⃣. Top Receivers (by Claims)"):
        st.dataframe(q.top_receivers(limit=10))

    with st.expander(" 6️⃣.Total Food Available"):
        st.dataframe(q.total_food_available())

    with st.expander(" 7️⃣. City with Most Food Listings"):
        st.dataframe(q.city_with_most_listings())

    with st.expander(" 8️⃣. Common Food Types"):
        st.dataframe(q.common_food_types())

    with st.expander(" 9️⃣. Claims per Food"):
        st.dataframe(q.claims_per_food(limit=10))

    with st.expander(" 🔟. Top Successful Provider (Completed Claims)"):
        st.dataframe(q.top_successful_provider())

    with st.expander(" 1️⃣1️⃣. Claim Status Distribution (%)"):
        st.dataframe(q.claim_status_percentage())

    with st.expander(" 1️⃣2️⃣. Average Quantity Claimed per Receiver"):
        st.dataframe(q.avg_quantity_per_receiver(limit=10))

    with st.expander(" 1️⃣3️⃣. Most Claimed Meal Type"):
        st.dataframe(q.most_claimed_meal_type())

    with st.expander(" 1️⃣4️⃣. Total Donated per Provider"):
        st.dataframe(q.total_donated_per_provider(limit=10))

    with st.expander(" 1️⃣5️⃣. Top Donated Foods"):
        st.dataframe(q.top_donated_foods(limit=5))