from setuptools import setup, find_packages

setup(
    name="ckn",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ckn=ckn.main:main",  # This links the command 'ckn' to the main function
        ],
    },
)