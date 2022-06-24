import array
from ast import Raise
from enum import Enum
import logging
import types

from tracemalloc import Filter
from urllib import request


from fastapi.routing import APIRoute
from fastapi import APIRouter, Body, FastAPI, File, Request, Response
from fastapi.utils import generate_unique_id
from fastapi import params
from fastapi.datastructures import Default
import fastapi

from exceptions import ObjectNotOfTypeRequestError, MissingFilterConfigFileError
from utils import checkGlobalFilters, loadFiltersFromFile
from starlette import routing
from starlette.types import ASGIApp
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute, Match

from typing import (
    Any,
    Callable
)

class FilterAPIRouter:
    def __init__(
        self, 
        prefix: str,
        enabled: bool = True,
        global_filters: array = [],
        method_filters: dict = {},
        configFile = None,
    ) -> None:

        self.globalFilters = []
        self.methodFilters = {}
        if (not configFile is None):
            if (isinstance(configFile, str)):
                with open(configFile, 'r') as file:
                    self.globalFilters, self.methodFilters = loadFiltersFromFile(file)
            elif (isinstance(configFile, type(File))):
                self.globalFilters, self.methodFilters = loadFiltersFromFile(configFile)

        self.globalFilters.extend(global_filters)
    
        for key in method_filters:
            if (not key in self.methodFilters):
                self.methodFilters[key] = method_filters[key]
            else:
                assert isinstance(self.methodFilters[key], array.ArrayType); "The method filter with key: {0} was not of type array".format(key)
                self.methodFilters[key].extend(method_filters[key])

        self.prefix = prefix
        self.enabled = enabled

    def enable(self, path: str, filter_classes: array = []) -> Callable:
        return print                                                        #TODO

    def includeFilterOnMethod(self, method: str, filter: callable):
        assert isinstance(filter, types.FunctionType); "The implemented filter must be of type: Function"
        if (not method in self.methodFilters):
            self.methodFilters[method] = [filter]
        else:
            _array = self.methodFilters[method]
            assert isinstance(_array, array.ArrayType); "methodFilters for the path {0} is not of type Array".format(method)
            self.methodFilters[method].append(filter)

        return self

    def includeGlobalFilter(self, filter: types.FunctionType): 
        assert isinstance(filter, types.FunctionType); "The implemented filter must be of type: Function"
        assert isinstance(self.globalFilters, array.ArrayType); "The global filters for the FilterAPIRouter is not of type Array"
        self.globalFilters.append(filter)
        return self

    

