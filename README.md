Resort AI Management System
🏨 Technical Overview
A production-grade resort management platform leveraging modern Python stack with AI-powered agentic workflows. The system provides intelligent guest interactions through specialized AI agents while maintaining real-time operational visibility via an analytical dashboard.

🛠️ Technology Stack Architecture
Core Infrastructure Layer
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

Component Integration Flow
Client Request
     ↓
[FastAPI Endpoint] ←── HTTP/WebSocket
     ↓
[Pydantic Schema Validation]
     ↓
[Agent Manager Routing]
     ↓
[Gemini 2.0 Flash Processing]
     ↓
[Tool Execution via SQLAlchemy]
     ↓
[SQLite Database Transaction]
     ↓
[Streamlit Dashboard ←───┐
     ↓                   │
[Real-time Response]     │
     ↓                   │
Client                  Update
                        ↓
                 [Plotly Charts]
                        ↓
                 [Pandas DataFrames]
                 
📊 Detailed Technology Specifications
Backend Framework (FastAPI)
Version: 0.104+ (ASGI-compliant)
Key Features:
Automatic OpenAPI/Swagger documentation at /docs
Async/await support for concurrent request handling
Dependency injection system
Request/Response validation with Pydantic
WebSocket endpoints for real-time communication
Configuration:
# Uvicorn server configuration
uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
AI Engine (Google Gemini 2.0 Flash)
SDK: google-generativeai Python client
Model: gemini-2.0-flash for low-latency operations
Integration Pattern:
User Input → Prompt Engineering → Gemini API → Structured Output
      ↓           ↓                  ↓             ↓
[Raw Text] [System + User]    [REST Call]   [JSON/Text]
                            [Context + Tools]
Agent Types:
Receptionist: General inquiries, facility information
Restaurant: Menu queries, order processing
Room Service: Amenity requests, maintenance
Dashboard Framework (Streamlit)
Architecture: React-like declarative UI
Key Components:
st.dataframe(): Tabular data display with sorting/filtering
st.plotly_chart(): Interactive visualizations
st.metric(): Real-time KPI cards
st.selectbox()/st.button(): Interactive controls
Update Mechanism: Polling-based synchronization with backend API
Data Visualization (Plotly + Pandas)
Plotly: Interactive, publication-quality graphs
Pie charts for request distribution
Bar charts for order volume trends
Time-series graphs for request patterns
Pandas: Data manipulation engine
# Typical dashboard data flow
API Response → Pandas DataFrame → Data Cleaning → Plotly Figure → Streamlit Display
Database Layer (SQLAlchemy + SQLite)
SQLAlchemy Features:
Declarative ORM with Base = declarative_base()
Session management with context handlers
Relationship modeling (one-to-many, many-to-one)
Alembic-ready migration structure
SQLite Configuration:
sqlite:///resort.db (relative path)
Connection pooling: 5-20 connections
Journal mode: WAL (Write-Ahead Logging)
Configuration Management (python-dotenv)
Structure:
.env
├── API_KEYS
│   └── OPENAI_API_KEY=gemini-...
├── DATABASE
│   └── DATABASE_URL=sqlite:///resort.db
└── APPLICATION
    ├── LOG_LEVEL=INFO
    └── POLLING_INTERVAL=2
Loading Pattern:
from dotenv import load_dotenv
load_dotenv()  # Loads from .env file
🔄 System Communication Patterns
HTTP API Communication
Endpoints:
  Guest-Facing:
    POST /chat: Process guest messages via AI agents
    GET /menu: Retrieve current menu offerings
    GET /order/{id}: Check order status
  
  Dashboard-Facing:
    GET /orders: Fetch all orders (with filtering)
    GET /requests: Fetch all service requests
    PUT /orders/{id}: Update order status
    PUT /requests/{id}: Update request status
  
  WebSocket:
    /ws/updates: Real-time status updates
Data Flow Between Components
┌─────────────┐    REST/JSON    ┌─────────────┐    SQLAlchemy    ┌─────────────┐
│  Streamlit  │ ◄─────────────► │   FastAPI   │ ◄─────────────► │   SQLite    │
│  Dashboard  │    Polling      │   Backend   │     ORM Calls   │  Database   │
└─────────────┘   (2s interval) └─────────────┘                 └─────────────┘
                         │                                              │
                         │                                              │
                    WebSocket                                      File I/O
                    (Real-time)                                   (resort.db)
                         │                                              │
                         ▼                                              ▼
┌─────────────┐    HTTP/JSON    ┌─────────────┐    Gemini API    ┌─────────────┐
│   Client    │ ◄─────────────► │   Agent     │ ◄─────────────► │  Google AI  │
│ (Frontend)  │   Request/      │  Framework  │    REST Calls   │   Services  │
└─────────────┘     Response    └─────────────┘                 └─────────────┘
🏗️ Development Architecture Patterns
Multi-Agent System Design
                      ┌─────────────────┐
                      │   Orchestrator  │
                      │  (FastAPI Route)│
                      └─────────┬───────┘
                                │
          ┌────────────┬────────┴───────┬─────────────┐
          │            │                 │             │
          ▼            ▼                 ▼             ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Receptionist   │ │   Restaurant    │ │  Room Service   │
│     Agent       │ │     Agent       │ │     Agent       │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ • Facility Info │ • Menu Queries    │ • Service Reqs   │
│ • Room Status   │ • Order Processing│ • Amenity Mgmt   │
│ • General Q&A   │ • Dietary Info    │ • Maintenance    │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                    │
         └───────────────────┼────────────────────┘
                             │
                      ┌──────▼──────┐
                      │  Tool Layer │
                      │  (SQLAlchemy)│
                      └──────┬──────┘
                             │
                      ┌──────▼──────┐
                      │  Database   │
                      │  (SQLite)   │
                      └─────────────┘
Database Schema Implementation
# SQLAlchemy ORM Pattern
class Order(Base):
    __tablename__ = 'orders'
    
    # Column definitions with type hints
    id = Column(Integer, primary_key=True)
    room_number = Column(Integer, nullable=False)
    items = Column(JSON)  # Storing order items as JSON
    total_amount = Column(Float)
    status = Column(String(50))  # Pending/Preparing/Delivered
    
    # SQLAlchemy relationships
    service_requests = relationship("ServiceRequest", back_populates="order")
    
    # Pydantic schema for API validation
    class Config:
        orm_mode = True
AI Agent Execution Pattern
# Simplified agent execution flow
def execute_agent_workflow(user_input: str) -> dict:
    # 1. Input validation (Pydantic)
    validated_input = validate_input(user_input)
    
    # 2. Intent classification (Gemini)
    intent = gemini_classify(validated_input)
    
    # 3. Agent routing
    agent = route_to_agent(intent)
    
    # 4. Tool execution
    result = agent.execute_tools(validated_input)
    
    # 5. Database persistence
    db_record = persist_to_database(result)
    
    # 6. Response generation
    response = generate_response(db_record)
    
    return {
        "response": response,
        "data": db_record,
        "metadata": {"agent": agent.name, "intent": intent}
    }
Data Flow Diagram
User sends a message via Chat Interface.
Agent processes the intent and calls a Tool (e.g., place_restaurant_order).
Tool writes data (Order/ServiceRequest) to resort.db using SQLAlchemy models.
Dashboard (Streamlit) polls the API (/orders, /requests) which reads from resort.db.
Staff updates status on Dashboard -> API updates resort.db -> User can query status.
Models (backend/models.py)
Order: Tracks room_number, items (JSON), total_amount, and status.
ServiceRequest: Tracks room_number, request_type, details, and status.
MenuItem: Stores the catalog of available food items and prices.
Dashboard Connectivity
The Streamlit dashboard (dashboard/app.py) does not connect directly to the database. Instead, it communicates via the FastAPI endpoints:

GET /orders: Fetches all restaurant orders.
GET /requests: Fetches all housekeeping/service requests.
PUT /orders/{id}: Updates order status (Pending -> Preparing -> Delivered).
PUT /requests/{id}: Updates request status.
This decoupling allows the backend to handle all logic and validation while the dashboard remains a lightweight UI layer.

🚀 Running the System
1. Start the Backend Server
This serves the API and the AI Agents.

uvicorn backend.main:app --reload --port 8000
2. Start the Dashboard
This launches the admin interface.

python -m streamlit run dashboard/app.py
🔑 Key Configuration
.env: Must contain OPENAI_API_KEY (used here for Gemini compatibility layer or direct Gemini configuration).
menu_output.txt: The text source for the Restaurant Agent to read the menu.des which specialist agent should handle the request.
*   **File:** `backend/agents.py` -> `AgentManager.route_request`
*   **Destinations:**
    *   `Restaurant`: For food orders and menu queries.
    *   `RoomService`: For housekeeping, laundry, and amenities.
    *   `Receptionist`: For general questions, pool/gym info, and room requests.

### 2. Specialist Agents
Each agent handles specific tasks using dedicated system prompts and tools.

*   **Receptionist Agent**
    *   **Prompt:** Persona of a helpful front-desk staff.
    *   **Tools:**
        *   `check_room_availability`: Checks database/mock logic for room status.
        *   `get_facility_info`: Provides info on gym, spa, pool, etc.

*   **Restaurant Agent**
    *   **Prompt:** Focused on menu knowledge and order accuracy.
    *   **Tools:**
        *   `get_menu_items`: Reads the `menu_output.txt` file to show current offerings.
        *   `place_restaurant_order`: Validates items against the DB and creates an `Order` record.

*   **Room Service Agent**
    *   **Prompt:** Efficient handling of guest needs.
    *   **Tools:**
        *   `create_room_service_request`: Creates a `ServiceRequest` record in the DB.

---

## 💾 Database & Dashboard Integration

The system maintains a "Single Source of Truth" in the `resort.db` SQLite database.

### Data Flow Diagram

1.  **User** sends a message via Chat Interface.
2.  **Agent** processes the intent and calls a **Tool** (e.g., `place_restaurant_order`).
3.  **Tool** writes data (Order/ServiceRequest) to `resort.db` using SQLAlchemy models.
4.  **Dashboard** (Streamlit) polls the API (`/orders`, `/requests`) which reads from `resort.db`.
5.  **Staff** updates status on Dashboard -> API updates `resort.db` -> User can query status.

### Models (`backend/models.py`)

*   **Order**: Tracks `room_number`, `items` (JSON), `total_amount`, and `status`.
*   **ServiceRequest**: Tracks `room_number`, `request_type`, `details`, and `status`.
*   **MenuItem**: Stores the catalog of available food items and prices.

### Dashboard Connectivity

The Streamlit dashboard (`dashboard/app.py`) does not connect directly to the database. Instead, it communicates via the FastAPI endpoints:

*   **GET /orders**: Fetches all restaurant orders.
*   **GET /requests**: Fetches all housekeeping/service requests.
*   **PUT /orders/{id}**: Updates order status (Pending -> Preparing -> Delivered).
*   **PUT /requests/{id}**: Updates request status.

This decoupling allows the backend to handle all logic and validation while the dashboard remains a lightweight UI layer.

---

## 🚀 Running the System

### 1. Start the Backend Server
This serves the API and the AI Agents.
```bash
uvicorn backend.main:app --reload --port 8000
```

### 2. Start the Dashboard
This launches the admin interface.
```bash
python -m streamlit run dashboard/app.py
```

### 3. Frontend (Optional)
If you have a separate frontend client (e.g., React or simple HTML), serve it on a different port (e.g., 8080).

---

## 🔑 Key Configuration

*   **.env**: Must contain `OPENAI_API_KEY` (used here for Gemini compatibility layer or direct Gemini configuration).
*   **menu_output.txt**: The text source for the Restaurant Agent to read the menu.
