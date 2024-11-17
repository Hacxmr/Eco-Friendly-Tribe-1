import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.express as px

# Load datasets
fabric_url = "https://huggingface.co/datasets/infinite-dataset-hub/FabricFrontiers/resolve/main/data.csv"
fabric_df = pd.read_csv(fabric_url)
fashion_df = pd.read_csv("sustainable_fashion_trends_2024.csv")

# Title
st.title("🌿 Sustainable Fashion & Fabric Recommendation Dashboard")
st.write("Explore sustainable fabrics and fashion trends while getting recommendations based on your selections!")

# Sidebar Filters for Sustainable Fashion Trends
st.sidebar.header("Fashion Trends Filter")
selected_country = st.sidebar.selectbox(
    "Select a Country",
    options=sorted(fashion_df['Country'].unique()),
    index=sorted(fashion_df['Country'].unique()).index("USA")  # Default: USA
)
year_range = st.sidebar.slider(
    "Select Year Range",
    int(fashion_df['Year'].min()),
    int(fashion_df['Year'].max()),
    (int(fashion_df['Year'].min()), int(fashion_df['Year'].max()))
)

# Filter Fashion Trends Data
filtered_fashion_df = fashion_df[
    (fashion_df['Country'] == selected_country) &
    (fashion_df['Year'] >= year_range[0]) &
    (fashion_df['Year'] <= year_range[1])
]

# Preprocess Fabric Data
encoder = OneHotEncoder()
encoded_labels = encoder.fit_transform(fabric_df[['label']]).toarray()

text_data = fabric_df['title'] + " " + fabric_df['description']
vectorizer = TfidfVectorizer(max_features=100)
text_vectors = vectorizer.fit_transform(text_data).toarray()

df_prepared = np.hstack([encoded_labels, text_vectors])

# Set up FAISS
vector_dim = df_prepared.shape[1]
index = faiss.IndexFlatL2(vector_dim)
index.add(df_prepared.astype('float32'))

# Define function to query similar items
def query_similar_items(input_vector, top_k=5):
    input_vector = np.array(input_vector).astype('float32').reshape(1, -1)
    distances, indices = index.search(input_vector, top_k)
    recommendations = indices[0][1:]  # Skip the first match (itself)
    return recommendations

# Dropdown for fabric selection
st.sidebar.header("Fabric Recommendation System")
fabric_names = fabric_df['title'].unique()
selected_fabric = st.sidebar.selectbox("Select a Fabric:", fabric_names)

if selected_fabric:
    selected_item_index = fabric_df[fabric_df['title'] == selected_fabric].index[0]
    selected_item = fabric_df.iloc[selected_item_index]

    # Display selected fabric details
    st.subheader("Selected Fabric:")
    st.write("**Title**:", selected_item['title'])
    st.write("**Description**:", selected_item['description'])
    st.write("**Source**:", selected_item['source'])
    st.write("**Label**:", selected_item['label'])

    # Fabric recommendations
    st.subheader("Recommended Fabrics:")
    example_vector = df_prepared[selected_item_index]
    similar_items = query_similar_items(example_vector)

    for idx in similar_items:
        recommended_item = fabric_df.iloc[idx]
        st.write("**Title**:", recommended_item['title'])
        st.write("**Description**:", recommended_item['description'])
        st.write("**Source**:", recommended_item['source'])
        st.write("**Label**:", recommended_item['label'])
        st.write("---")

# Main Dashboard for Sustainable Fashion Trends
st.markdown(f"### Fashion Trends in {selected_country} ({year_range[0]} - {year_range[1]})")
st.dataframe(filtered_fashion_df)

# Visualizations for Fashion Trends
st.markdown("### Sustainability Ratings Distribution")
pie_chart = px.pie(
    filtered_fashion_df,
    names="Sustainability_Rating",
    title="Sustainability Ratings",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(pie_chart, use_container_width=True)

st.markdown("### Environmental Impact by Brand")
bar_chart = px.bar(
    filtered_fashion_df,
    x="Brand_Name",
    y=["Carbon_Footprint_MT", "Water_Usage_Liters"],
    barmode="group",
    title="Carbon Footprint and Water Usage",
    labels={"value": "Impact Value", "variable": "Impact Metric"},
    color_discrete_sequence=px.colors.qualitative.Vivid
)
st.plotly_chart(bar_chart, use_container_width=True)

st.markdown("### Market Trend Analysis")
scatter_plot = px.scatter(
    filtered_fashion_df,
    x="Average_Price_USD",
    y="Market_Trend",
    size="Waste_Production_KG",
    color="Material_Type",
    title="Market Trends by Material Type",
    hover_data=["Brand_Name", "Certifications"],
    size_max=20,
    color_discrete_sequence=px.colors.qualitative.Prism
)
st.plotly_chart(scatter_plot, use_container_width=True)

# Check if selected fabric is sustainable
st.markdown("### Sustainability Check")
if selected_fabric:
    sustainable_brands = filtered_fashion_df['Brand_Name'].unique()
    if any(selected_item['source'] in brand for brand in sustainable_brands):
        st.success(f"The selected fabric '{selected_item['title']}' is linked to sustainable practices!")
    else:
        st.warning(f"The selected fabric '{selected_item['title']}' might not align with sustainability practices.")

# Download filtered fashion data
st.markdown("### Download Filtered Fashion Data")
csv = filtered_fashion_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="filtered_fashion_trends.csv",
    mime="text/csv"
)

# Sidebar Insights
st.sidebar.header("Insights")
if not filtered_fashion_df.empty:
    total_brands = len(filtered_fashion_df['Brand_Name'].unique())
    avg_price = filtered_fashion_df['Average_Price_USD'].mean()
    avg_carbon_footprint = filtered_fashion_df['Carbon_Footprint_MT'].mean()
    
    st.sidebar.markdown(f"**Total Brands:** {total_brands}")
    st.sidebar.markdown(f"**Avg Price (USD):** ${avg_price:.2f}")
    st.sidebar.markdown(f"**Avg Carbon Footprint (MT):** {avg_carbon_footprint:.2f}")
else:
    st.sidebar.markdown("No data available for selected filters.")

# Footer
st.markdown("---")
st.markdown("Dashboard created with ❤️ using Streamlit.")
