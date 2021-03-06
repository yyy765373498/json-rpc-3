2014-07-01 orhideous@gmail.com
------------------------------

* Improved json_datetime_default/json_datetime_hook (support for datetime/date/time)
* Add example for simple TCP server and request proxy

2014-06-27 orhideous@gmail.com
------------------------------

* Now KeyError from dispatcher methods calls handled properly

2014-06-25 orhideous@gmail.com
------------------------------

* Fixed error with ignored serializer/deserializer hooks in dispatcher

2014-06-24 orhideous@gmail.com
------------------------------

* Heavily rewritten core
* Redesigned and refactor your application architecture
* Changed signature internal methods for a more strict adherence to standards
* Fixed tests

2014-06-17 orhideous@gmail.com
------------------------------

* Drop Python 2.x support
* Drop JSON-RPC 1.0 support
* Add datetime serialization/deserialization
* Available json.object_hook
* Code cleanup

2014-05-25 kirill.pavlov@phystech.edu
-------------------------------------

* Add python 2.6 support
* Update server notification processing
* Add functionality to dispatcher, it is possible to init it with
class

2013-11-09  kirill.pavlov@phystech.edu
--------------------------------------

* Add JSON-RPC 1.0 support.
* Add dispatcher for functions.
* Add notification support (separate notification and id=null for
JSON-RPC 2.0 request).
* Add custom json serialize (based on json) with datetime.Datetime
and decimal.Decimal serialization support.
* Move JSONRPC* classes to JSONRPC20*, as far as there is JSONRPC10*.
* Add dispatcher and JSONPRCManager to jsonrpc/__init__, they are no
longer in jsonrpc.jsonrpc module.

2013-10-13  kirill.pavlov@phystech.edu
--------------------------------------

* Add examples of usage.
* Init documentation.
* Remove six from dependencies.

2013-10-08  kirill.pavlov@phystech.edu
--------------------------------------

* Implement JSON-RPC 2.0 specification.
