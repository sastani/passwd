### Passwd as a service

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
If you are not using OSX or Linux, set ``use_test`` in ``config.toml`` to ``true`` and it will use the test files in the ``files`` subdirectory.
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

## Supported requests
### Note: If an invalid uid or gid is passed (i.e. the uid/gid is a string), the API will return a 400 error. A 400 error will also be returned if any of the fields in a query do not match a valid field name.


**GET /users**

Return a list of all users on the system, as defined in the passwd file.

**GET
/users/query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<
hq>][&shell=<sq>]**

Return a list of users matching all of the specified query fields.

**GET /users/&lt;uid&gt;**

Return a single user with &lt;uid&gt;. Return 404 if `<uid>` is not found.

**GET /users/`<uid>`/groups**

Return all the groups for a given user.

**GET /groups**

Return a list of all groups on the system, a defined by /etc/group.


**GET
/groups/query[?name=<nq>][&gid=<gq>][&member=<mq1>[&member=<mq2>][&.
..]]**

Return a list of groups matching all of the specified query fields

**GET /groups/`<gid>`**

Return a single group with `<gid>`. Return 404 if `<gid>` is not found.

