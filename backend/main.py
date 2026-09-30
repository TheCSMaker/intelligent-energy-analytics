from fastapi import FastAPI

app = FastAPI(
    title="Intelligent Energy Analytics API",
    description="Backend API for electrical energy analytics and intelligent load monitoring.",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "Intelligent Energy Analytics",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
