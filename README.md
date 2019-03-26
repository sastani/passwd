###Passwd as a service

# Installation:

## Clone this repository

``` 
git clone https://github.com/sastani/passwd 
```

## Setup a virtual environment (optional, but recommended)
Use a vritual environment to create a seperate development environment, with its own install of Python and packages.

Install virtualenv:

``` 
pip install virtualenv 
``` 

Create a new virtual environment called ``venv``:

``` 
virtualenv venv 
```

Activate the virtual environment:

``` 
source ./venv/bin/activate 
```

## Run the setup script

``` 
python setup.py install
```

## Configure settings 
The program defaults to the ``passwd`` and ``group`` files on a UNIX system (which are located at ``/etc/passwd`` and ``/etc/groups``).
If you are not using OSX or Linux, set ``use_test`` in ``config.toml`` to ``false`` and it will use the test files in the ``files`` subdirectory.
Change the paths in ``[files.test]`` if you would like to use your own files.

## Run!
``` 
python service
```

## Making requests
Requests can be made using ``curl``, an API development tool like ``Postman``, or even your browser.
Since this API only supports ``GET`` requests, these can be made by simply making http requests from your browser.
For example, the following would return all groups.

```
http://localhost:8080/groups

```

