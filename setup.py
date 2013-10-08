from setuptools import setup, find_packages

from state_field import __version__

install_requires = [
    'Django>=1.4.2',
    'mock==1.0.1',
]

setup(
    name='django-state-field',
    version=__version__,
    description='Django custom field for changing states',
    author='iMom0',
    author_email='mobeiheart@gmail.com',
    url='https://github.com/imom0/django-state-field',
    license='BSD',
    test_suite="runtests.runtests",
    test_requirements=['mock==1.0.1'],
    package_dir={'': 'state_field'},
    packages=find_packages('state_field'),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ]
)
