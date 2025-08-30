<img width="959" height="437" alt="image" src="https://github.com/user-attachments/assets/c6aad4b7-04de-408a-ab8b-bb612ec7f894" />

🦜 Chat with Any Database

This project is a Streamlit-based chatbot powered by LangChain + OpenAI, which lets you interact with your database in natural language.
Instead of writing complex SQL queries, just ask questions in plain English, and the chatbot will:

🔗 Connect to either SQLite (student.db) or your own MySQL database

💬 Understand your queries using OpenAI LLMs

📝 Convert them into SQL automatically

📊 Fetch and display results in a conversational style

✨ Features

🌐 Choose between local SQLite or remote MySQL connection

🔑 Secure handling of API keys and DB credentials

⚡ Real-time query execution with natural language

🎨 Simple, soft UI with ivory, pink, and white theme

🚀 How it Works

Enter your OpenAI API key.

Select your database type (SQLite/MySQL).

Ask your question (e.g., “Show me all students with marks above 80”).

The chatbot generates SQL → runs the query → shows results.

🛠️ Tech Stack

Python 3

Streamlit (UI)

LangChain (LLM framework)

OpenAI GPT Models (natural language → SQL)

SQLAlchemy (DB connections)
