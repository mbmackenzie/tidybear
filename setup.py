from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tidybear',
    version='0.0.3',
    description='A tidier approach to pandas.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Matt Mackenzie',
    author_email='mbm2228@columbia.edu',
    url='https://github.com/mbmackenzie/tidybear',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ]
)