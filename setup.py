import sys
from setuptools import setup, Extension, find_packages

def get_sno4py_extension():
    """Defines the C-backend extension module."""

    if sys.platform == "win32":
        extra_compile_args = [
            '/O2',
            '/W3',
            '/std:c11',        # C11 mode: stdbool, stdint, mixed decls
            '/wd4244',         # conversion warnings (size_t ↔ int)
            '/wd4267',         # size_t → int conversion
            '/wd4996',         # deprecation warnings
        ]
        extra_link_args = []
    else:
        extra_compile_args = [
            '-O3',
            '-std=c11',
            '-Wno-sign-compare',
            '-Wno-unused-function',
            '-Wno-unused-variable',
        ]
        extra_link_args = []

    return Extension(
        name="sno4py",
        sources=[
            "src/sno4py/src/sno4py.c",
            "src/sno4py/src/spipat.c",
            "src/sno4py/src/image.c",
            "src/sno4py/src/image_strs.c",
            "src/sno4py/src/spipat_stubs.c",
        ],
        include_dirs=["src/sno4py/src"],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )

setup(
    name="SNOBOL4python",
    version="0.5.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=[get_sno4py_extension()],
    include_package_data=True,
)