Topi<img width="11%" align="right" src="https://github.com/caltechlibrary/topi/raw/main/.graphics/topi-icon.png">
======

Topi (_"**T**IND **O**bject **P**ython **I**nterface"_) is a Python package for getting basic data from a TIND server.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/topi.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/topi/releases)
[![DOI](https://img.shields.io/badge/dynamic/json.svg?label=DOI&style=flat-square&colorA=gray&colorB=navy&query=$.metadata.doi&uri=https://data.caltech.edu/api/record/1890)](https://data.caltech.edu/records/1890)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![PyPI](https://img.shields.io/pypi/v/topi.svg?style=flat-square&color=orange)](https://pypi.org/project/topi/)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

[TIND](https://tind.io) is an [integrated library system](https://en.wikipedia.org/wiki/Integrated_library_system). The Caltech Library uses a hosted solution by TIND for its [library catalog](https://caltech.tind.io).  Recent versions of TIND provide a REST API for getting a subset of information using network calls.  To make writing interfaces and automation scripts in Python easier, the Caltech Library [Digital Library Development team](https://www.library.caltech.edu/staff?&field_directory_department%5B0%5D=754) developed Topi (_"**T**IND **O**bject **P**ython **I**nterface"_), a Python package that provides an object-oriented interface to data in a TIND catalog.

Topi is not a complete API for interacting with TIND instances.  At this time, it provides an interface for retrieving only  two kinds of objects: bibliographic records, and items/holdings associated with those records.

A "topi" is also a [species of antelope](https://en.wikipedia.org/wiki/Topi) found in Africa.  The topi is currently classified as [_vulnerable_](https://en.wikipedia.org/wiki/Vulnerable_species) by the [International Union for Conservation of Nature](https://www.iucn.org) (IUCN) due to [threats](https://www.iucnredlist.org/species/6235/50185422) that include human development, hunting and droughts.


Installation
------------

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `topi` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `topi` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install topi
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `topi` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/topi.git
```

Usage
-----

Topi is a application programming interface (API) library; it does not offer a command-line interface.  There are three main option classes in Topi: `Tind`, `TindRecord`, and `TindItem`.  The rest of this section describes these classes and how to use them.

### Object classes

#### `Tind`

An object of the `Tind` class serves as the main point of interaction with a TIND server.  The constructor for `Tind` takes only one argument: the base network URL for the server.  Using it is very simple:

```python
from topi import Tind

tind = Tind('https://caltech.tind.io')
```

An instance of the `Tind` class offers just two methods: `record`, to create `TindRecord` objects, and `item`, to create `TindItem` objects.  These object classes are described below.


#### `TindRecord`

This object class represents a bibliographic record in a TIND database.  The fields of the record are derived from the MARC representation of the bibliographic record in TIND.  The following are the fields in a record object in Topi:

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

A `TindRecord` object can be obtained using the factory method `record(...)` on the `Tind` interface object.  This method takes one of two mutually-exclusive keyword arguments: either a TIND record identifier, or a MARC XML string obtained from a TIND server for a TIND bibliographic record.  Here is an example:

```python
from topi import Tind

tind = Tind('https://caltech.tind.io')
rec  = tind.record(tind_id = 680311)
```

Note the use of the keyword argument.  Below is an example of how to create a record from an existing MARC XML file obtained from a TIND server some other way &ndash; let's assume it is stored a file named `downloaded-marc.xml`:

```python
from topi import Tind

with open('downloaded_marc.xml', 'r') as xf:
    xml_string = xf.read()

tind = Tind('https://caltech.tind.io')
rec  = tind.record(marc_xml = xml_string)
```

The `thumbnail_url` field is lazily evaluated: its value is only obtained from the TIND server the first time the field is accessed by a calling program.  This is more efficient for situations where the thumbnail is never needed by an application, but it does mean that there is a delay the first time the field is accessed.


#### `TindItem`
    
Conceptually, in TIND an "item" is a specific copy of a work; this copy has a barcode and other item-specific information such as a location.  Each item is associated with a TIND record (represented by a `TindRecord` in Topi, described above).  The following are the fields in an item object in Topi:

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

With Topi, a `TindItem` object can be obtained using the factory method `item(...)` on the `Tind` interface object.  This method takes a single argument: a barcode.  Here is an example:

```python
from topi import Tind

tind = Tind('https://caltech.tind.io')
item = tind.item(35047018228114)
```

Item records have parent pointers to the corresponding bibliographic record, in the form of a `TindRecord`.  Thus, given an item object, it's possible to look up the rest of the bibliographic record simply by dereferencing the `.parent` field:

```python
from topi import Tind

tind = Tind('https://caltech.tind.io')
item = tind.item(35047018228114)
print(item.parent.title)
```

Calling the `item` method on `Tind` will return an empty `TindItem` object.


### Additional notes

Topi fills out the `thumbnail_url` field of a `TindRecord` object by using TIND's API for the purpose.  This only retrieves what a given TIND database contains for the cover image of a work.  Other sources such as the [Open Library Covers API](https://openlibrary.org/dev/docs/api/covers) may have cover images that a TIND database lacks, but it is outside the scope of Topi to provide an interface for looking outside the TIND database.


Known issues and limitations
------------------------------

Currently, the coverage of the fields in `TindRecord` is limited.  Not all fields of a MARC XML record are mapped to fields in `TindRecord` at this time.  (Code contributions are welcome!)


Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/topi/issues) for this repository.


Contributing
------------

We would be happy to receive your help and participation with enhancing Topi!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


License
-------

Software produced by the Caltech Library is Copyright (C) 2021, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Acknowledgments
---------------

This work was funded by the California Institute of Technology Library.

The [vector artwork](https://thenounproject.com/term/antelope/931009/) of an antelope, used as the icon for this repository, was created by [parkjisun](https://thenounproject.com/naripuru/) for the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

Topi makes use of numerous open-source packages, without which Topi could not have been developed.  I want to acknowledge this debt.  In alphabetical order, the packages are:

* [commonpy](https://github.com/caltechlibrary/commonpy) &ndash; a collection of commonly-useful Python functions
* [cssselect](https://pypi.org/project/cssselect/) &ndash; `lxml` add-on to parse CSS3 selectors 
* [ipdb](https://github.com/gotcha/ipdb) &ndash; the IPython debugger
* [lxml](https://lxml.de) &ndash; an XML parsing library for Python
* [setuptools](https://github.com/pypa/setuptools) &ndash; library for `setup.py`
* [sidetrack](https://github.com/caltechlibrary/sidetrack) &ndash; simple debug logging/tracing package


<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/topi/main/.graphics/caltech-round.png">
  </a>
</div>
