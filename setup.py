from setuptools import setup, find_packages

setup(
    name="apknife",
    version='1.0.18',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "apknife=apknife.apknife:main",
        ],
    },
)
