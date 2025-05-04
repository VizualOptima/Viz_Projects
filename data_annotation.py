import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#app title
st.title("Data Annotation App")

#file/dataset upload
file_upload = st.file_uploader("Upload your file",type=["csv"])
if file_upload is not None:
    startup_df = pd.read_csv(file_upload)

#to have the user select the column to annotate
column_pick = st.multiselect("Select text column",startup_df.columns)

if not column_pick:
    st.warning("Please select at least one column.")
else:
    st.success(f"Annotating the following column(s): {', '.join(column_pick)}")

# #create the annotation storage
# if "annotations" not in st.session_state:
#     st.session_state.annotations = {}

#to enter keywords/labels
st.subheader("Keywords and label tags")
keywords = st.text_input("E.g : AI, blockchain,finance").split(",")
keywords = [word.strip().lower() for word in keywords if word.strip()]

#Annotation

st.subheader("Annotation")

if st.button("Annotate Columns"):
    def row_has_keyword(row):
        return any(
            any(word in str(row[col]).lower() for word in keywords)
            for col in column_pick
        )
    startup_df["contains_keyword"] = startup_df.apply(row_has_keyword,axis=1)

    annotated_df = startup_df[startup_df["contains_keyword"]==True]
    st.session_state.annotated_df = annotated_df

    st.success("Annotations applied across selected columns")

 # Download annotated data
st.subheader("Download Data")
if "annotated_df" in st.session_state and not st.session_state.annotated_df.empty:    
    st.download_button(
            label="Download Annotated Data",
            data=st.session_state.annotated_df.to_csv(index=False),
            file_name="annotated_startups_multi_column.csv"
        )
else: st.info("No annotated data available yet. Please run annotation first.")

st.subheader("Charts")

industry_counts = (
        annotated_df[Industry]
        .value_counts()
        .sort_values(ascending=False)
    )

st.write(industry_counts)
st.bar_chart(industry_counts)

scatter_df = annotated_df[[Industry, year_col]].dropna()

fig, ax = plt.subplots()
ax.scatter(scatter_df[year_col], scatter_df[industry_col].astype(str))
ax.set_xlabel("Year Founded")
ax.set_ylabel("Industry")
ax.set_title("Tagged Startups by Year and Industry")
st.pyplot(fig)