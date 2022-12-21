"""Setup"""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="pycfdns",
    version="master",
    author="Joakim Sorensen",
    author_email="hi@ludeeus.dev",
    description="Update Cloudflare DNS records.",
    install_requires=["aiohttp>=3.6.1,<4.0"],
    long_description=LONG,
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/pycfdns",
    packages=setuptools.find_packages(include=["pycfdns", "pycfdns.*"]),
    package_data={"pycfdns": ["py.typed"]},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
