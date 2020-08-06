

import setuptools


setuptools.setup(

    name="cryptotrackerbot",
    version="1",

    license="AGPL-3.0",

    author="Dario 91DarioDev",
    author_email="dariomsn@hotmail.it",

    install_requires=[
        "python-telegram-bot",
        "requests",
        "matplotlib",
        "image"
    ],

    packages=[
        "cryptotrackerbot",
    ],

    entry_points={
        "console_scripts": [
            "cryptotrackerbot = cryptotrackerbot.__main__:main",
        ],
    },

    include_package_data=True,
    zip_safe=False,

    classifiers=[
        "Not on PyPI"
    ],

)
