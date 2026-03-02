from setuptools import setup, Extension, find_packages

def get_sno4py_extension():
    """Defines the C-backend extension module."""
    return Extension(
        name="SNOBOL4python._backend",
        sources=[
            "src/sno4py/src/sno4py.c",
            "src/sno4py/src/spipat.c",
            "src/sno4py/src/image.c",
            "src/sno4py/src/image_strs.c",
            "src/sno4py/src/spipat_stubs.c"
        ],
        include_dirs=["src/sno4py/src"],
        extra_compile_args=['-O3', '-Wno-sign-compare', '-Wno-unused-function']
    )

# The critical call that prevents the 'No distribution was found' error
setup(
    name="SNOBOL4python",
    version="0.5.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=[get_sno4py_extension()],
    include_package_data=True,
)