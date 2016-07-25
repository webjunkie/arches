# Installation

## System Requirements

To begin development or make a test installation of Arches, you will need the following:

**Disk Space**
+ 1.5gb for all dependencies (Postgres/PostGIS, Python, GEOS, etc.)
+ 300mb for all Arches code

In production, the amount of disk space you need will depend on the number of resources in your database, especially any uploaded images or media files.

**Memory (RAM)**
+ 1gb in development

In production, we advise an increase in RAM (to 4-16gb), primarily to support ElasticSearch.

**Operating System**

Arches works on all major operating systems (Linux, Windows, Mac OSX), but installing dependencies and the arches code will differ from system to system. Most enterprise-level installations of Arches have been created on Linux systems.

---

When viewing Arches, please note that it has been developed for modern browsers.

* Chrome
* Firefox
* Internet Explorer 10 (or higher)
* Safari
* Opera

## Dependencies

* PostgreSQL relational database (version 9.5)
* PostGIS (version 2.x) spatial module for PostgreSQL
* Python (version 2.7.6 - there seem to be issues with later versions of python)
* GEOS

These instructions will provide some guidance on installing
the required dependencies and getting Arches up and running quickly:

http://arches3.readthedocs.org/en/latest/installing-dependencies-linux/

http://arches3.readthedocs.org/en/latest/installing-dependencies-windows/

## Installing Arches

[THIS CONTENT HAS NOT YET BEEN ALTERED FROM V3 -AC]

For the installation process you will need **pip** installed on your system. If you don't already have it, you can find instructions to install it here: https://pip.pypa.io/en/latest/installing.html

### Unix

If you have installed the dependencies, you're ready to install Arches.

1. Create the Arches Project folder:

    * Create a folder called 'Projects' (or some other meaningful name) on your system.  

2.  Install virtualenv:

    * Open a command prompt and type:

```
pip install virtualenv==1.11.4
```

    * virtualenv creates a directory with it's own installation of Python and Python executables.

3. Create the ENV folder:

    Navigate to your Projects directory (or wherever you named the root Arches folder) and create your virtual environment with the following command:

        $ virtualenv ENV

4. Install Arches:

    * Activate your virtual environment with the following command:

        * On Linux (and other POSIX systems):

                $ source ENV/bin/activate

        * On Windows:

                \path to 'Projects'\ENV\Scripts\activate

    * You should see the name of your virtual environment in parentheses proceeding your command prompt like so `(ENV)`:

            (ENV)$

    Install Arches (your virtual environment must be activated):

            (ENV)$ pip install arches

That's it, you're done.  You should now have a folder structure that looks like this:

    /Projects
        /ENV
        
### Windows

### Mac OS X

## System Architecture
Arches is based on Django and uses Postgres/PostGIS for its database backend. Unlike v3, v4 now stores all resource business data as "tiles" (see below), which are JSON objects in the Postgres database; PostGIS is now only used for auxiliary overlay tables.

![Arches Architecture](img/system-architecture.png)

Each Arches installation includes its own instance of ElasticSearch that resides within the app itself. ElasticSearch is extremely fast and very flexible, allowing adjacent Arches apps to either share clusters or operate completely independent of each other.

In development, the Django webserver can be used to view Arches through a browser. In production, a real webserver (like Apache or nginx) must be used.

[I know all of the distribution architecture hasn't been fully decided, so this can be filled out more and modified at a later date -AC 7/15]

## Arches Applications

Generally arches applications are installed in a folder directly under the Arches root folder.  You can install as many Arches applications as you like, and they'll all use the same Arches framework and virtual environment.  A typical Arches application installation will therefore look something like this:

    /Projects
        /ENV (virtual environment where the Arches framework is installed)
        /my_arches_app
        /another_arches_app

**Note:**
    If you want to install an existing Arches application, such as the Heritage Inventory Package (HIP), you should stop here and go to: http://arches-hip.readthedocs.org/en/latest/getting-started/#installation.
    
## Docker/AMI/...

## High Availability
