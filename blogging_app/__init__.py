from fastapi import FastAPI, HTTPException
from routers import routes


app = FastAPI(title="FlyJob API", description="Blogging App API")


app.include_router(routes, home, about, contact)

