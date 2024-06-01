from setuptools import find_packages, setup

setup(
    name="chkjson",
    version="0.1",
    description="Decode Starcraft's .chk (CHK) format to and from JSON.",
    url="https://github.com/sethmachine/chkjson",
    author="sethmachine",
    author_email="sethmachine01@gmail.com",
    license="MIT",
    install_requires=["dataclass-wizard==0.22.3"],
    package_data={package: ["py.typed"] for package in find_packages()},
    packages=find_packages(),
    zip_safe=False,
)
