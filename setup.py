from setuptools import setup, find_packages

setup(
    name='prelims',
    version='0.0.1',
    description='Front matter post-processor for static site generators',
    author='Takuya Kitazawa',
    author_email='k.takuti@gmail.com',
    license='MIT',
    url='https://github.com/takuti/prelims',
    packages=find_packages(exclude=['*tests*']),
    install_requires=['numpy', 'scikit_learn', 'PyYAML'],
)
