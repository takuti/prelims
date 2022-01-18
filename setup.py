from setuptools import setup, find_packages

DISTNAME = 'prelims'
VERSION = '0.0.5'
DESCRIPTION = 'Front matter post-processor for static site generators'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
AUTHOR = 'Takuya Kitazawa'
AUTHOR_EMAIL = 'k.takuti@gmail.com'
LICENSE = 'MIT'
URL = 'https://github.com/takuti/prelims'
DOWNLOAD_URL = 'https://pypi.org/project/prelims/#files'


def setup_package():
    metadata = dict(
        name=DISTNAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        url=URL,
        download_url=DOWNLOAD_URL,
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
            'Topic :: Office/Business :: News/Diary',
            'Topic :: Software Development',
            'Topic :: Text Processing :: Markup',
            'Development Status :: 3 - Alpha',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9'
        ],
        packages=find_packages(exclude=['*tests*']),
        python_requires='>=3.7',  # follow sklearn
        install_requires=['numpy>=1.14.6', 'scikit_learn>=1.0', 'PyYAML>=5.1'],
    )

    setup(**metadata)


if __name__ == '__main__':
    setup_package()
