from setuptools import setup, find_packages
import os
import sys
#TODO: nltk, spacy data dependency

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of Django requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install django
This will install the latest version of Django which works on your
version of Python. If you can't upgrade your pip (or Python), request
an older version of Django:
    $ python -m pip install "django<2"
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)



with open('README.md') as f:
      readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='ehrkit',
      version='0.1.0',
      description='NLP library for EHR data',
      url='https://github.com/Yale-LILY/EHRKit',
      author='LILY',
      install_requires=[
      	'allennlp',
      	'torch',
      	'numpy',
      	'sklearn',
        'pymysql',
        'sshtunnel',
        'nltk',
        'spacy',
        'gensim',
        'pandas',
        'bert-extractive-summarizer',
        'files2rouge',
        'scipy'
      ],
      # license='MIT',
      packages=['ehrkit', 'external', 'summarizers', 'summarizers.evaluate'],
      license=license,
      long_description=readme
)
