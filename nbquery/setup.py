from distutils.core import setup
import setuptools

setup(
  name='nbquery',
  version='0.0.1',
  packages=['nbquery'],
  package_dir={'nbquery': 'nbquery'},
  author='Dwayne V Campbell',
  author_email='dwaynecampbell13 _at_ gmail.com',
  description='Used to query NewsBlasters datastore',
  long_description=open('README.md').read(),
  url='http://skillachie.github.io/TBD/',
  download_url='http://pypi.python.org/pypi/TBD',
  keywords='newsblaster,nlp,news,summarization'.split(),
  license='GNU LGPLv2+',
  install_requires=[
    "elasticsearch >= 1.2.0"
    ],
  classifiers=[
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
  'Topic :: Software Development :: Libraries :: Python Modules',
  ]
)
