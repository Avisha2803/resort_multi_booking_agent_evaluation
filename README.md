# Resort Booking & Management System Documentation

This document provides a detailed overview of the intelligent resort management system, explaining how AI agents work, how data flows between components, and how the dashboard connects to the backend.

## 🏗️ System Architecture

The project consists of three main components:

1.  **Backend API (FastAPI)**: Handles chat operations, agent routing, and database interactions.
2.  **Streamlit Dashboard**: A real-time interface for resort staff to view orders, requests, and analytics.
3.  **AI Agents (Google Gemini)**: Intelligent agents that handle user queries, process orders, and manage service requests.

### Directory Structure

-   `backend/`: Contains the core logic, API, database models, and agent definitions.
-   `dashboard/`: Contains the Streamlit application for the admin interface.
-   `resort.db`: SQLite database storing orders, service requests, and menu items.

---

## 🤖 How the Agents Work

 The system uses a **Multi-Agent Architecture** powered by Google Gemini 2.0 Flash.

### 1. The Orchestrator (Router)
*   **Role:** The entry point for all user messages.
*   **Logic:** It analyzes the user's intent and decides which specialist agent should handle the request.
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
