from distutils.core import setup

setup(
    name="feast_custom_offline_store",
    version="0.0.1",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["feast==0.12.1"],
)
