# AI-Assisted CRM using MCP Server

An experimental **AI-powered CRM application** built with **FastAPI** and the **Model Context Protocol (MCP)**.
This project demonstrates how MCP can be integrated into a real-world application to allow **AI agents to interact with backend APIs and perform CRM operations through natural language**.

The system includes a **CRM API**, **MCP server**, and an **AI chatbot interface** capable of executing actions such as creating contacts, retrieving lead information, managing tasks, and more.

This project was built as a learning initiative to explore:

* Model Context Protocol (MCP)
* AI Agent integration with backend services
* Tool-based LLM workflows
* Real-world AI application architecture

---

# Features

### AI Chatbot with MCP Tools

Users can interact with the CRM using natural language.

Example prompts:

* "Create a new contact named John Doe"
* "Show all leads with status Open"
* "Update contact phone number"
* "List all tasks for today"

The chatbot communicates with the **MCP server**, which exposes backend APIs as tools for the AI agent.

---

### CRM Backend

The CRM backend includes APIs for managing:

* Contacts
* Leads
* Deals
* Tasks
* Users

---

### MCP Server Integration

The project exposes the FastAPI backend as an **MCP-compatible server**, allowing AI agents to call backend APIs through structured tools.

---

### Redis-based Memory Cache

To optimize LLM usage:

* User queries are cached
* Repeated questions return cached responses
* Reduces token usage and API latency

---

### JWT Authentication

Secure authentication system with:

* User login
* Role-based permissions
* Token-based authentication

---

# Tech Stack

Backend

* FastAPI
* Python
* SQLAlchemy
* Jinja2 Templates

AI & LLM

* LangChain
* Groq LLM
* MCP (Model Context Protocol)

Caching

* Redis

Frontend

* HTML
* CSS
* JavaScript

---

# Architecture Overview

```
User
   │
   │ Chat Request
   ▼
FastAPI Chat Endpoint
   │
   ▼
LLM Client (LangChain Agent)
   │
   ▼
MCP Client
   │
   ▼
MCP Server (FastAPI Tools)
   │
   ▼
CRM APIs
   │
   ▼
Database
```

The LLM agent decides which MCP tool to call based on the user prompt.

---

# Project Structure

```
AI-Assisted-CRM-Using-MCP-Server
├─ app
│  ├─ chatbot
│  │  ├─ cache_service.py
│  │  ├─ handle_error.py
│  │  ├─ llm_client.py
│  │  └─ redis_client.py
│  │
│  ├─ core
│  │  ├─ cache_invalidator.py
│  │  ├─ config.py
│  │  └─ security.py
│  │
│  ├─ dependencies
│  │  ├─ auth.py
│  │  └─ permission.py
│  │
│  ├─ models
│  │  ├─ contacts.py
│  │  ├─ deals.py
│  │  ├─ leads.py
│  │  ├─ tasks.py
│  │  └─ users.py
│  │
│  ├─ routes
│  │  ├─ routers
│  │  │  ├─ auth.py
│  │  │  ├─ chat.py
│  │  │  ├─ contacts.py
│  │  │  ├─ dashboard.py
│  │  │  ├─ deals.py
│  │  │  ├─ leads.py
│  │  │  └─ tasks.py
│  │  └─ routes.py
│  │
│  ├─ schemas
│  │  ├─ chat.py
│  │  ├─ contacts.py
│  │  ├─ deals.py
│  │  ├─ leads.py
│  │  ├─ tasks.py
│  │  └─ users.py
│  │
│  ├─ static
│  │  ├─ css
│  │  └─ js
│  │
│  ├─ templates
│  │  ├─ dashboard.html
│  │  ├─ contacts.html
│  │  ├─ deals.html
│  │  ├─ leads.html
│  │  ├─ tasks.html
│  │  ├─ login.html
│  │  └─ register.html
│  │
│  ├─ main.py
│  └─ db.py
│
├─ client.py
├─ run.py
├─ requirements.txt
└─ README.md
```

---

# Installation

### Clone the Repository

```
git clone https://github.com/yourusername/AI-Assisted-CRM-Using-MCP-Server.git
cd AI-Assisted-CRM-Using-MCP-Server
```

---

### Create Virtual Environment

```
python -m venv .venv
```

Activate it:

Windows

```
.venv\Scripts\activate
```

Linux / Mac

```
source .venv/bin/activate
```

---

### Install Dependencies

```
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key
```

---

# Running the Application

Start the server:

```
python run.py
```

Application will run at:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI provides interactive documentation:

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# MCP Endpoint

The MCP server is exposed at:

```
/llm/mcp
```

This allows AI agents to access CRM APIs as tools.

---

# Example Chat Interaction

User Prompt

```
Create a new contact named John Doe with phone number 9876543210
```

AI Agent

1. Understands intent
2. Calls MCP tool
3. Executes CRM API
4. Returns response to user

---

# Learning Objectives

This project demonstrates:

* Integrating **Model Context Protocol (MCP)** with FastAPI
* Building **AI agents that call backend APIs**
* Tool-based LLM architecture
* Caching LLM responses using Redis
* Designing scalable AI-powered backend systems

---

# Future Improvements

Possible enhancements:

* Multi-tenant CRM support
* Vector database for semantic memory
* Conversation history storage
* Streaming responses
* AI analytics for CRM data
* Role-based AI permissions

---

# License

This project is open-source and available under the MIT License.

---

# Author

Mohamed Jafir Ashraf

Software Engineer | Python Developer | AI Application Engineer

---

# Acknowledgements

* FastAPI
* LangChain
* Groq
* Model Context Protocol
