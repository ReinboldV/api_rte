from setuptools import setup
import api_rte
setup(
    name='api_rte',
    version=api_rte.__version__,
    description='Library RTE API',
    author='Vincent Reinbold',
    author_email='vincent.reinbold@geeps.centralesupelec.fr',
    license='GNU GENERAL PUBLIC LICENSE v3',
    packages=['api_rte'],
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=['requests', 'urllib3', 'pandas'],
    test_suite='tests',
)
