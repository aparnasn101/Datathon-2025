# ------------------------------
# 11) SIDEBAR: MONTHLY REVIEWS (May–October)
# ------------------------------
st.sidebar.header("📅 Monthly Shipment Reviews")

# Normalize column names
shipments.columns = [c.strip().lower().replace(" ", "_") for c in shipments.columns]

months = ["May", "June", "July", "August", "September", "October"]

for month in months:
    st.sidebar.subheader(f"Monthly Review: {month}")
    st.sidebar.markdown(f"**Start Date:** {month} 1, 2025")
    
    # Loop through all ingredients in shipment file
    for _, row in shipments.iterrows():
        ingredient = row.get("ingredient", "Unknown Ingredient")
        freq = str(row.get("frequency", "Unknown")).capitalize()
        qty = row.get("quantity_per_shipment", "N/A")
        unit = row.get("unit_of_shipment", "")
        est_supply = row.get("estimated_weekly_supply", "N/A")
        total_recv = row.get("total_received", "N/A")
        
        # Calculate next restock based on frequency
        start_date = pd.to_datetime(f"2025-{month}-01", errors="coerce")
        if "week" in freq.lower():
            interval = 7
        elif "biweek" in freq.lower():
            interval = 14
        elif "month" in freq.lower():
            interval = 30
        else:
            interval = 14  # fallback

        next_restock = start_date + pd.Timedelta(days=interval)
        next_restock_str = next_restock.strftime("%B %d, %Y")
        
        # Bullet point summary per ingredient
        st.sidebar.markdown(f"""
        • **{ingredient}**  
            - Restocked: {freq}  
            - Next restock due: {next_restock_str}  
            - Quantity per shipment: {qty} {unit}  
            - Estimated weekly supply: {est_supply}  
            - Total received this cycle: {total_recv}
        """)
    
    st.sidebar.markdown("---")




