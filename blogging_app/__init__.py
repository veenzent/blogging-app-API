from fastapi import FastAPI, HTTPException
from blogging_app.routers.home import home_routes
from blogging_app.routers.about import about_routes
from blogging_app.routers.contacts import contacts_routes

app = FastAPI(title="Blog APP", description="Blogging App API")


app.include_router(home_routes, prefix="/home", tags=["Home Page"])
app.include_router(about_routes, prefix="/about", tags=["About Page"])
app.include_router(contacts_routes, prefix="/contacts", tags=["Contacts Page"])

