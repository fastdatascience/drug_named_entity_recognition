import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'drug-named-entity-recognition',
    author="Thomas Wood",
    author_email="thomas@fastdatascience.com",
    description='Drug Named Entity Recognition library to find and resolve drug names in a string (drug named entity linking)',
    keywords= ['drug', 'bio', 'biomedical', 'medical', 'pharma', 'pharmaceutical', 'ner', 'nlp', 'named entity recognition', 'natural language processing', 'named entity linking'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://fastdatascience.com/drug-named-entity-recognition-python-library",
    project_urls={
        "Documentation": "https://fastdatascience.com/drug-named-entity-recognition-python-library",
        "Bug Reports": "https://github.com/fastdatascience/drug_named_entity_recognition/issues",
        "Source Code": "https://github.com/fastdatascience/drug_named_entity_recognition",
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": ["check-manifest"],
        # 'test': ['coverage'],
    },
    package_data={'': ['*.csv']},
    include_package_data=True,
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)
