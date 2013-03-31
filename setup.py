from setuptools import setup, find_packages

install_requires = [
    'Django>=1.4.2',
]

setup(
    name='django-state-field',
    version='0.3',
    description='Django custom field for changing states',
    author='iMom0',
    author_email='mobeiheart@gmail.com',
    url='https://github.com/imom0/django-state-field',
    license='BSD',
    test_suite="runtests.runtests",
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
