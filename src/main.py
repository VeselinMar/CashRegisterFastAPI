from fastapi import FastAPI

app = FastAPI()

# run project from src directory
# uvicorn main:app --reload --app-dir src

@app.get("/")
def read_root():
    return {"message": "Hey there!"}
