from sys import prefix
from typing import Callable
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.routing import APIRoute
from filter import FilterAPIRouter
from utils import loadFiltersFromFile
from starlette.middleware import Middleware
from middleware import CustomFilterMiddleware
import uvicorn

class FilterRouter(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            print("HEY MAN. DUCKY WAS HERE")
            #raise HTTPException(status_code=401, detail="You encountered the wrong filter bud!")
            
        return custom_route_handler

def newCallable(request: Request) -> Request:
    print("HEY MAN. DUCKY WAS HERE")
    raise HTTPException(status_code=205)
    
    return request

router = FilterAPIRouter(prefix= "/cars").includeFilterOnMethod(method= "DoNothing", filter=newCallable)

middleware = [
Middleware(
    CustomFilterMiddleware, 
    filter_routers =[
        router
    ]
)
]
app = FastAPI(middleware=middleware)


@app.get("/cars/hey")
async def DoNothing():
    return "nuffin"

@app.get("/")
async def RunApp():
    return "Run"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)