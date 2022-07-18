import unittest

from pkg_resources import ResolutionError

from fastapi_filter.filter import FilterAPIRouter

class FilterAPIRouterTests(unittest.TestCase):

    def FilterOne(self):
        pass

    def FilterTwo(self):
        pass

    def FilterThree(self):
        pass

    def RequestPath():
        pass

    def ChainingFiltersTest(self):
        router = FilterAPIRouter(prefix="/")
        (router.includeFilterOnMethod('RequestPath', [self.FilterOne, self.FilterThree])
                .includeGlobalFilter(self.FilterTwo)
        )
        assert(self.FilterTwo in router.globalFilters)
        assert(router.methodFilters == {'RequestPath': [self.FilterOne, self.FilterThree]})

