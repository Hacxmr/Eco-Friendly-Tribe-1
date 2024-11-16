import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
df = pd.read_csv("sustainable_fashion_trends_2024.csv")

# Page title
st.title("🌿 Sustainable Fashion Trends Dashboard")

# Sidebar filters
st.sidebar.header("Filter Data")
selected_country = st.sidebar.selectbox(
    "Select a Country",
    options=sorted(df['Country'].unique()),
    index=sorted(df['Country'].unique()).index("USA")  # Default: "USA"
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['Year'].min()),
    int(df['Year'].max()),
    (int(df['Year'].min()), int(df['Year'].max()))
)

# Filter data based on user input
filtered_df = df[(df['Country'] == selected_country) &
                 (df['Year'] >= year_range[0]) &
                 (df['Year'] <= year_range[1])]

# Main Dashboard
st.markdown(f"### Data Overview for {selected_country} ({year_range[0]} - {year_range[1]})")
st.dataframe(filtered_df)

# Pie chart for Sustainability Ratings
st.markdown("### Distribution of Sustainability Ratings")
pie_chart = px.pie(
    filtered_df,
    names="Sustainability_Rating",
    title="Sustainability Ratings Distribution",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(pie_chart, use_container_width=True)

# Bar chart for Carbon Footprint and Water Usage
st.markdown("### Environmental Impact by Brand")
bar_chart = px.bar(
    filtered_df,
    x="Brand_Name",
    y=["Carbon_Footprint_MT", "Water_Usage_Liters"],
    barmode="group",
    title="Carbon Footprint and Water Usage",
    labels={"value": "Impact Value", "variable": "Impact Metric"},
    color_discrete_sequence=px.colors.qualitative.Vivid
)
st.plotly_chart(bar_chart, use_container_width=True)

# Scatter plot for Market Trend Analysis
st.markdown("### Market Trend Analysis")
scatter_plot = px.scatter(
    filtered_df,
    x="Average_Price_USD",
    y="Market_Trend",
    size="Waste_Production_KG",
    color="Material_Type",
    title="Market Trends Based on Material Type",
    hover_data=["Brand_Name", "Certifications"],
    size_max=20,
    color_discrete_sequence=px.colors.qualitative.Prism
)
st.plotly_chart(scatter_plot, use_container_width=True)

# Download filtered data
st.markdown("### Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="filtered_sustainable_fashion_data.csv",
    mime="text/csv"
)

# Add interactive insights
st.sidebar.header("Insights")
if not filtered_df.empty:
    total_brands = len(filtered_df['Brand_Name'].unique())
    avg_price = filtered_df['Average_Price_USD'].mean()
    avg_carbon_footprint = filtered_df['Carbon_Footprint_MT'].mean()
    
    st.sidebar.markdown(f"**Total Brands:** {total_brands}")
    st.sidebar.markdown(f"**Avg Price (USD):** ${avg_price:.2f}")
    st.sidebar.markdown(f"**Avg Carbon Footprint (MT):** {avg_carbon_footprint:.2f}")
else:
    st.sidebar.markdown("No data available for selected filters.")

# Footer
st.markdown("---")
st.markdown("Dashboard created with ❤️ using Streamlit.")
