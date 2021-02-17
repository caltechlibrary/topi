Potion<img width="6%" align="right" src="https://github.com/caltechlibrary/potion/raw/main/.graphics/potion-icon.png">
======

Potion (_"**P**ython **o**bjects for **TI**ND **o**peratio**n**s"_) is a Python package for getting basic data from a TIND server.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/potion.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/potion/releases)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

[TIND](https://tind.io) is an [integrated library system](https://en.wikipedia.org/wiki/Integrated_library_system). The Caltech Library uses a hosted solution by TIND for its [library catalog](https://caltech.tind.io).  Recent versions of TIND provide a REST API for getting a subset of information using network calls.  To make writing interfaces and automation scripts in Python easier, the Caltech Library [Digital Library Development team](https://www.library.caltech.edu/staff?&field_directory_department%5B0%5D=754) developed Potion (_"**P**ython **o**bjects for **TI**ND **o**peratio**n**s"_), a Python package that provides an object-oriented interface to data in a TIND catalog.

Potion is not a complete API for interacting with TIND instances.  At this time, it provides an interface for retrieving only  two kinds of objects: bibliographic records, and items/holdings associated with those records.


Installation
------------

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `potion` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `potion` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install potion
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `potion` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/potion.git
```

Usage
-----

Potion is a application programming interface (API) library; it does not offer a command-line interface.  There are three main option classes in Potion: `Tind`, `TindRecord`, and `TindItem`.  The rest of this section describes these classes and how to use them.

### `Tind`

An object of the `Tind` class serves as the main point of interaction with a TIND server.  The constructor for `Tind` takes only one argument: the base network URL for the server.  Using it is very simple:

```python
from potion import Tind

tind = Tind('https://caltech.tind.io')
```

An instance of the `Tind` class offers just two methods: `record`, to create `TindRecord` objects, and `item`, to create `TindItem` objects.  These object classes are described below.


### `TindRecord`

This object class represents a bibliographic record in a TIND database.  The fields of the record are derived from the MARC representation of the bibliographic record in TIND.  The following are the fields in a record object in Potion:

| Field name      | Type   | Description                                             |
|-----------------|--------|---------------------------------------------------------|
| `tind_id`       | string | The TIND record identifier                              |
| `tind_url`      | string | The URL to the online record page in TIND               |
| `title`         | string | The title (derived from MARC data field 245)            |
| `subtitle`      | string | The subtitle (derived from MARC data field 245)         |
| `author`        | string | The author(s) (derived from MARC data field 245 or 100) |
| `edition`       | string | The edition (derived from MARC data field 250)          |
| `year`          | string | The year (extracted from MARC control field 008)        |
| `isbn_issn`     | list   | ISBN or ISSN numbers (from MARC data field 020)         |
| `description`   | string | A description, concatenated from MARC data field 300    |
| `bib_note`      | string | The value of MARC data field 504, subfield "a"          |
| `thumbnail_url` | string | The URL of the cover image in TIND (if any)             |
| `items`         | list   | A list of `TindItem` objects                            |

A `TindRecord` object can be obtained using the factory method `record(...)` on the `Tind` interface object.  This method takes one of two mutually-exclusive arguments: either a TIND record identifier, or a MARC XML string obtained from a TIND server for a TIND bibliographic record.  Here is an example:

```python
from potion import Tind

tind = Tind('https://caltech.tind.io')
rec  = tind.record(tind_id = 680311)
```


### `TindItem`
    
Conceptually, in TIND an "item" is a specific copy of a work; this copy has a barcode and other item-specific information such as a location.  Each item is associated with a TIND record (represented by a `TindRecord` in Potion, described above).  The following are the fields in an item object in Potion:

| Field name    | Type         | Description                                         |
|---------------|--------------|-----------------------------------------------------|
| `parent`      | `TindRecord` | The parent record for this item                     |
| `barcode`     | string       | The item's barcode                                  |
| `type`        | string       | The type of item this is (e.g., "book")             |
| `volume`      | string       | The volume                                          |
| `call_number` | string       | The call number                                     |
| `description` | string       | A description of the specific item (e.g., "copy 1") |
| `library`     | string       | The library where the item is located               |
| `location`    | string       | The location of the item in the library             |
| `status`      | string       | Status of the item listed in TIND                   |

A `TindRecord` object can be obtained using the factory method `item(...)` on the `Tind` interface object.  This method takes a single argument: a barcode.  Here is an example:

```python
from potion import Tind

tind = Tind('https://caltech.tind.io')
rec  = tind.item(35047018228114)
```


Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/potion/issues) for this repository.


Contributing
------------

We would be happy to receive your help and participation with enhancing Potion!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


License
-------

Software produced by the Caltech Library is Copyright (C) 2021, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Acknowledgments
---------------

This work was funded by the California Institute of Technology Library.

The [vector artwork](https://thenounproject.com/term/potion/150643/) of a bottle of potion, used as the icon for this repository, was created by [Lee Mette](https://thenounproject.com/leemette/) from the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/potion/main/.graphics/caltech-round.png">
  </a>
</div>
