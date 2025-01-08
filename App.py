import streamlit as st
import pandas as pd
from POC_3011 import execute_queries, create_agent, load_data

# Streamlit App Configuration
st.title("TB-Fraud")
st.header("Estimate the Impact of AI Technology in Fighting Tax Fraud")
st.subheader("Powered by FacultyAI and TBI")

# File Upload for Queries
queries_file = st.file_uploader("Upload a Queries.txt file", type=["txt"])

if queries_file:
    # Read file content
    file_content = queries_file.read().decode("utf-8")
    st.write("### Content of Queries.txt")
    st.text_area("File Content", file_content, height=300)

    # Load data files
    ai_file = "R1.simple_AI.xlsx"
    no_ai_file = "R1.simple_NO_AI.xlsx"
    df_ai = load_data(ai_file)
    df_no_ai = load_data(no_ai_file)

    # Define context and create agent
    context = """
    You are an AI assistant specializing in financial data analysis and fraud detection.
    You have access to two datasets:
    - Dataset 1 (AI): This dataset simulates the use of AI technology in detecting tax fraud, including detailed metrics.
    - Dataset 2 (No AI): This dataset reflects traditional methods without AI involvement.

    Your goal is to provide insights into the differences in fraud detection efficiency between the two approaches.
    Specifically:
    1. Compare key metrics such as fraud detection rates and error margins.
    2. Provide high-level summaries and statistical analyses.
    3. Answer user queries to help stakeholders understand the impact of AI on fraud reduction.
    """
    api_key = st.secrets["OPENAI_API_KEY"]  # Use secrets for API keys
    agent = create_agent(context, [df_ai, df_no_ai], api_key)

    # Process queries
    queries = file_content.splitlines()
    with st.spinner("Processing queries..."):
        results = execute_queries(agent, queries)

    # Display results in a DataFrame
    df_results = pd.DataFrame(dict([(query, pd.Series(data)) for query, data in results.items()]))
    st.write("### Query Results")
    st.dataframe(df_results)

    # Downloadable results
    output_file = "query_results_as_columns.xlsx"
    df_results.to_excel(output_file, index=False)
    with open(output_file, "rb") as f:
        st.download_button(
            label="Download Excel Results",
            data=f,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.warning("Please upload a 'Queries.txt' file to view its content and process queries.")

