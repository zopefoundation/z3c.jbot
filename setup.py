from setuptools import find_packages
from setuptools import setup


setup(
    name='z3c.jbot',
    version='2.0',
    description="Drop-in template overrides.",
    long_description=(open('README.rst').read() + "\n" +
                      open('CHANGES.rst').read()),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Zope',
        'Framework :: Zope :: 3',
        'Framework :: Zope :: 5',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='page template override',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/z3c.jbot',
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'setuptools',
        'zope.pagetemplate',
        'zope.component',
        'zope.configuration',
        'zope.security',
        'zope.publisher',
    ],
    extras_require={
        'test': [
            'Zope',
            'Products.BTreeFolder2',
            'Products.CMFCore',
            'plone.resource',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
