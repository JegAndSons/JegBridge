from setuptools import setup, find_packages

setup(
    name="JegBridge",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",  # Minimum Python version
)
