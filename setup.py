from setuptools import setup, find_packages
import os

# Safely read the README.md file
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

# Safely read the requirements.txt file
requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = f.read().splitlines()

setup(
    name="apknife",
    version='1.1.8',
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
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "apknife.modules.tools": ["baksmali.jar"],  # Ensure baksmali.jar is included in the package
    },
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "apknife=apknife.apknife:main",
        ],
    },
    zip_safe=False,  # Prevent package compression to ensure access to baksmali.jar
)
