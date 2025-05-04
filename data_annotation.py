import streamlit as st
import pandas as pd
import os

#app title
st.title("Data Annotation App")

#file/dataset upload
file_upload = st.file_uploader("Upload your file",type=["csv"])
if file_upload is not None:
    startup_df = pd.read_csv(file_upload)

#to have the user select the column to annotate
column_pick = st.selectbox("Select text column",startup_df.columns)

#create the annotation storage
if "annotations" not in st.session_state:
    st.session_state.annotations = {}

# Display one row at a time for annotation
index = st.number_input("Go to row number", min_value=0, max_value=len(startup_df)-1, step=1)
words = startup_df.loc[index, column_pick]

#Words to annotate
st.subheader("Words to Annotate")
st.write(words)

#multiselect keywords
keywords = st.text_input("Enter word/label to tag").split(",")
selected_keywords = [k.strip() for k in keywords if k.strip() in words]

st.write("Detected keyword in text:", selected_keywords)

#save annotation
if st.button("Save Annotation"):
    st.session_state.annotations[index] = selected_keywords
    st.success("Annotation saved")

 # Download annotations
    if st.button("Download Annotations"):
        annotated_df = pd.DataFrame([
            {"Row": k, "Text": startup_df.loc[k, column_pick], "Annotations": v}
            for k, v in st.session_state.annotations.items()
        ])

         # Save to a local file
        output_path = "saved_annotations.csv"
        annotated_df.to_csv(output_path, index=False)

        st.success(f"Annotations saved locally at: {os.path.abspath(output_path)}")
        st.write("Current working directory:", os.getcwd())

        st.download_button("Download CSV", data=annotated_df.to_csv(index=False), file_name="annotations.csv")

    # Show existing annotations
    if st.checkbox("Show All Annotations"):
        st.write(st.session_state.annotations)