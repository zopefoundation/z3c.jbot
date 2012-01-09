from setuptools import setup, find_packages

version = '0.7.1'

setup(name='z3c.jbot',
      version=version,
      description="Drop-in template overrides.",
      long_description="\n".join(
          (open("README.txt").read(), open("CHANGES.txt").read())),
      classifiers=[
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        ],
      keywords='page template override',
      author='Malthe Borch',
      author_email='mborch@gmail.com',
      url='',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['z3c'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.pagetemplate',
          'zope.component',
          'zope.configuration',
          'zope.security',
          'zope.publisher',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
