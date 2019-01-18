import os

import sys
from setuptools import setup


if sys.version_info.major < 3:
    sys.exit('Sorry, Python < 3 is not supported')

DIR = os.path.dirname(__file__)
REQUIREMENTS = os.path.join(DIR, 'requirements.txt')


with open(REQUIREMENTS) as f:
    reqs = f.read()

setup(
    name='fc_model',
    version='0.1.0',
    description='sql framework for python',
    license='MIT Licence',
    url='https://github.com/fangqk1991/py-sql',
    author='fang',
    author_email='me@fangqk.com',
    packages=['fc_sql'],
    include_package_data=True,
    platforms='any',
    install_requires=reqs.strip().split('\n'),
)
