from setuptools import setup, find_packages

setup(
    name='filter_api',
    version='0.1.9',
    license='GNU',
    author="Pratyush Makkar",
    author_email='pratyushmakkar@gmail.com',
    packages=find_packages(),
    url='https://github.com/PratyushMakkar/fastapi-filter',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    description="Implement filters for each request path before they are handled by the main function.",
    keywords='fastapi filter Starlette uvicorn',
    install_requires=[
          'fastapi',
          'starlette',
          'uvicorn'
      ],
)