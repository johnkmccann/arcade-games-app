from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import games

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(games.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Arcade Games API!"}