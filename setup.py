import io
import os
from setuptools import setup, find_packages

with io.open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-user-agreement',
    version='0.0.9',
    packages=find_packages(exclude=['project']),
    include_package_data=True,
    description='django-user-agreement',
    long_description=README,
    install_requires=[
        'Django>=1.11,<2.1',
    ],
    url='https://github.com/Keyintegrity/django-user-agreement',
    author='keyintegrity',
    author_email='uishnk@yandex.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
