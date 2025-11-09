# ------------------------------
# 10) SIDEBAR: INGREDIENTS RUNNING LOW
# ------------------------------
st.sidebar.header("⚠️ Ingredients Running Low")

if len(valid_cols) == 0:
    st.sidebar.info("No valid ingredients available to check.")
else:
    # Pick the last month (October in your dataset)
    last_month = months_in_data[-1]
    current_data = monthly_totals[monthly_totals["Month"] == last_month]

    # Compute max per ingredient across all months
    max_per_ing = monthly_totals[valid_cols].max()
    current_vals = current_data[valid_cols].iloc[0]

    # Calculate percentage remaining
    percent_remaining = (current_vals / max_per_ing) * 100
    low_ingredients = percent_remaining[percent_remaining <= 25]  # ≤ 25% of max

    if low_ingredients.empty:
        st.sidebar.success("✅ No ingredients currently running low!")
    else:
        st.sidebar.warning(f"{len(low_ingredients)} ingredients running low.")
        
        # Horizontal bar plot for low ingredients
        fig_low, ax_low = plt.subplots(figsize=(5, len(low_ingredients) * 0.4))
        ax_low.barh(low_ingredients.index, low_ingredients.values, color="salmon")
        ax_low.set_xlabel("% Remaining")
        ax_low.set_title(f"Ingredients Running Low - {last_month}")
        plt.tight_layout()
        st.sidebar.pyplot(fig_low)


# ------------------------------
# 11) SIDEBAR: RESTOCK RECOMMENDATIONS (SHIPMENT FILE)
# ------------------------------
st.sidebar.header("📦 Restock Recommendations")

try:
    shipment_df = shipments.copy()
    shipment_df.columns = shipment_df.columns.str.strip()

    # Normalize column names
    col_map = {
        "Ingredient": "Ingredient",
        "Last Shipment": "Last Shipment",
        "Amount Received": "Amount Received",
        "Frequency": "Frequency"
    }
    shipment_df = shipment_df.rename(columns={k: v for k, v in col_map.items() if k in shipment_df.columns})

    # Safety check
    required_cols = ["Ingredient", "Last Shipment", "Amount Received", "Frequency"]
    if not all(c in shipment_df.columns for c in required_cols):
        st.sidebar.error(f"Shipment file missing columns. Expected: {required_cols}")
    else:
        # Compute usage for the latest month (same last_month as above)
        latest_usage = monthly_totals[monthly_totals["Month"] == last_month][valid_cols].iloc[0]

        alerts = []
        for _, row in shipment_df.iterrows():
            ing = row["Ingredient"]
            if ing not in latest_usage:
                continue  # skip ingredients not tracked in monthly_totals

            received = row["Amount Received"]
            used = latest_usage[ing]
            remaining_pct = max(0, 100 - (used / received * 100)) if received > 0 else 0

            # classify timing
            if remaining_pct <= 25:
                timing = "Week 4 (urgent restock)"
            elif remaining_pct <= 50:
                timing = "Week 3 (moderate restock)"
            else:
                timing = "Sufficient this month"

            alerts.append({
                "Ingredient": ing,
                "Frequency": row["Frequency"],
                "Amount Received": received,
                "Remaining %": round(remaining_pct, 1),
                "Timing": timing
            })

        if len(alerts) == 0:
            st.sidebar.info("✅ All ingredients are currently within normal restock levels.")
        else:
            st.sidebar.markdown("Every two weeks, review these restock suggestions:")
            for a in alerts:
                st.sidebar.markdown(
                    f"""
                    **🧂 {a['Ingredient']}**
                    - Frequency: {a['Frequency']}
                    - Amount received: {a['Amount Received']}
                    - Remaining stock: {a['Remaining %']}% of last shipment
                    - Recommended restock: *{a['Timing']}*
                    - Timestamp: *third week of the month*
                    """
                )

except Exception as e:
    st.sidebar.error(f"Error processing shipment file: {e}")

