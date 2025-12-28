Resort AI Management System
🏨 Technical Overview
A production-grade resort management platform leveraging modern Python stack with AI-powered agentic workflows. The system provides intelligent guest interactions through specialized AI agents while maintaining real-time operational visibility via an analytical dashboard.

🛠️ Technology Stack Architecture

┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  FastAPI (REST API)            │   Streamlit (Dashboard)    │
│  • ASGI with Uvicorn           │   • Reactive Web App       │
│  • OpenAPI 3.0 Documentation   │   • Real-time Updates      │
│  • WebSocket Support           │   • Plotly Visualization   │
│  • Pydantic Validation         │   • Pandas DataFrames      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI & BUSINESS LOGIC LAYER                │
├─────────────────────────────────────────────────────────────┤
│  Google Gemini 2.0 Flash      │   Custom Agent Framework    │
│  • Generative AI Core         │   • Multi-Agent Orchestration│
│  • Intent Classification      │   • Tool Execution Engine   │
│  • Natural Language Processing│   • Context Management      │
│  • Response Generation        │   • State Transition Logic  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA PERSISTENCE LAYER                   │
├─────────────────────────────────────────────────────────────┤
│  SQLAlchemy ORM               │   SQLite Database           │
│  • Declarative Base           │   • File-based Storage      │
│  • Session Management         │   • ACID Compliance         │
│  • Relationship Mapping       │   • Concurrent Access       │
│  • Transaction Control        │   • .db File Format         │
└─────────────────────────────────────────────────────────────┘
