The Excel Agent implements a Langchain Agent for the manipulationn of structured data using plain (English) language. 
The TBFraud function in the POC.py file is embedded in a Streamlit application, App.py, allowing the access from an internet server.
Structured data is extracted from Excel files and loaded into pandas dataframes. 
The TBFraud function passes the relevant information about the files using context message and requires to the LLm to write a Python code in order to proviude a compelling answer to the queries of the user (loaded in a "Queries.txt" file).
Answers are then saved into a downloadable Excel file.
Tests included: Data Extraction, data simple manipulation, calculation of new quantities not previously present in the original dataframe,
update of key parameters used for the generation of the data included in the dataframe and followed by recalculation of relevant quantities,
comparison between quantities extracted from 2 dataframes.
