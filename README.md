Patcher-server
==============

A generic patcher system

This is a django module


Installation
============

You need to add in your settings.py

    INSTALLED_APPS = (
        'Patcher'
    )

In your urls.py

    urlpatterns = patterns('',
        url(r'^patcher/', include('Patcher.urls')),
    )

You can change "patcher" if you want.



Usage
=====


urls
----


* \<soft name\> = [\w-]+
* \<version\>   = [\d]+.[\d]+.[\d]+  (major.minor.patch)
* \<bit\>   = 32 or 64
* \<os\>    = [\w-]+
* \<file\>  = [\w.-]+

```Python
"get/<soft name>/<version>/<os>-x<bit>/(<file>)?" #return a .zip with all the file for this version (if file is not empty, anly this file is send)
"maj/<soft>/<version>/(last|<version>)/<os>-x<bit>.json" #return a json with all maj to mak to go to the specified version
"push/" #send files to the server to creat a new version. This url is only uses with Patcher-send script. It use post params
"list/" #list of all the soft
"<soft>/list/" #list of all the version of a soft
```


You also have a script to upload a new soft.
The soft name have to existe in the database.

usage:
    Patcher-send.sh <exe> <url:port> <path/to/requirement.txt>


Requirement
===========

For the script only:
    * Monitoring-info in your path (https://github.com/Krozark/monitoring)
    * gen-requirement.sh (if you do not put yours) (https://github.com/Krozark/gen-requirement)

you can replace it by whatever you want, but the output must contain:
	* osName: <value>
	* osBit: <value>


