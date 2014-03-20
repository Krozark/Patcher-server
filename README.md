Patcher-server
==============

A generic patcher system

This is a django module

Usage
=====

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


