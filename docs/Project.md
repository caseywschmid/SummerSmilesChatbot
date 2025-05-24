# Project Description

Goal: To create a chatbot for the website summersmiles.com

Description: The chatbot will be attached to a vector database of all of the websites content. It will use Open AI as the LLM. Currently, only the backend code is needed. The object is to create a custom bot that we be higher quality than other out of the box solutions. The key to this is the quality of the scraping of the site and the construction of the bots "brain". 

# Tasks: 
- Create the basic framework that will control an individual chat session. I want to use the built in OpenAI API for controlling the conversation state. There is no need to store the conversation state across sessions. Whenever a user visits the site, a new session will be created and the chatbot will start from scratch. 
- Create an Open AI Service that will handle the creation of the vector store that will contain all of the sites information. This service should also handle the chat feature making calls to the OpenAI API for the chat functionality. 

## Tech Stack

- Python
- FastAPI
- OpenAI