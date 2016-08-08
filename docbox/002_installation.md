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

## System Architecture
Arches is based on Django and uses Postgres/PostGIS for its database backend. Unlike v3, v4 now stores all resource business data as "tiles" (see below), which are JSON objects in the Postgres database; PostGIS is now only used for auxiliary overlay tables.

![Arches Architecture](img/system-architecture.png)

Each Arches installation includes its own instance of ElasticSearch that resides within the app itself. ElasticSearch is extremely fast and very flexible, allowing adjacent Arches apps to either share clusters or operate completely independent of each other.

In development, the Django webserver can be used to view Arches through a browser. In production, a real webserver (like Apache or nginx) must be used. For more information on configuring Arches for a production environment, please see [this section](#arches-in-production).

[I know all of the distribution architecture hasn't been fully decided, so this can be filled out more and modified at a later date -AC 7/15]

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

### Dev Install

If you'd like to make an Arches installation based on the current repo, you'll need to have pip and git installed on your system. If you don't already have these utilities, you can find pip instructions [here](https://pip.pypa.io/en/latest/installing.html) and git instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Once you have pip and git, just follow these instructions (some syntax may vary based on operating system).

Begin by creating a new directory called `Projects`, and enter it with the command line.

```
$ mkdir Projects && cd Projects
```

Clone the latest version of the official Arches repo.

```
$ git clone http://archesproject/arches.git
```

Install virtualenv, which allows us to develop in a sandboxed Python install with specific dependencies without interfering with the global Python install.

```
$ pip install virtualenv==13.1.2
```

Create a new virtual environment alongside your cloned repo.

```
$ virtualenv ENV
```

You should now have this directory structure:

```
/Projects
    /arches    #this is the cloned repo
    /ENV       #this is the virtual environment
```

Now that you have the virtual environment, you must activate it.

On Linux and OSX:

```
$ source ENV/bin/activate
```

On Windows:

```
> ENV\Scripts\activate
```

Now that the virtual environment is activated, the command line is prefixed with its name (in this case `ENV`). Before we can install Arches into it though, we must change one setting. Create a new file called `settings_local.py` within this directory: `/Projects/arches/arches/` and paste the following code into it.

```
# Override settings.py to installing with Dev mode to get you extra dependencies.
# https://github.com/archesproject/arches/wiki/Setting-up-your-development-environment/
MODE = 'DEV'
```

This `MODE` variable will tell Django to install Arches as a developer, so you are now ready for the actual installation. Use the following commands to do so.

```
(ENV)$ python setup.py install
(ENV)$ python setup.py develop
(ENV)$ python manage.py packages -o setup
```

Once these commands have run successfully, you are ready to [run the Django development server](#running-the-django-development-server) and view your app through a browser.

Extra note: You can optionally install honcho, which will allow us to easily start up Arches and to test changes faster.

```
$ pip install honcho
```

You can use Honcho to assist starting Arches, ElasticSearch and LiveReload:

```
$ honcho start
```

### Running the Django Development Server

Once you have followed the steps outlined for your operating system above, use `python manage.py runserver` to run the Django development server. Open a browser, navigate to localhost:8000, and you will see your Arches app.

If you have Arches installed on a remote server (like an Amazon EC2 instance), you may need to explictly set the host and port like this `python manage.py runserver 0:8000`. Then you can navigate to <your IP or domain>:8000 to view your running Arches instance.

Please skip down to the [production section](#basic-production-configuration) when you are ready to start showing your Arches installation to the world.

## ORIGINAL CONTENT


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

### Install Notes

### Mac OS X