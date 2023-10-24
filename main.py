from blogging_app import app

@app.get("/")
async def get():
    return {"Blog App": "Curiosity births Innovations. Discover articles, thoughts, and professionals from authors on any topic"}