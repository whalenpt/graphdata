from setuptools import setup

with open("README.rst","r") as f:
    long_description = f.read()
exec(open("graphdata/version.py").read())

setup(
        name='graphdata',
        version=__version__,
        description='Wrapper functions for matplotlib utilizing data files',
        long_description=long_description,
        long_description_content_type="text/x-rst",
        url="https://github.com/whalenpt/graphdata",
        author="Patrick Whalen",
        author_email="whalenpt@gmail.com",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        extras_require= {
            "dev": [
                "pytest","twine",
                ],
            },
        packages=["graphdata"],
        package_dir={'.' : 'graphdata'},
        python_requires='>=3.6.0',
        install_requires=["numpy>=1.14.0","matplotlib>=3.0.0"]
)



