---
title: ilabs.client
---
[API reference](api)

There are two levels of API access:

  * low level, implemented by `ILabsApi` class. It
    pretty much mirrors the REST endpoints as documented on [InnodataLabs
    website](http://developer.innodatalabs.com).
  * intermediate level, implemented by
    `ILabsPredctor` class. This class can
    be used to do a file-in => file-out prediction. Most (but not all)
    InnodataLabs endpoints provide this type of prediction.

## Authentication
You need `user_key` secret to access InnodataLabs API endpoints. To obtain
`user_key`, register on
[InnodataLabs developer site](https://developer.innodatalabs.com/login).

You will need to pass this key to client classes explicitly or implicitly.

### Explicit authentication
All client classes allow one to specify `user_key` by passing it as an argument.

For example:
```
from ilabs.aclient.ilabs_api import ILabsApi

api = ILabsApi(user_key='1234567890')
api.ping()
```

### Implicit authentication
If `user_key` is not provided, client will try to look it up following this
logic:

1. Environment variable `ILABS_USER_KEY`
2. User and system configuration files, in this order:
  * `~/.config/ilabs/ilabs.conf`
  * `/etc/ilabs.conf`

Configuration file uses standard format of python `configparser.ConfigParser`.
The value of `user_key` should be specified as option `ilabs_user_key` in
section `[ilabs]`.

Example of configuration file contents:
```
[ilabs]
ilabs_user_key=01234567890
```

## ILabsApi
Low-level access to the InnodataLabs API endpoints. Takes care of the
following concerns:

1. Looks up user authentication key, if not provided explicitly.
2. Modifies request headers to include user authentication key

Example:
```python
api = ILabsApi()
await api.ping()
```

## ILabsPredictor
Implements file-in to file-out process. Takes care of polling for the
asynchronous job status.

Example:
```python
predictor = ILabsPredictor.init(domain='ilabs.bib')

binary_data = b'''<brs:b xmlns:brs="http://innodatalabs.com">
<brs:r>Jack Nadeau and Mike Abukhoff, Continuous Machine Learning, \
Innodata Press, Noida, India</brs:r>
<brs:r>Bill Gates, Microsoft Kills Windows, Finally!, \
Private communication, 2019</brs:r>
</brs:b>
'''

predicted_tagging = await predictor(binary_data, progress=print)

// this will return serialized XML file with predicted tagging
```

