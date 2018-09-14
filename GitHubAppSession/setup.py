from setuptools import setup

setup(
    name="GitHubAppSession",
    author="Matt Morgan",
    author_email="mattmorganpdx@gmail.com",
    description="A GitHub App Session manager",
    version="0.6.1",
    packages=["ghas"],
    include_package_data=True,
    install_requires=["requests", "PyJWT", "cryptography"],
    url="https://github.com/mattmorganpdx/GitHubAppSession",
)
