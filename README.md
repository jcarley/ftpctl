
### Development

To setup the dev environment run the following commands

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

$ make build

Now you can run the app like it was an executable script

$ ftpctl --help

