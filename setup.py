from setuptools import setup, find_packages

setup(
    name="APKnife",
    version='1.0.6',
    description="APKnife is an advanced tool for APK analysis, modification, and security auditing. Whether you're a security researcher, penetration tester, or Android developer, APKnife provides powerful features for reverse engineering, decompiling, modifying, and analyzing APK files.",
    author="Mr_nightmare",
    author_email="hmjany18@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/elrashedy1992/APKnife",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "alembic==1.14.1",
        "androguard==4.1.3",
        "apkInspector==1.3.2",
       
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Homepage": "https://github.com/elrashedy1992/APKnife",
        "Documentation": "https://github.com/elrashedy1992/APKnife/wiki",
        "Source": "https://github.com/elrashedy1992/APKnife",
    },
    entry_points={
        'console_scripts': [
            'apknife = apknife.main:main',  # قم بتعديل المسار إلى وظيفة التنفيذ
        ],
    },
)
