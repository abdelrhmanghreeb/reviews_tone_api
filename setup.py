from setuptools import setup, find_packages

setup(
    name='Reviews Tone API',
    version='v0.0.1',
    description="An API wrapping Watson's Tone Analyzer and creating Elastic Search index of experimental hotel reviews dataset",
    author='Abdelrahman Mattar',
    author_email='abdelrhmanghreeb@gmail.com',
    license='Proprietary: open source',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: Arabic',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='ES NLP Watson',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'ibm-watson>=4.6.0',
        'pandas',
        'flask',
        'flask_restful',
        'tqdm',
        'elasticsearch',
    ],
    extras_require={
        'test': ['nose2'],
    },
    test_suite='nose2.collector.collector',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'reviews_tone_api=reviews_tone_api.api:run',
        ],
    },
)