import array
from ast import Raise
from enum import Enum
import logging
import types

from tracemalloc import Filter
from urllib import request



from fastapi import APIRouter, Body, FastAPI, File, Request, Response
from fastapi.utils import generate_unique_id
from fastapi import params
from fastapi.datastructures import Default
import fastapi

from fastapi_filter.utils import checkGlobalFilters, loadFiltersFromFile


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
                assert hasattr(self.methodFilters[key], '__len__'); "The method filter with key: {0} was not of type array".format(key)
                self.methodFilters[key].extend(method_filters[key])

        self.prefix = prefix
        self.enabled = enabled

    def includeFilterOnMethod(self, method: str, filter: types.FunctionType):
        if (hasattr(filter, '__len__')):
            for _filter in filter:
                self.includeFilterOnMethod(method, _filter)
                return
 
        assert isinstance(filter, types.FunctionType); "The implemented filter must be of type: Function"
        if (not method in self.methodFilters):
            self.methodFilters[method] = [filter]
        else:
            _array = self.methodFilters[method]
            assert hasattr(_array, '__len__'); "methodFilters for the path {0} is not of type Array".format(method)
            self.methodFilters[method].append(filter)

        return self

    def InsertMethodLevelFilter(self, filter_classes: array = []) -> Callable:
        def FilteredMethod(function):
            for filter in filter_classes:
                self.includeFilterOnMethod(function.__name__, filter)
        return FilteredMethod

    def includeGlobalFilter(self, filter: types.FunctionType): 
        assert isinstance(filter, types.FunctionType); "The implemented filter must be of type: Function"
        assert hasattr(self.globalFilters, '__len__'); "The global filters for the FilterAPIRouter is not of type Array"
        self.globalFilters.append(filter)
        return self

    

