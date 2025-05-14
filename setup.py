from setuptools import setup, Extension
import os

ext_modules = [
    Extension(
        "SNOBOL4python.SNOBOL4patterns",
        sources=[os.path.join("src/SNOBOL4python", "SNOBOL4patterns.c")],
    )
]

setup(
    name="src/SNOBOL4python",
    version="0.4.6",
    packages=["SNOBOL4python"],
    ext_modules=ext_modules,
)
