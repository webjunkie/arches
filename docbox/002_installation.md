# Installation

## System Requirements

To begin development or make a test installation of Arches, you will need the following:

**Disk Space**
+ 1.5gb for all dependencies (Postgres/PostGIS, Python, GEOS, etc.)
+ 300mb for all Arches code

In production, the amount of disk space you need will depend on the number of resources in your database, especially any uploaded images or media files.

**Memory (RAM)**
+ 1gb

In production, we advise an increasing your memory to 4-16gb, primarily to support ElasticSearch.

**Operating System**

Arches works on all major operating systems (Linux, Windows, Mac OSX), but installing dependencies will differ from system to system. Most enterprise-level installations of Arches have been created on Linux servers.

---

When viewing Arches, please note that it has been developed for modern browsers.

* Chrome
* Firefox
* Internet Explorer 10 (or higher)
* Safari
* Opera

## Dependencies

Before installing Arches, you must be sure to have these software dependencies on your system.

* PostgreSQL relational database (version 9.5)
* PostGIS (version 2.x) spatial module for PostgreSQL
* Python (version 2.7.6 - there seem to be issues with later versions of python)
* GEOS


These instructions will provide some guidance on installing the required dependencies and getting Arches up and running quickly:

http://arches3.readthedocs.org/en/latest/installing-dependencies-linux/

http://arches3.readthedocs.org/en/latest/installing-dependencies-windows/

## Installing Arches

For basic installations of Arches, v4 now comes with an installation wizard. Just download and run the appropriate installer for your operating system.

[Windows Installer](#installing-arches)

[Mac Installer](#installing-arches)

[Linux Installer](#installing-arches)

To install a devopment version of Arches, please see our [developer documentation](https://github.com/archesproject/arches/wiki).