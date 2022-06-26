# :gear: fastapi-filter
fastapi-filter is a library that allows the client to implement filters for each route in an API. It uses a Starlette middleware to determine which filters should be executed before the main handler is called. 

## :inbox_tray: Dependancies And Installtion 
Currently support is limited to ```fastapi ``` and it is a dependency. The project will be expanded to include all applications built on top of ```Starlette```. 
1. Install the following python libraries
    -  <kbd>pip install fastapi</kbd> 
2. Add the <kbd>fastapi-filter</kbd> directory into your project directory using the <kbd>git clone</kbd> commpand. 
## :pushpin: Quickstart

To begin filtering requests, the ```CustomFilterMiddleware``` class must be configured and registered with our ```Starlette``` application.

If we have the following route in our application,

```python
app = FastAPI()

@app.get("/")
async def HelloWorld():
    return "Hello World"
```

Creating filters is an incredibly simple process. The filter must be of type <kbd>FunctionType</kbd> and accept a parameter of <kbd>request</kbd> which is of type <kbd>fastapi.Request</kbd>.   

```python
# The method takes an object request of type fastapi.Request
def TimeRouteFilter(request: Request) -> Request:
    time = datetime.now()
    print("The time of incoming request to '/' is {0}".format(time))
    return request           #All filters must return an object of type Request
```


After our filter is created, we can register it with an instance of ```FilterAPIRouter``` which will overlook all incoming requests with the prefix <kbd>"/"</kbd> and implement the neccesary filters. 

```python
from fastapi-filter.filter import FilterAPIRouter

my_filter = FilterAPIRouter(prefix = "/")
            .includeFilterOnMethod(method = "HelloWorld", filter = TimeRouteFilter)
            .includeFilterOnMethod(...)
```

Alternatively a decorator can be used to register <kbd>TimeRouteFilter</kbd>

```python
import fastapi

def TimeRouteFilter(request: Request) -> Request:
    time = datetime.now()
    print("The time of incoming request to '/' is {0}".format(time))
    return request

my_filter = FilterAPIRouter(prefix = "/")

app = FastAPI()

@my_filter.enable(filters = [TimeRouteFilter])
@app.get("/")
async def HelloWorld():
    return "Hello World"
```

Our filter can now be finally registered with our middleware application.  

```python
import fastapi
from fastapi-filter.filter import FilterAPIRouter

my_filter = FilterAPIRouter(prefix = "/")
            .includeFilterOnMethod(method = "HelloWorld", filter = TimeRouteFilter)
            .includeFilterOnMethod(...)

app_middleware = [
  Middleware(CustomFilterMiddleware, filter_routers =[my_filter])
]

app = FastAPI(middleware=app_middleware)

@app.get("/")
async def HelloWorld():
    return "Hello World"
```
## Documentation
1. 
1. ## :hammer_and_wrench: Contributing to the project
If you would like to contribute to the project, feel free to create a pull request. Make sure that all documentation is present for any changes.  
## :scroll: License

The library is licensed under <kbd>GNU GENERAL PUBLIC LICENSE</kbd>

