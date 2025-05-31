from fastapi import FastAPI
from app.routers import auth, books, readers, borrowings
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrowings.router)