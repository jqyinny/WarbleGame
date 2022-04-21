from setuptools import setup

setup(
    name='warble',
    packages=['warble'],
    include_package_data=True,
    install_requires=[
        'flask','flask_sqlalchemy','flask_socketio',
    ],
)