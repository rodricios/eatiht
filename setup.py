from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='eatiht',
    version='0.0.9',
    description='A package and script for extracting article text in html documents.',
    keywords='extract extracted extracting extraction filter filtered filtering remove removed removing removal text textbody body content contents sentence sentences word words boilerplate boilerpipe delete tag tags opening closing main article html hypertext Rodrigo Palacios rodrigo palacios im-rodrigo im_rodrigo',
    url='https://github.com/im-rodrigo/eatiht',
    author='Rodrigo',
    author_email='rodrigopala91@gmail.com',
    license='MIT',
    packages=['eatiht'],
    install_requires=[
        'lxml',
        'requests',
    ],
    scripts=['bin/eatiht'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)
