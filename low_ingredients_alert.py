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

