from fastapi import FastAPI
from database import engine,SessionLocal
import models
from routers import user_rout,log,todos,admin,register_rout

app=FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(user_rout.router)
app.include_router(log.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(register_rout.router)




@app.get('/')
def home():
    return "Hello"


