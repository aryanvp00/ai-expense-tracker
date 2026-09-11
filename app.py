from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from routers.expenses import router as expense_router
from routers.auth import router as auth_router
from routers.ai import router as ai_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expense_router)
app.include_router(auth_router)
app.include_router(ai_router)


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}