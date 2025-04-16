from setuptools import setup


setup(
    name="z3c.jbot",
    version="3.1.dev0",
    description="Drop-in template overrides.",
    long_description=(
        open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Zope",
        "Framework :: Zope :: 3",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="page template override",
    author="Zope Foundation and Contributors",
    author_email="zope-dev@zope.dev",
    url="https://github.com/zopefoundation/z3c.jbot",
    license="ZPL-2.1",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "setuptools",
        "zope.pagetemplate",
        "zope.component",
        "zope.configuration",
        "zope.security",
        "zope.publisher",
    ],
    extras_require={
        "test": [
            "Zope",
            "Products.BTreeFolder2",
            "Products.CMFCore",
            "plone.resource",
        ],
    },
)
