# AI-Assisted CRM using MCP Server

This is an experimental **AI-powered CRM application** I built using **FastAPI** and the **Model Context Protocol (MCP)**.

I created this project to explore how MCP can be integrated into a real-world backend so that **AI agents can interact with APIs and perform CRM operations using natural language**.

The system includes a **CRM API, MCP server, and an AI chatbot interface**. Through the chatbot, users can perform actions like creating contacts, retrieving lead details, updating information, and managing tasks using simple natural language commands.

I built this project mainly to learn and experiment with:

- Model Context Protocol (MCP)
- AI agent integration with backend APIs
- Tool-based LLM workflows
- Real-world AI application architecture

---

## Features

### AI Chatbot with MCP Tools
I built a chatbot that allows users to interact with the CRM using natural language.  
The chatbot communicates with the **MCP server**, which exposes backend APIs as tools for the AI agent.

Example prompts:

- "Create a new contact named John Doe"
- "Show all leads with status Open"
- "Update contact phone number"
- "List all tasks for today"

---

### CRM Backend
The backend provides APIs for managing **Contacts, Leads, Deals, Tasks, and Users**.

---

### MCP Server Integration
The FastAPI backend is exposed as an **MCP-compatible server**, enabling AI agents to call APIs through structured tools.

---

### Redis Memory Cache
User queries are cached using **Redis**, allowing repeated questions to return cached responses and reducing LLM token usage and latency.

---

### JWT Authentication
Secure authentication with **user login, role-based permissions, and token-based access**.

---

## Architecture Overview

### CRM + MCP System Architecture

<p align="center">
  <img src="https://github.com/MdJafirAshraf/AI-Assisted-CRM-Using-MCP-Server/blob/main/images/crm_mcp_architecture_diagram.png" width="900">
</p>

### Layered Architecture

<p align="center">
  <img src="https://github.com/MdJafirAshraf/AI-Assisted-CRM-Using-MCP-Server/blob/main/images/crm_mcp_layer_architecture_diagram.png" width="900">
</p>

The LLM agent decides which MCP tool to call based on the user prompt.

---

## Project Structure

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

Here’s the **updated `.md` installation guide using `uv` properly** (creating environment + installing dependencies). I also made the language slightly clearer and more natural for a **GitHub README**.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Assisted-CRM-Using-MCP-Server.git
cd AI-Assisted-CRM-Using-MCP-Server
```

---

### Install `uv`

If you don’t have **uv** installed, install it first.

```bash
pip install uv
```

---

### Create Virtual Environment

Initiate uv:

```
uv init
```

Create a virtual environment using **uv**:

```bash
uv venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / Mac**

```bash
source .venv/bin/activate
```

---

### Install Dependencies

Install the project dependencies:

```bash
uv pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_secret_key
```

---

## Running the Application

Start the FastAPI server:

```bash
python run.py
```

The application will start at:

```
http://127.0.0.1:8000
```

---

### API Documentation

FastAPI provides interactive API documentation.

**Swagger UI**

```
http://127.0.0.1:8000/docs
```

---

### MCP Endpoint

The **MCP server** is exposed at:

```
/llm/mcp
```

This endpoint allows **AI agents to interact with the CRM backend APIs as MCP tools**.

---

If you'd like, I can also help you add **3 more powerful README sections** that make your repo look **more professional for AI/LLM engineer portfolios**:

* **Project Architecture Diagram**
* **MCP Tool Flow Explanation**
* **AI Agent Workflow (User → LLM → MCP → API)**

These sections make recruiters immediately understand the project.


## Example Chat Interaction

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

## Learning Objectives

This project demonstrates:

* Integrating **Model Context Protocol (MCP)** with FastAPI
* Building **AI agents that call backend APIs**
* Tool-based LLM architecture
* Caching LLM responses using Redis
* Designing scalable AI-powered backend systems

---

# License

This project is open-source and available under the MIT License.



