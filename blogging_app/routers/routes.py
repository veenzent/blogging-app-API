from fastapi import APIRouter, Request, status, Depends, HTTPException


blog_router = APIRouter()


#     --   G E T   R E Q U E S T S   --

@blog_router.get("/")
async def get_index():
    return {"message": "Welcome to Blogging App API"}





#     --   C R E A T E   R E Q U E S T S   --





#     --   U P D A T E   R E Q U E S T S   --





#     --   D E L E T E   R E Q U E S T S   --