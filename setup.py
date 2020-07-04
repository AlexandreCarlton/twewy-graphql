from setuptools import setup, find_packages

setup(
    name='twewy',
    version='0.0.1',
    description='The World Ends With You GraphQL endpoint',
    author='Alexandre Carlton',
    packages=find_packages(),
    python_requires='>=3.6.0',
    install_requires=[
        'graphene-sqlalchemy==2.3.0.dev1',
        'Flask-GraphQl==2.0.1',
        'xmltodict==0.12.0'
    ]
)




