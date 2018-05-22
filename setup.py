import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pycfdns",
    version="0.0.1",
    author="Joakim Sorensen",
    author_email="joasoe@gmail.com",
    description="A module for updating Cloudflare DNS records.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/pycfdns",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)