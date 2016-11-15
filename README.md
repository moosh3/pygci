# pygci

[![PyPI version](https://badge.fury.io/py/pygci.svg)](https://badge.fury.io/py/pygci)

```pygci``` is a thin Python library allowing easy access to Google's Civic Information API.

### Features

- Query data for:
  - Available elections
  - Information relevant to a voter based on their registered address
  - Political geography and representative information via address

- OAuth 1 and 2 support
- Seamless Python 3 support


### Installation

You can install ```pycgi``` via [pip](https://www.pip-installer.org)

```
$ pip install pygci
```

or, with [easy_install](http://pypi.python.org/pypi/setuptools)

```
$ easy_install pycgi
```

Or, to grab the current Github code

```
$ git clone https://github.com/aleccunningham/pygci.git
$ cd pygci
$ python setup.py install
```

### Documentation

You can check out the docs at https://pygci.readthedocs.io/en/latest

#### Representatives

- Levels:
    
    A list of office levels to filter queryes by. Only offices
    that serve at least one of these levels will be returned.
    Divisions that don't contain a matching office will not be
    returned.

    - ```administrativeArea1```
    - ```administrativeArea2```
    - ```country```
    - ```international```
    - ```locality```
    - ```regional```
    - ```special```
    - ```subLocality1```
    - ```subLocality2```

- Roles:

    A list of office roles to filter queries by. Only offices
    fufilling one of these roles will be returned. Divisions that
    don't contain a matching office will not be returned.

    - ```deputyHeadOfGovernment```
    - ```executiveCouncil```
    - ```governmentOfficer```
    - ```headOfGovernment```
    - ```headOfState```
    - ```highestCourtJudge```
    - ```judge```
    - ```legislatorLowerBody```
    - ```legislatorUpperBody```
    - ```schoolBoard```
    - ```specialPurposeOfficer```

#### Elections

A list of election IDs can be obtained at https://www.googleapis.com/civicinfo/v2/elections?key=
