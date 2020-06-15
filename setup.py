import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="octocruncher", # Replace with your own username
    version="0.1.0",
    author="Trevor Gross",
    author_email="tgross@intrepidcs.com",
    description="A simple package to implement the Octopart API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tgross35/octocruncher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
