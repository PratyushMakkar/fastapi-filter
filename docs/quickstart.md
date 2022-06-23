# :pushpin: Quickstart

To begin filtering requests, the ```CustomFilterMiddleware``` class must be configured and registered with our ```Starlette``` application.

If we have the following route in our application,

```python
app = FastAPI()

@app.get("/")
async def HelloWorld():
    return "Hello World"
```

To include a filter that logs the datetime for all incoming requests to <kbd>"/"</kbd>, we would first extend the ```APIRoute``` class and override the ```get_route_handler()``` method. Further documentation can be found on the [FastAPI website](https://fastapi.tiangolo.com/advanced/custom-request-and-route/).  

```python
import time
from typing import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute

class TimeRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        async def custom_route_handle(request: Request)-> Response:
            current_time = time.time()
            print("Incoming request at time:{0}".format(current_time))
            return request

        return custom_route_handler
```
After our filter is created, we can register it with an instance of ```FilterAPIRouter``` which will overlook all incoming requests with the prefix <kbd>"/"</kbd> and implement the neccesary filters. 

```python
from fastapi-filter.filter import FilterAPIRouter

my_filter = FilterAPIRouter(prefix = "/")
            .includeFilterOnMethod(method = "HelloWorld", filter = TimeRoute)
            .includeFilterOnMethod(...)
```

Alternatively a decorator can be used to register <kbd>TimerRouter</kbd>

```python
import fastapi

my_filter = FilterAPIRouter(prefix = "/")

app = FastAPI()

@my_filter.filter(filters = [TimeRoute])
@app.get("/")
async def HelloWorld():
    return "Hello World"
```

Our filter can now be finally registered with our middleware application.  

```python
import fastapi
from fastapi-filter.filter import FilterAPIRouter

my_filter = FilterAPIRouter(prefix = "/")
            .includeFilterOnMethod(method = "HelloWorld", filter = TimeRoute)
            .includeFilterOnMethod(...)

app_middleware = [
  Middleware(CustomFilterMiddleware, filter_routers =[my_filter])
]

app = FastAPI(middleware=app_middleware)

@app.get("/")
async def HelloWorld():
    return "Hello World"
```

