from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="apknife",
    version='1.1.5',
    description="APKnife is an advanced tool for APK analysis, modification, and security auditing. Whether you're a security researcher, penetration tester, or Android developer, APKnife provides powerful features for reverse engineering, decompiling, modifying, and analyzing APK files.",
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
        "apknife.tools": ["baksmali.jar"],
    },
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "apknife=apknife.apknife:main",
        ],
    },
)
