#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

# Function to load data from supported file formats
def load_data(file_path):
    """
    Load data from a file into a pandas DataFrame.

    Args:
        file_path (str): Path to the file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    file_formats = {
        "csv": pd.read_csv,
        "xls": pd.read_excel,
        "xlsx": pd.read_excel,
        "xlsm": pd.read_excel,
        "xlsb": pd.read_excel,
    }
    
    try:
        ext = file_path.split(".")[-1].lower()
        if ext in file_formats:
            return file_formats[ext](file_path).fillna('')
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        raise IOError(f"Failed to load data: {e}")

# Function to create a LangChain agent
def create_agent(context, df_list, api_key):
    """
    Create a pandas DataFrame agent for querying data.

    Args:
        context (str): The instructions for the agent.
        df_list (list): List of DataFrames for querying.
        api_key (str): API key for the language model.

    Returns:
        pandas_df_agent: Configured agent instance.
    """
    llm = ChatOpenAI(
        temperature=0, model="gpt-4o", openai_api_key=api_key
    )
    return create_pandas_dataframe_agent(
        llm,
        df_list,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True,
        max_iterations=100,
        max_execution_time=10000,
        prefix=context,
    )

# Main function to execute queries
def execute_queries(agent, queries):
    """
    Execute a list of queries on the LangChain agent.

    Args:
        agent: LangChain agent instance.
        queries (list): List of queries.

    Returns:
        dict: Results for each query.
    """
    results = {}
    for query in queries:
        try:
            result = agent.invoke(query)
            results[query] = result if isinstance(result, list) else [result]
        except Exception as e:
            results[query] = [str(e)]
    return results

# Example usage (encapsulate actual implementation in __main__):
if __name__ == "__main__":
    # Sample data files
    ai_file = "R1.simple_AI.xlsx"
    no_ai_file = "R1.simple_NO_AI.xlsx"

    # Load data
    df_ai = load_data(ai_file)
    df_no_ai = load_data(no_ai_file)

    # Define the context
    context = """Instructions... (Add full context details here)."""

    # Create the agent
    api_key = os.getenv("OPENAI_API_KEY")  # Ensure the key is set in the environment
    agent = create_agent(context, [df_ai, df_no_ai], api_key)

    # Queries from user input
    queries = ["Provide a summary of tax revenues."]

    # Execute queries
    results = execute_queries(agent, queries)

    # Display results
    for query, response in results.items():
        print(f"Query: {query}\nResponse: {response}")

