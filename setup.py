from setuptools import setup

setup(name='eatiht',
      version='0.1',
      description='A tool for extracting article text in html documents.',
      keywords='extract extracted extracting extraction filter filtered filtering remove removed removing removal text textbody body content contents sentence sentences word words boilerplate boilerpipe delete tag tags opening closing main article html hypertext Rodrigo Palacios rodrigo palacios im-rodrigo im_rodrigo',
      url='http://github.com/im-rodrigo/eatiht',
      author='Rodrigo',
      author_email='rodrigopala91@gmail.com',
      license='MIT',
      packages=['eatiht'],
      install_requires=[
          'lxml',
      ],
      zip_safe=False)
