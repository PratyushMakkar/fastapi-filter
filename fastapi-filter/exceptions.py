from typing import Optional
from fastapi import APIRouter, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

class FilterAPIRouterError(Exception):

    def __init__(self, router_name: str, msg= None):
        if (msg == None):
            msg = "An Error occured with the filter: {0}".format(router_name)
        super().__init__(msg)
    

class ObjectNotOfTypeRequestError(FilterAPIRouterError):

    def __init__(self, filter_name: str):
        super().__init__(
            self,
            filter_name,
            msg = "The Object: {0} is not of type fastapi.Request and cannot be implemented as a filter"
                .format(filter_name)
        )

class MissingFilterConfigFileError(FilterAPIRouterError):

    def __init__(self, router_name: str):
        super().__init__(
            router_name,
            msg = "Method level configurations file for the  APIRouter class Instance: {0} were not found. Either set useConfig to False or provide a valid configuration file"
            .format(router_name)
        )

class HTTPException(StarletteHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: object = None,
        headers: Optional[dict[str, object]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

def _handleHTTPException(http_exception: StarletteHTTPException):
    return Response(status_code=400)
    '''
    return Response(
        status_code=http_exception.status_code,
        headers= http_exception.headers,
        content= http_exception.detail
    )  
    '''