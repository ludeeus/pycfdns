"""Setup"""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="pycfdns",
    version="0.1.0",
    author="Joakim Sorensen",
    author_email="ludeeus@gmail.com",
    description="Update Cloudflare DNS A records.",
    install_requires=["aiohttp", "async_timeout"],
    long_description=LONG,
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/pycfdns",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
