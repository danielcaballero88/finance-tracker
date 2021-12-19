import fastapi as fa


app = fa.FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
