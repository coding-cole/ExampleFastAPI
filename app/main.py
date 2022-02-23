from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth_routes, post_routes, user_routes, vote_routes
from .config import settings


print(settings.database_password)

# models.Base.metadata.create_all(bind=engine) # no longer needed since we now use alembic

app = FastAPI()

origins = [
    "*",
    # "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_routes.router)
app.include_router(user_routes.router)
app.include_router(auth_routes.router) 
app.include_router(vote_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API!!!"}