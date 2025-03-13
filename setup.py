from setuptools import setup, find_packages
import os

long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f.readlines() if line.strip()]

setup(
    name="apknife",
    version="1.2.0",
    description="APKnife is an advanced tool for APK analysis, modification, and security auditing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mr_nightmare",
    author_email="hmjany18@gmail.com",
    url="https://github.com/elrashedy1992/APKnife",
    project_urls={
        "Homepage": "https://github.com/elrashedy1992/APKnife",
        "Documentation": "https://github.com/elrashedy1992/APKnife/wiki",
        "Source": "https://github.com/elrashedy1992/APKnife",
    },
    license="MIT",
    license_files=["LICENSE"],
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "apknife.modules.tools": ["baksmali.jar"]
    },
    install_requires=requirements if requirements else [],
    entry_points={
        "console_scripts": [
            "apknife=apknife.apknife:main",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Development Status :: 5 - Production/Stable",
    ],
    zip_safe=False,
)
