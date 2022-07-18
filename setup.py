from setuptools import setup, find_packages


setup(
    name='filter_api',
    version='0.1',
    license='MIT',
    author="Pratyush Makkar",
    author_email='',
    packages=find_packages('filter_api'),
    package_dir={'': 'filter_api'},
    url='',
    keywords='Implement request path level filtering for HTTP Requests in FastAPI',
    install_requires=[
          'fastapi',
          'starlette',
          'uvicorn'
      ],

)