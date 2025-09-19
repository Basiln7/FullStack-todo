from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# to run at vercel(host )
from mangum import Mangum

# importing my own module
from models import User, CreateUser, Task, CreateTask
from database import SessionLocal, engine, Base
from auth import create_access_token
from security import hash_password, verify_password

# Initialize App and Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# to run vercal
handler = Mangum(app)

# create database tables
Base.metadata.create_all(bind=engine)

# This gives each route access to the database.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This enables JWT-based authentication for protected routes.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# These serve your frontend pages
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Register Route
@app.post("/register")
def register(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(name=user.name, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User '{new_user.name}' registered successfully"}

# Login Route
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.name})
    return {"access_token": token, "token_type": "bearer"}

# Create task protected
@app.post("/tasks")
def create_task(task: CreateTask, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    new_task = Task(task_name=task.task_name, task_description=task.task_description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created", "task": new_task}

# get all tasks
@app.get("/tasks")
def get_tasks(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# Delete Task (Protected)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted"}

