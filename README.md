# Client to send and receive metrics

## Interaction protocol

The client communicates with the server with a simple text protocol through a TCP socket.

The protocol supports two types of requests to the server from the client:

- *sending data to save it on the server*

- *getting saved data*

---
<br>

The general format of the client's request:

> `<command> <request data><\n>`

command - the command can take one of two values: put or get

request data - "key name" or "*"

<br>

Example to put data:

> `put server.cpu 23.7 1150864247\n`

<br>

Example to get data from server:

> `get server.cpu\n`

<br>

Command to receive all data:

> `get *\n`

<br>

Request example:

```python
>>> from solution import Client

>>> client = Client("127.0.0.1", 8888, timeout=15)

>>> client.put("server.cpu", 0.5, timestamp=1150864247)

>>> client.put("server.cpu", 2.0, timestamp=1150864248)

>>> client.put("server.cpu", 0.5, timestamp=1150864248)

>>> client.put("server.cpu", 3, timestamp=1150864250)

>>> client.put("server.cpu", 4, timestamp=1150864251)

>>> client.put("server.memory", 4200000)

>>> print(client.get("*"))
```
