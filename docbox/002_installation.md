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

Arches works on all major operating systems (Linux, Windows, Mac OSX), but installing dependencies will differ from system to system. Most enterprise-level installations of Arches have been created on Linux systems.

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

## Installing Dependencies

Before installing Arches, you must be sure to have these software dependencies on your system.

* PostgreSQL relational database (version 9.5)
* PostGIS (version 2.x) spatial module for PostgreSQL
* Python (version 2.7.6 - there seem to be issues with later versions of python)
* GEOS


These instructions will provide some guidance on installing the required dependencies and getting Arches up and running quickly:

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

### Running the Django Development Server

Once you have followed the steps outlined for your operating system above, use `python manage.py runserver` to run the Django development server. Open a browser, navigate to localhost:8000, and you will see your Arches app.

If you have Arches installed on a remote server (like an Amazon EC2 instance), you may need to explictly set the host and port like this `python manage.py runserver 0:8000`. Then you can navigate to <your IP or domain>:8000 to view your running Arches instance.

## Basic Production Configuration

When you are finished with development on your Arches app, it's time to put it into production. Configurations will differ greatly from project to project, but a few tasks must be handled no matter what:

1. [Switch to a production webserver](#serving-arches-with-apache)
2. [Pass static file handling over the new webserver](#handling-static-files)
3. [Set `DEBUG = False`](#setting-debug--false)

Below are steps for accomplishing these tasks. Please see [this section](#section-overview) to read about some more complex and efficient production strategies.

### Serving Arches with Apache

During development, it's easiest to use the Django webserver to view progress on your app. However, once you are ready to put the app into production, you'll have to use a more efficient webserver like Apache or nginx.

We have the most experience using Apache, which is very easy to install and configure. The following instructions work for Ubuntu 14.04, minor changes may be necessary for a different OS.

---

Get apache2 and the wsgi mod

```
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi
```

In order to properly configure Apache, we must:

1. Create a python daemon process: make python-path to app and to the python virtual environment
2. Set the path to your app's wsgi.py file and reference to the python daemon process created above
3. Give apache access to the necessary directory

All of these tasks are handled by adding a block of code to Apache's `../sites-enabled/000-default.conf` file. Use this command to open the file

```
$ sudo nano /etc/apache2/sites-enabled/000-default.conf
```

and under `<VirtualHost *:80>` paste the following code, changing directory and file paths where necessary:

```
WSGIDaemonProcess arches python-path=/home/ubuntu/Projects/my_hip_app:/home/ubuntu/Projects/ENV/lib/python2.7/site-packages
WSGIScriptAlias / /home/ubuntu/Projects/my_hip_app/wsgi.py process-group=arches

<Directory /home/ubuntu/Projects/my_hip_app/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
```

Use `ctrl+x` to save the file.

We must also give Apache permission to modify one of the app's log files.

```
$ sudo chgrp www-data /home/ubuntu/Projects/my_hip_app/my_hip_app/logs/application.txt
```

Finally, restart Apache.

```
$ sudo service apache2 restart
```

You should now be able to view your app from any web browser by nagivating directly to your IP address. Note that with Apache serving your app, any changes to a .py file will not be reflected in the app until you restart Apache (use the command shown above).

### Handling Static Files

You'll have to set up your static files (all .js and .css files) to be served by your webserver, not by Django. This is because Django will serve your static files while in development, but ceases to do so when you have set DEBUG = False.

---

Create a new directory to hold the static files. Place this within your app, adjacent to the `models` and `templates` directories.

```
$ sudo mkdir /arches/arches/static
```

Now open your `settings.py` file, and add these lines to it:

```
STATIC_ROOT = os.path.join(PACKAGE_ROOT, 'static')
STATIC_URL = "/static/"
```

This will point Django to your new static directory, and also tell it how to create a URL that points to that directory. Now, from within the directory that holds your `manage.py` file, run this command:

```
python manage.py collectstatic
```

Watch as all of or static files are copied to the new directory. Now we are ready to tell Apache where to find them. Use

```
$ sudo nano /etc/apache2/sites-enabled/000-default.conf
```

to open the same configuration file as you modified above. You'll see `<VirtualHost *:80>` at the top and some familiar code below it. Below the original code you added, paste this block, changing paths as necessary.

```
Alias /static/ /srv/crhim/crip/crip/static/

<Directory /srv/crhim/crip/crip/static/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
```

The Alias line tells Apache where to look when Django sends it the `/static/` URL, and the subsequent block allows Apache access to your newly created static directory.

Now restart Apache and you are finished! Note that you must run the `collectstatic` command any time you make any changes to .js or .css files.

### Setting DEBUG = False

Now that you have turned over the webserver responsibilities to a production webserver (in this case, Apache), you are ready for the final step. Open your `settings.py` file, and set `DEBUG = False` (just add that line if necessary). Now restart Apache.

Turning off the Django debug mode will:

1. Suppress the verbose Django error messages in favor of a standard 404 or 500 error page.
2. Cause Django to stop serving static files.

You will now find Django error messages printed in your `logs/application.txt`.

## Arches Applications

[NOT SURE HOW RELEVANT THIS IS IN V4]

Generally arches applications are installed in a folder directly under the Arches root folder.  You can install as many Arches applications as you like, and they'll all use the same Arches framework and virtual environment.  A typical Arches application installation will therefore look something like this:

    /Projects
        /ENV (virtual environment where the Arches framework is installed)
        /my_arches_app
        /another_arches_app

**Note:**
    If you want to install an existing Arches application, such as the Heritage Inventory Package (HIP), you should stop here and go to: http://arches-hip.readthedocs.org/en/latest/getting-started/#installation.