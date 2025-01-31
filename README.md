# DeepSeek_LangChain_Ollama
End To End Gen AI App Using DeepSeek-R1 With Langchain And Ollama to run locally.

The plan is to use all the specific models and integrate them with langchain.

# Steps:
1. Import prompt templates
2. Add some custom CSS styling for markdown and sidebar (with model selection, model capabilities selection, additional information, and contact information)
3. Create chat engine - initiate the LLM engine to use chat Ollama
4. Provide system prompt configuration
5. Manage the state of session
6. Create chat container
7. Display chat messages
8. Chat input and processing
9. Create chat processing pipeline using lcl expression
10. Take system prompt, update with respect to user, and return chat prompt template
11. Append user chat message with respect to role and content and build the prompt chain, responses, and then append to message log

# To run:
Install requirements listed in requirements.txt using the command 'pip install -r requirements.txt' and run app.py, then open the local/network URL.
