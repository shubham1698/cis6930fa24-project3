from setuptools import setup, find_packages

setup(
	name='project3',
	version='1.0',
	author='Shubham Manoj Singh',
	author_email='sh.singh@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources', 'tmp')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']    	
)