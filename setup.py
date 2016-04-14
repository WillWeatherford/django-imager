"""Setup forDjango Imager app."""
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, 'README.md')) as f:
#     README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#     CHANGES = f.read()

REQUIRES = [
    'django',
    'psycopg2',
]
TEST = [
    'tox',
    'coverage',
    'pytest-cov',
    'factory-boy',
    'django-registration',
]

DEV = [
    'ipython',
]


setup(name='Django Imager',
      version='0.0',
      description='Web application to upload and save images.',
      # long_description=README + '\n\n' + CHANGES,
      author=('Will Weatherford'),
      author_email='weatherford.william@gmail.com',
      url='',
      license='MIT',
      keywords='django',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='django-imager',
      install_requires=REQUIRES,
      extras_require={
          'test': TEST,
          'dev': DEV
      },
      )
