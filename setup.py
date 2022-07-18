from setuptools import setup, find_packages


setup(
    name='filter_api',
    version='0.1.4',
    license='MIT',
    author="Pratyush Makkar",
    description_file = "README.md",
    author_email='',
    packages=find_packages(),
    url='',
    keywords='Implement request path level filtering for HTTP Requests in FastAPI',
    install_requires=[
          'fastapi',
          'starlette',
          'uvicorn'
      ],

)