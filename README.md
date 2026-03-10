# Herrea Inventory System

Herrea is a lightweight, team‑based inventory management platform designed for small groups, clubs, and organizations.  
It provides:

- A clean, modern **WebUI** with login‑based access  
- A simple, well‑structured **REST API** for automation and integrations  
- Team‑scoped inventory separation  
- Admin and public permission layers  
- Zero external dependencies (SQLite + Flask)

Herrea is fully open‑source under the **GNU AGPLv3** license.

---

## ✨ Features

### 🔐 WebUI with login-based access
- Username/password login  
- Session-based authentication  
- No headers required for normal use  
- Clean, responsive interface (coming soon)

### 🧩 Team-based inventory
- Users only see items belonging to their team  
- Admins can manage all teams  
- Public users are read-only

### 🛠️ Admin tools
- Add, edit, remove items  
- View logs  
- Manage teams (future)

### 🌐 REST API (optional)
- Header-based authentication for scripts and integrations  
- Same permission model as WebUI  
- Read-only public endpoints  
- Full admin endpoints

### 📦 Zero-config database
- SQLite backend  
- Automatic schema creation  
- Portable and easy to back up

### 🕊️ AGPLv3 licensed
- All modifications must remain open  
- Perfect for community-driven development

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize the database
```bash
python - << 'EOF'
from app.db import init_db
init_db()
EOF
```

### 3. Run the server
```bash
python run.py
```

WebUI will be available at:

```
http://127.0.0.1:3000/
```

API endpoints remain under:

```
/str/api/
```

---

## 🔑 Authentication

### WebUI (recommended)
- Login form  
- Session cookie  
- No headers required  
- Intended for normal users

### API (optional)
Use only for scripts, bots, or integrations:

```
X-User: <username>
X-Pass: <password>
```

---

## 🧭 API Overview

### Admin API (`/str/api/admin/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/add` | Add an item |
| POST | `/edit` | Edit an item |
| POST | `/remove` | Remove an item |
| GET | `/logs` | View logs |

### Public API (`/str/api/public/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/items` | List items for the user's team |
| GET | `/item/<id>` | Get a specific item |

---

## 🗄️ Database Schema

### items
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Item name |
| quantity | INTEGER | Amount |
| team | TEXT | Team owner |
| notes | TEXT | Optional notes |

### logs
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| action | TEXT | add/edit/remove |
| item_id | INTEGER | Affected item |
| username | TEXT | Who performed the action |
| timestamp | DATETIME | Auto |

---

## 🧪 Example API Requests

### Add an item (admin)
```bash
curl -X POST http://127.0.0.1:3000/str/api/admin/add \
  -H "X-User: admin" \
  -H "X-Pass: adminpass" \
  -H "Content-Type: application/json" \
  -d '{"name":"Tent","quantity":3,"team":"alpha","notes":"New"}'
```

### Read items (public)
```bash
curl http://127.0.0.1:3000/str/api/public/items \
  -H "X-User: member" \
  -H "X-Pass: memberpass"
```

---

## 🧑‍💻 Development

- Python 3.10+
- Flask
- SQLite
- No external services required

---

## 📜 License

This project is licensed under the **GNU AGPLv3**.  
See the `LICENSE` file for details.

---

## 🖼️ Logo

*(Your logo will go here)*

---

## 🤝 Contributing

Pull requests are welcome.  
All contributions must be licensed under **AGPLv3**.

---

## 🌐 Wiki

Full documentation is available in the Wiki:

- Installation
- WebUI usage
- API reference
- User management
- Database structure
- Deployment
- FAQ
