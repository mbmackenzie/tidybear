from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tidybear',
    version='0.0.1',
    description='A tidy approach to pandas',
    long_description=readme,
    author='Matt Mackenzie',
    author_email='mbm2228@columbia.edu',
    url='https://github.com/mbmackenzie/tidybear',
    license=license,
    install_requires=[
        "pandas"
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Data Scientists',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ]
)