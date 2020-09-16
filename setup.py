import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AI-routesetting", # Replace with your own username
    version="0.0.1",
    author="Frances Hubis",
    author_email="frances.hubis@gmail.com",
    description="Learning MoonBoard boulder problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diskontinuum/AI-routesetting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL-3.0-or-later",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
