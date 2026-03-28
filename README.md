# AI-Assisted CRM Using MCP Server

A full-stack CRM application integrated with an MCP (Model Context Protocol) server, built for learning how real-world AI agents communicate with backend services. The project includes a built-in chatbot that lets you perform CRM operations — creating contacts, managing deals, updating leads — using natural language prompts.

I built this using FastAPI, which made it straightforward to expose every endpoint as both a REST API and an MCP tool simultaneously. The goal was to demonstrate how modern applications can be designed to serve both human users and AI agents from a single codebase.

> This project is purely for educational purposes — to understand how to build your own MCP server, how to structure tools that AI agents can understand, and how AI agents communicate with MCP servers in a real-world context.

---

## Why I Built This

AI agents are everywhere now. Most developers know how to build APIs for users, but building APIs that AI agents can reliably understand and use is a different skill. This project is my attempt to bridge that gap with a real, working example.

What I handled in this project:

- Designed the system architecture and layered structure
- Built the MCP server on top of FastAPI endpoints
- Created the LLM client and AI agent
- Implemented Redis-based cache memory for faster agent-to-MCP communication and to avoid redundant API calls
- Secured all MCP access with JWT authentication via request headers
- Enforced role-based access control for both the REST API and MCP tools

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

The LLM agent reads the user prompt, decides which MCP tool to call, executes the corresponding CRM API, and returns the result — all automatically.

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

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Assisted-CRM-Using-MCP-Server.git
cd AI-Assisted-CRM-Using-MCP-Server
```

### 2. Install `uv`

I use `uv` for package management — it's significantly faster than pip.

```bash
pip install uv
```

### 3. Create a Virtual Environment

```bash
uv init
uv venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_secret_key
```

---

## Running the Application

```bash
python run.py
```

The server will start at:

```
http://127.0.0.1:8000
```

### API Documentation

FastAPI's interactive Swagger UI is available at:

```
http://127.0.0.1:8000/docs
```

### MCP Endpoint

The MCP server is exposed at:

```
/llm/mcp
```

This is the endpoint that AI agents use to interact with the CRM backend as a set of callable MCP tools.

---

## Example Chat Interaction

The chatbot supports natural language commands for creating, updating, and retrieving records. Delete operations and queries using raw IDs are intentionally not supported through the chat interface.

**User prompt:**
```
Create a new contact named John Doe with phone number 9876543210
```

**What happens internally:**
1. The AI agent interprets the intent from the prompt
2. It selects and calls the appropriate MCP tool
3. The tool executes the corresponding CRM API
4. The result is returned to the user in natural language

---

## License

This project is open-source and available under the [MIT License](LICENSE).