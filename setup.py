from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='dataview',
    version='0.1.0',
    description='view HDF5 data through directory tree using plotly and dash',
    long_description=readme,
    url='https://github.com/folk-lab/dataview',
    packages=['dataview'],
    include_package_data=True,
    install_requires = ['h5py','numpy','dash','dash-core-components','dash-html-components']
)
