from setuptools import setup, find_packages

setup(
    name="apknife",
    version="1.0.0",
    author="mrnightmare",
    author_email="hmjani18@gmail.com",
    description="Advanced APK analysis & modification tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/elrashedy1992/APKnife",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "prompt_toolkit",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "apknife=apknife.apknife:main",
        ],
    },
)
