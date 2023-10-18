from fastapi import FastAPI, HTTPException
from blogging_app.routers import routes, home, about, contacts

app = FastAPI(title="FlyJob API", description="Blogging App API")


app.include_router(home, prefix="/home", tags=["Home Page"])
app.include_router(about, prefix="/about", tags=["About Page"])
app.include_router(contacts, prefix="/contacts", tags=["Contacts Page"])


# home, about, contacts)

