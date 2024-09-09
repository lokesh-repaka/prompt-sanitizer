import streamlit as st
from llm_guard import scan_prompt
from llm_guard.input_scanners import Anonymize, PromptInjection
from llm_guard.output_scanners import Deanonymize, Sensitive
from llm_guard.vault import Vault

# Initialize vault
vault = Vault()

# Define input and output scanners
input_scanners = [Anonymize(vault), PromptInjection()]

# Default prompt
default_prompt = (
    "Make an SQL insert statement to add a new user to our database. "
    "Name is John Doe. Email is test@test.com, but also possible to contact "
    "him with hello@test.com email. Phone number is 555-123-4567, and "
    "the IP address is 192.168.1.100. The credit card number is 4567-8901-2345-6789. "
    "He works in Test LLC."
)

# Streamlit application
st.title("Prompt Sanitizer")
st.write("A tool that automatically cleans sensitive information from prompts, ensuring safe and secure use with Large Language Models (LLMs).")

# Create a text box for the user to enter the prompt with increased height
user_prompt = st.text_area("Enter your prompt:", default_prompt, height=200)

# Create a button to submit the prompt
if st.button("Submit"):
    # Sanitize the prompt using input scanners
    sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, user_prompt)
    
    # Display the sanitized prompt in a text area to keep the output
    st.subheader("Sanitized Prompt:")
    st.text_area("Sanitized Output:", sanitized_prompt, height=200)
    
    # Check if the prompt is valid
    if any(results_valid.values()) is False:
        st.error(f"The prompt is not valid. Scores: {results_score}")
    else:
        st.success("The prompt is valid.")
        #st.write(f"Scores: {results_score}")