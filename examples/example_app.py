from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.routing import APIRoute
from fastapi_filter.filter import FilterAPIRouter

from starlette.middleware import Middleware
from fastapi_filter.middleware import CustomFilterMiddleware
import uvicorn

def TimeRouteFilter(request: Request) -> Request:
    time = datetime.now()
    print("The time of incoming request to '/route_one' is {0}".format(time))
    return request   

def MethodLevelFilter(request: Request) -> Request:
    time = datetime.now()
    print("The first method-level filter was executed at {0}".format(time))
    return request

def SampleErrorfilter(request: Request) -> Request:
    raise HTTPException(status_code=400, detail="The request is bound to fail!") 
         
FilterRouter = FilterAPIRouter(
    prefix="/route_one", 
    global_filters=[TimeRouteFilter]
).includeFilterOnMethod("route_one_handler", MethodLevelFilter).includeFilterOnMethod('route_one_handler', SampleErrorfilter)

middleware = [
Middleware(
    CustomFilterMiddleware, 
    filter_routers =[
        FilterRouter
    ]
)
]

app = FastAPI(middleware=middleware)

@app.get("/route_one/path")
def route_one_handler():
    return {"Detail": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)