import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django_user_agreement',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    description='django_user_agreement',
    long_description=README,
    url='https://github.com/Keyintegrity/django_user_agreement',
    author='keyintegrity',
    author_email='uishnk@yandex.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
