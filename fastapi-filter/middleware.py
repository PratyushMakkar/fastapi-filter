from array import array
from cgitb import handler
import logging
import re
import string
import types
import traceback
from typing import Callable
from urllib import request
from fastapi import  APIRouter, HTTPException, Response
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.applications import Starlette
from starlette.requests import Request 
from starlette.responses import Response
from starlette.routing import Match
from exceptions import _handleHTTPException

from urllib.parse import urlparse


from filter import FilterAPIRouter

def _prepareRequestURL(request_url: str) -> dict:
        url_dict = {}
        parsed = urlparse(str(request_url))
        path = parsed.path
        url_dict["path"] = path
        if (path[0] == "/"):
            url_dict['prefix'] = "/{0}".format(path.split("/")[1])
        else:
            url_dict['prefix'] = "/{0}".format(path.split("/")[0])
        return url_dict

class CustomFilterMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, filter_routers = []):
        for item in filter_routers:
            assert isinstance(item, FilterAPIRouter), "All objects passed to CustomFilterMiddleware must be of type FilterAPIRouter"
        self.filter_routers :array = filter_routers
        super().__init__(app)
    
    
    @staticmethod
    def _implementFilters(request: Request, filters = []):
        if (filters is None):
            return request

        for filter_request in filters:
            if (not isinstance(filter_request, types.FunctionType)):
                raise HTTPException(status_code=500, detail= "Internal servor error due to filters")
            request = filter_request(request)
            assert(isinstance(request, Request))
        return request
        

    @staticmethod
    def _match(filter: FilterAPIRouter, handler: str) -> array:
        if filter is None:
            return []

        if (hasattr(filter, "methodFilters")):
            try:
                filters_array = filter.methodFilters[handler] 
                return filters_array
            except KeyError as err:
                logging.debug("The method: {0} could not be matched to any filters".format(handler))
                print(traceback.print_exception(err))

        return []

    @DeprecationWarning
    def _findRequestFilters(self, request_url: str) -> array:
        url_dict = _prepareRequestURL(request_url)
        prefix = url_dict['prefix']
        path = url_dict["path"]
        print("prefix: {0}, path: {1}".format(prefix, path))
        for filter_router in self.filter_routers:
            if (not filter_router.enabled):
                return []

            if (filter_router.prefix == prefix):
                return CustomFilterMiddleware._match(filter_router, path)

    async def dispatch(self, request: Request, call_next:  RequestResponseEndpoint) -> Response:
        app: Starlette = request.app
        request_url = request.url

        for route in app.routes:
            match, _ = route.matches(request.scope)
            if match == Match.FULL and hasattr(route, "endpoint"):
                handler = route.endpoint
                break
            handler = None
        
        if (handler is None):
            return await call_next(request)

        handler_name = "{0}".format(handler.__name__)

        filter_router = None
        expected_prefix = _prepareRequestURL(request_url)['prefix']

        try:
            for filter_route in self.filter_routers:
                if (filter_route.enabled and filter_route.prefix == expected_prefix):
                    filter_router = filter_route
                    break
        except AttributeError as err:
            logging.debug("An attribute error was raised. Likely cause is filter_route.enabled is not an attribute.")
            print(traceback.print_exception(err))

        if (filter_router is None):
            return await call_next(request)

        filters_array = CustomFilterMiddleware._match(filter_route, handler= handler_name)

        try:
            request = CustomFilterMiddleware._implementFilters(request, filters_array)
        except HTTPException as err:
            return _handleHTTPException(err)
        
        response = await call_next(request)
        
        return response
