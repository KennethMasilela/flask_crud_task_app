# Flask Task Manager App

A lightweight **CRUD (Create, Read, Update, Delete)** task manager built with **Flask**, **SQLite**, and **SQLAlchemy**, supporting **user registration/login**, task assignment, and priority management.

---

## Features

- User Authentication (Register, Login, Logout)
- Create, Edit, Delete Tasks
- Tasks linked to logged-in users
- Fields: title, description, status, due date, priority, category, notes
- Bootstrap-styled UI with flash messages
- Password hashing via `werkzeug.security`

---

## Screenshots

![Login Page](images/login.png)
![Register Page](images/register.png)
![Welcome Dashboard](images/welcome.png)
![Task Manager structure container](images/task_manager.png)
![Add tasks fields](images/Add_task.png)
![Task Table Fields](images/task_list_table.png)
![Add Task Button](images/button%20add%20task.png)
![Delete And Edit Buttons](images/buttons%20delete%20and%20edit.png)
![Edit Popup Table Container](images/popup%20edit%20task%20table.png)
![Save and Cancel edit Buttons](images/save%20and%20cancel%20button.png)
![Confirmation Update Message popup](images/update%20task%20pop%20confirmation.png)
![Confirmation Delete Message popup](images/pop%20delete%20confirmatio.png)
![Logout Button](images/button%20logout.png)
![Confirmation Logout Message popup](images/successful%20logout.png)
---

## Tech Stack

- **Python 3**
- **Flask**
- **SQLite**
- **SQLAlchemy**
- **Jinja2 Templates**
- **Bootstrap 4/5 (optional)**

---

## Installation & Running

### Prerequisites

- Python 3.x
- `pip`
- (Optional) Virtual environment

### Installation

```bash
git clone https://github.com/KennethMasilela/flask_crud_task_app.git
cd flask-crud-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
