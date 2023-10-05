from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import tempfile


def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    # configure the look of the page
    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

    # as for the CSV file to analyse
    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    # create a temp file to perform analysis on 
    if csv_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".csv") 
        tfile.write(csv_file.getvalue())
        tfile.close() 
        # this si the OPENAI agent that performs the processing
        agent = create_csv_agent(
            OpenAI(temperature=0), tfile.name, verbose=True)

        #prompt the user for a question
        user_question = st.text_input("Ask a question about your CSV: ")

        #answer the user question
        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                st.write(agent.run(user_question))


if __name__ == "__main__":
    main()