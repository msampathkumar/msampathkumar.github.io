import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(layout="wide")

# File path for the CSV
CSV_FILE = "models.csv"


# Load the data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_FILE)
        int_columns = ["input_max_tokens", "output_max_tokens"]
        for col in int_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        return df
    except FileNotFoundError:
        return pd.DataFrame()


# Save the data
def save_data(df):
    df.to_csv(CSV_FILE, index=False)


# Main app
def main():
    st.title("Model CSV Editor")

    # Load the data
    df = load_data()

    # Display the data editor
    st.info("Edit the data below and click 'Save Changes' to update the CSV file.")
    edited_df = st.data_editor(df, num_rows="dynamic")

    # Save button
    if st.button("Save Changes"):
        save_data(edited_df)
        st.success("Changes saved successfully!")
        # st.experimental_rerun()


if __name__ == "__main__":
    main()
