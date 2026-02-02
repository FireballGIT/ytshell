# YTShell Syntax
### The official guide to ```.ytconfig``` files!
---
### What is ```.ytconfig```?

A YouTube configuration file(```.ytconfig```) is a helpful file you can load into YTShell. It's kind of like ```.env``` or ```.toml```, but it's specifically designed for YTShell.

---

### How do you use it?
All YouTube configuration files MUST start with the definition block:
```[DEFINE]```.
This is the header for defining connections. Now, how do you do that? It's simple, like this:
```ytconf
nval rss: sval.endl;
nval id: sval.endl;
nval handle: sval.endl;
nval usn: sval.return;
```
Note that it uses ```.endl;``` to move to the next declaration and uses ```.return;``` to tell the parser that that is the last definition.
```nval``` means "new value".

Now, for actually connecting them, you would do this:
```ytconf
[CONFIG]
val rss = "RSSLinkHere"..endl,
val id = "UC..."..endl,
val handle = "@..."..endl,
val usn = "SuperAwesomeChannel123!"..return,
```
Note that instead of ```.endl;``` and ```.return;```, it uses ```..endl,``` and ```..return,```.

Finally, for the end block:
```[!!END]```

---

### Whole Example File:
```ytconf
[DEFINE]
nval rss: sval.endl;
nval id: sval.endl;
nval handle: sval.endl;
nval usn: sval.return;

[CONFIG]
val rss = "RSSLinkHere"..endl,
val id = "UC..."..endl,
val handle = "@...",
val usn = "SuperAwesomeChannel123!"

[!!END]
```
