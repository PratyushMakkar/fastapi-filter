import array
import json
import traceback
from exceptions import ObjectNotOfTypeRequestError
import fastapi
from fastapi import File

'''
The method ensures that each element of the global filter array 
inherits from fastapi.Request so that it can be called during execution.
'''
def checkGlobalFilters(globalFilters: array) -> array:
    for filter in globalFilters:
        if not isinstance(filter, fastapi.Request):
            raise ObjectNotOfTypeRequestError(filter.__name__)
    return globalFilters

'''
Used to prepare a dictionary of paths and Request class that acts as a filter. 
An input file of type .Json is used and the dictionary should have the following shape. 
{"/path": [array of filters]}
'''
def loadFiltersFromFile(json_file):
    data = json.load(json_file)
    global_filters = []
    method_level_filters = {}
    try:
        global_filters = _prepareClassesFromStringNames(data["global_filters"])
    except KeyError as err:
        print("Missing Key 'global_filters' in {0}".format("JsonFile"))
        print(traceback.print_exception())

    try: 
        method_level_filters_array = data['method_level_filters']
        for item in method_level_filters_array:
            path = item["path"]
            method_level_filters[path] =_prepareClassesFromStringNames(item['filters'])
    except KeyError as err:
        print("Missing Key 'global_filters' in {0}".format("JsonFile"))
        print(traceback.print_exception())
    
    return global_filters, method_level_filters

def _prepareClassesFromStringNames(filters_array_string: array) -> array:
    filtrs_array = []                       #TODO
    return filters_array_string
