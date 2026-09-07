from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exception_middleware
from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_router

app = FastAPI(title="Enterprise Assistant API", description="API for AI Enterprise Assistant Chatbot")

# Add this root endpoint
@app.get("/")
async def root():
    return {
        "message": "Enterprise Assistant API is running!",
        "docs": "Visit /docs for Swagger documentation",
        "endpoints": {
            "upload_pdfs": "/api/upload-pdfs",
            "ask_question": "/api/ask-question"
        }
    }

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Fixed: This should be boolean, not list
    allow_methods=["*"],
    allow_headers=["*"]
)

# middleware exception handlers
app.middleware("http")(catch_exception_middleware)

# routers
app.include_router(upload_router)
app.include_router(ask_router)