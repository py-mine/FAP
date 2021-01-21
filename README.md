# FAP - F*cking Awesome Plugins [Decommissioned]
![cod quality](https://www.codefactor.io/repository/github/py-mine/fap/badge) ![code size](https://img.shields.io/github/languages/code-size/py-mine/FAP?color=0FAE6E) ![issues](https://img.shields.io/github/issues/py-mine/FAP) ![build status](https://img.shields.io/github/workflow/status/py-mine/FAP/Python%20application?event=push)

*FAP (F\*cking Awesome Plugins) is a plugin auto-updater, that is also a plugin itself!*

## Features
* Parses a `plugins.yml` file for plugins which have git repositories.
* Auto-updates those plugins (and itself) when the `setup()` coroutine is called.
* Acts just like a plugin, and can be loaded as one (See [the PyMine implementation](https://github.com/py-mine/PyMine/blob/main/pymine/api/__init__.py#L33-L55))

<!--test-->
