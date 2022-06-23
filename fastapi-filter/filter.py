import array
from ast import Raise
from enum import Enum
import logging

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
        _globalFilters: array = [],
        _methodFilters: dict = {},
        configFile = None,
    ) -> None:
        if (not configFile is None):
            if (isinstance(configFile, str)):
                with open(configFile, 'r') as file:
                    self.globalFilters, self.methodFilters = loadFiltersFromFile(file)
            elif (isinstance(configFile, type(File))):
                self.globalFilters, self.methodFilters = loadFiltersFromFile(configFile)

        self.globalFilters.extend(_globalFilters)
    
        for key in _methodFilters:
            if (not key in self.methodFilters):
                self.methodFilters[key] = _methodFilters[key]
            else:
                assert isinstance(self.methodFilters[key], array.ArrayType); "The method filter with key: {0} was not of type array".format(key)
                self.methodFilters[key].extend(_methodFilters[key])

        self.prefix = prefix
        self.enabled = enabled

    def filter(self, path: str, filter_classes: array = []) -> Callable:
        return print               #TODO

    def _addMethodLevelFilter(self, path: str, filter: Request):
        try:
            if (not isinstance(self.methodFilters[path]), array.ArrayType):
                raise TypeError("self.methodFilters[{0}] is not of type Array".format(path))
            self.methodFilters[path].append(filter)
        except KeyError as err:
            logging.debug("Path: {0} was not recognized by the router and the filter could not be added".format(path))
            #TODO implement logging instead of printing

    def _addGlobalFilter(self, filter: Request):
        self.globalFilters.append(filter)
        return self.globalFilters

    

