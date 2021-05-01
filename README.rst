=========
GraphData
=========

..
.. image:: https://img.shields.io/pypi/v/graphdata.svg
        :target: https://pypi.python.org/pypi/graphdata

..
.. image:: https://img.shields.io/travis/whalenpt/graphdata.svg
        :target: https://travis-ci.com/whalenpt/graphdata
..
.. image:: https://readthedocs.org/projects/graphdata/badge/?version=latest
        :target: https://graphdata.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


Wrapper functions for plotting (scientific simulation) data files with matplotlib. 
The primary goal is to essentially be able to plug a filename into a desired matplotlib
graph and have it plot the result rather than to have to load and format the data first.
A secondary goal is be able to 'collect' a group of related data files (such as
data sampled at different times) sharing some common fileID (e.g. data files named
[fileID]_[fileNumber].dat) and be able to plug the fileID into a matplotlib function
wrapper for easy graphing of multiple data files.

* Free software: MIT license
* Documentation: https://graphdata.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
