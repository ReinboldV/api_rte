from setuptools import setup

setup(
    name='api_rte',
    version=0.1,
    description='Library RTE API',
    author='Vincent Reinbold',
    author_email='vincent.reinbold@centralesupelec.fr',
    license='GNU GENERAL PUBLIC LICENSE v3',
    packages=['api_rte', 'data'],
    classifiers=["Programming Language :: Python :: 3.6"], install_requires=['requests']
)
