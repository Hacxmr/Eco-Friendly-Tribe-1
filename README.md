# Eco-Friendly Fabric Recommendation System

This project is a fabric recommendation system that helps users find eco-friendly and sustainable fabric options by suggesting similar fabrics based on an initial selection. The recommendation system is powered by FAISS (Facebook AI Similarity Search), and it uses Streamlit for an interactive frontend experience.

This system is a part of the [Eco-Friendly Tribe]([https://github.com/Hacxmr/Eco-Friendly-Tribe](https://hacxmr-eco-friendly-tribe-1-sustainable-fabric-dashboard-azfixm.streamlit.app/)) project, which aims to promote sustainable fabric choices.

![Eco-Friendly Fabric Recommendation System](https://github.com/Hacxmr/Eco-Friendly-Tribe/blob/main/fabric_recomm.jpg)

## Features

- **Fabric Selection**: Users can choose a fabric from a dropdown menu to find similar fabrics.
- **Text Vectorization**: Uses TF-IDF to transform fabric titles and descriptions into numerical vectors.
- **Label Encoding**: One-hot encodes categorical labels.
- **Similarity Search**: Utilizes FAISS to find and recommend fabrics similar to the selected one.

## Dataset

The dataset used is [FabricFrontiers](https://huggingface.co/datasets/infinite-dataset-hub/FabricFrontiers), a CSV file with columns like `idx`, `title`, `description`, `source`, and `label`.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Hacxmr/Eco-Friendly-Tribe.git
    cd Eco-Friendly-Tribe
    ```

2. Install the required dependencies:

    ```bash
    pip install streamlit pandas faiss-cpu scikit-learn numpy
    ```

## Usage

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
