# Meadowlark D5020


[![Meadowlark D5020](https://img.shields.io/pypi/v/meadowlark_d5020.svg)](https://pypi.python.org/pypi/meadowlark_d5020)



Meadowlark D5020 with optional tango server and simulator


Apart from the core library, an optional [simulator](https://pypi.org/project/sinstruments) is also provided.



Apart from the core library, an optional [tango](https://tango-controls.org/) device server is also provided.


## Installation

From within your favorite python environment type:

`$ pip install meadowlark_d5020`

## Library

The core of the meadowlark_d5020 library consists of Meadowlark_d5020 object.
To create a Meadowlark_d5020 object you need to pass a communication object.

The communication object can be any object that supports a simple API
consisting of two methods (either the sync or async version is supported):

* `write_readline(buff: bytes) -> bytes` *or*

  `async write_readline(buff: bytes) -> bytes`

* `write(buff: bytes) -> None` *or*

  `async write(buff: bytes) -> None`

A library that supports this API is [sockio](https://pypi.org/project/sockio/)
(Meadowlark D5020 comes pre-installed so you don't have to worry
about installing it).

This library includes both async and sync versions of the TCP object. It also
supports a set of features like re-connection and timeout handling.

Here is how to connect to a Meadowlark_d5020 controller:

```python
import asyncio

from sockio.aio import TCP
from meadowlark_d5020 import Meadowlark_d5020


async def main():
    tcp = TCP("192.168.1.123", 5000)  # use host name or IP
    meadowlark_d5020_dev = Meadowlark_d5020(tcp)

    idn = await meadowlark_d5020_dev.idn()
    print("Connected to {} ({})".format(idn))


asyncio.run(main())
```


### Simulator

A Meadowlark_d5020 simulator is provided.

Before using it, make sure everything is installed with:

`$ pip install meadowlark_d5020[simulator]`

The [sinstruments](https://pypi.org/project/sinstruments/) engine is used.

To start a simulator you need to write a YAML config file where you define
how many devices you want to simulate and which properties they hold.

The following example exports a hardware device with a minimal configuration
using default values:

```yaml
# config.yml

devices:
- class: Meadowlark_d5020
  package: meadowlark_d5020.simulator
  transports:
  - type: tcp
    url: :5000
```

To start the simulator type:

```terminal
$ sinstruments-server -c ./config.yml --log-level=DEBUG
2020-05-14 16:02:35,004 INFO  simulator: Bootstraping server
2020-05-14 16:02:35,004 INFO  simulator: no backdoor declared
2020-05-14 16:02:35,004 INFO  simulator: Creating device Meadowlark_d5020 ('Meadowlark_d5020')
2020-05-14 16:02:35,080 INFO  simulator.Meadowlark_d5020[('', 5000)]: listening on ('', 5000) (newline='\n') (baudrate=None)
```

(To see the full list of options type `sinstruments-server --help`)





### Tango server

A [tango](https://tango-controls.org/) device server is also provided.

Make sure everything is installed with:

`$ pip install meadowlark_d5020[tango]`

Register a Meadowlark_d5020 tango server in the tango database:
```
$ tangoctl server add -s Meadowlark_d5020/test -d Meadowlark_d5020 test/meadowlark_d5020/1
$ tangoctl device property write -d test/meadowlark_d5020/1 -p address -v "tcp://192.168.123:5000"
```

(the above example uses [tangoctl](https://pypi.org/project/tangoctl/). You would need
to install it with `pip install tangoctl` before using it. You are free to use any other
tango tool like [fandango](https://pypi.org/project/fandango/) or Jive)

Launch the server with:

```terminal
$ Meadowlark_d5020 test
```


## Credits

### Development Lead

* Alberto López Sánchez <alopez@cells.es>

### Contributors

None yet. Why not be the first?
