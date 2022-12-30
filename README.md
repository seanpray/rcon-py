### Barebones rcon implementation in python

Example usage:
Both the timeout and port are optional arguments, default port is 25565 and timeout is 15 seconds
```
# host, port, timeout in ms
c = Client("0.0.0.0", 1200, timeout_ms=100)
# must be authenticated to send a message
c.auth("pass")
print(c.send("list").body)
```

#### install

```
$ pip install git+https://github.com/notseanray/rcon-py.git#egg=rcon_py
```
