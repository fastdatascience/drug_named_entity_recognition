from distutils.core import setup

with open("README.rst", "r") as fh:
  long_description = fh.read()

setup(
  name = 'drug-named-entity-recognition',
  packages = ['drug_named_entity_recognition'],
  version = '0.1',
  license='MIT', 
  description = 'Finds drug names in a string',
  long_description=long_description,
  author = 'Thomas Wood',
  #author_email = 'thomas@fastdatascience.com',
  url = 'https://fastdatascience.com',   
  keywords = ['drug', 'bio', 'biomedical', 'medical', 'pharma', 'pharmaceutical', 'ner', 'nlp', 'named entity recognition', 'natural language processing'],
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  package_data={'': ['*.csv']},
  include_package_data=True,
)
