from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tidybear',
    version='0.0.0',
    description='A tidy approach to pandas',
    long_description=readme,
    author='Matt Mackenzie',
    author_email='mbm2228@columbia.edu',
    url='https://github.com/mbmackenzie/tidybear',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)