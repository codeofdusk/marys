import setuptools

with open("README.md", "r", encoding="utf-8") as fin:
    long_description = fin.read()

setuptools.setup(
    name="marys",
    version="0.0.1",
    author="Bill Dengler",
    author_email="codeofdusk@gmail.com",
    description="Python library to obtain dining hours and menus at Swarthmore College",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codeofdusk/marys",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
