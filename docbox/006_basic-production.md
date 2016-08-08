# Basic Production Configuration

## Basic Production Overview

When you are finished with development on your Arches app, it's time to put it into production. Configurations will differ greatly from project to project, but a few tasks must be handled no matter what:

1. [Switch to a production webserver](#serving-arches-with-apache)
2. [Pass static file handling over the new webserver](#handling-static-files)
3. [Set `DEBUG = False`](#setting-debug--false)

Below are steps for accomplishing these tasks. Please see [this section](#advanced-production-overview) to read about some more complex and efficient production strategies.

## Serving Arches with Apache

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

## Handling Static Files

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

## Setting DEBUG = False

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