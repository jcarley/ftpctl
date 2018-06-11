
### Development

The folowing development instructions assume Mac OSX, but they would work on a
Linux machine as well if you adjust accordingly.

To setup the dev environment run the following commands.

#### Prerequisites

Building and developing on OSX

    $ brew install python3

You can develop and build for Linux by using Docker for Mac.  Install
Docker for Mac and follow the instructions below.


#### Option 1 - via Docker (Debian Stretch)

    $ make build
    $ make run
    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install --editable .


#### Option 2 - no Docker (OSX)

    $ virtualenv -p /usr/local/bin/python3 venv
    $ . venv/bin/activate
    $ pip install --editable .


### Building

#### For Linux

    $ make build-linux

#### For OSX

    $ make build-osx

Now you can run the app like it was an executable

    $ dist/osx/ftpctl-darwin-x64 --help

