from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hola estas conectado mediante FastAPI"}

@app.get("/data")
async def data():
     return{"events": ["event1", "event2", "event3"]}