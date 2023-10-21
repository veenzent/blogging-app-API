from blogging_app import app

@app.get("/")
async def get():
    return {"message": "Hello World"}