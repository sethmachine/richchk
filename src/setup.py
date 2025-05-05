from setuptools import find_packages, setup

_PACKAGE_DATA = {package: ["py.typed"] for package in find_packages()}
_PACKAGE_DATA["richchk"] = [
    "mpq/stormlib/dlls/macos/*.*",
    "mpq/stormlib/dlls/windows/x64/*.*",
    "mpq/stormlib/dlls/linux/*.*",
]

setup(
    name="richchk",
    version="0.1",
    description="Parse Starcraft CHK format into a rich, readable, and editable format.",
    url="https://github.com/sethmachine/richchk",
    author="sethmachine",
    author_email="sethmachine01@gmail.com",
    license="MIT",
    install_requires=["dataclass-wizard==0.22.3", "PyYAML==6.0.1", "mutagen==1.47.0"],
    package_data=_PACKAGE_DATA,
    packages=find_packages(),
    zip_safe=False,
)
