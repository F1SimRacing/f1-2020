import setuptools

import cassandra

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cassandra",
    version=cassandra.__version__,
    author="Chris Hannam",
    author_email="ch@chrishannam.co.uk",
    description="Display telemetry data and spot anomalies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrishannam/f1-2020",
    packages=setuptools.find_packages(exclude=("tests", "examples", "data")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["f1_2020_telemetry"],
    include_package_data=True,
    entry_points={"console_scripts": ["cassandra-recorder=cassandra.recorder:main",]},
)
