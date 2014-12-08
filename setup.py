import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-admeris-IOP',
    version='0.1',
    packages=['IOPHttpsTransaction'],
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app as library to interface with Admeris IOP for Interac Online.',
    long_description=README,
    author='Michael (MIck) Villeneuve',
    author_email='mrmickca@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	'Topic :: Software Development :: Libraries',
    ],
)
