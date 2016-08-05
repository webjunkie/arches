# Advanced Production Configurations

## Section Overview

[THIS WHOLE PRODUCTION CONFIGURATION SECTION IS MORE OR LESS APPLICABLE TO V3, SO THERE MAY BE AN OPPORTUNITY TO LINK TO A MORE CENTRAL LOCATION I.E. STORE THESE SECTIONS ELSEWHERE -AC]

[THE FORMATTING HAS NOT YET BEEN CONVERTED FROM .RST -AC]

## Migrating Your Local App to AWS EC2

**Introduction**

If you've been doing your Arches development work locally, on a laptop or desktop computer, you will eventually need to transfer your app to a remote server of some kind in order for it to be served through the internet. This can be done in many different ways, and in this section we'll give a thorough explanation of how to use AWS EC2 with Arches in a `very basic way`. Please look elsewhere for guidance on server administration and maintentance.

**Prerequisites**

A few components must be in place before you are ready to complete these steps.

1. You will need an AWS account, which is just an extension of a normal Amazon account.  `Here's <http://aws.amazon.com/getting-started/>`_ some information on how to get started with AWS. Do not worry about pricing; if you are new to AWS you will be able to do everything listed below for less than $1.

2. You'll need an SSH client in order to access your remote server's command console. We recommend `PuTTY <http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html>`_ as an easy to use, light-weight SSH client. While downloading PuTTY, also be sure to get its companion utility, PuTTYgen (same page).

3. You'll need an FTP client in order to transfer files (your Arches app customizations) to your server. We recommend `FileZilla <https://filezilla-project.org/download.php>`_.

    .. note::
        Advanced users may forego using an FTP client and do all their file transferring by using a GitHub repo to store and maintain their app. This is a much more streamlined method, but has a steeper learning curve.
        
Once you have an AWS account set up, and PuTTY/PuTTYgen and FileZilla installed on your local computer, you are ready to begin.

**#1. Create an EC2 Instance**

From your AWS account console, navigate to the EC2 section. You should get to a screen that looks something like this:

|ec2|

Click on "Launch Instance"

You now have the opportunity to customize your instance before you launch it, and you should see seven steps listed across the top of the page. For our purposes, we only need to worry about a few of them:

* In Step 1, choose "Ubuntu Server 14.04 LTS" as your operating system
* In Step 2, choose t2.micro for the instance type (because it will be free for you)
* In Step 5, tag your server with a name (this is helpful, though not necessary)
* In Step 6, you'll need to:
    * Select "Create a new security group"
    * Name it "arches-security"
    * Modify the rules of this security group to match the following
=================== =====================  ================================  ====================
Type                Protocol               Port Range                        Source
=================== =====================  ================================  ====================
HTTP                TCP                    80                                Anywhere (0.0.0.0/0)
Custom TCP Rule     TCP                    8000                              Anywhere (0.0.0.0/0)
SSH                 TCP                    22                                My IP
=================== =====================  ================================  ====================
        
* In Step 7, click Launch

When you launch the instance, you will be asked to create a new key pair. This is very important. Name it something like "arches-keypair", and download it to an easy-to-access location on your computer. You will use this later to give the SSH and FTP clients access to your server. `Do not misplace this file.`

Once you have launched the instance, click "View Instances" to see your running (and stopped) EC2 instances. The initialization process takes a few moments, so we can leave AWS alone for now and head to the next step.

.. note::
    Your Security Group is the firewall for your server. Each rule describes a specific type of access to the server, through a specific port, from a specific IP address. `Never` allow access through port 22 to any IP but your own. If you need to access your server from a new location (coffee shop, school) you'll need to update the SSH security rule with your new IP address.

**#2. Convert your AWS .pem Key Pair to a .ppk Key Pair**

PuTTY uses key files in a different format than AWS distributes by default, so you'll have to make a quick conversion:

1. Open PuTTYgen
2. Click Load
3. Find the .pem file that you downloaded when launching your instance (you may have to switch to "All Files (*.*)")
4. Once loaded, click Save
5. Ignore the prompt for a passphrase, and save it with the same name as your original .pem file, now with the .ppk extension.

**#3.Connect to your EC2 Instance with PuTTY**

Now go back to AWS, and look at the status of your server instance. By now, it probably says "2/2 checks passed" in the Status Checks column, and you should have an address (xx.xx.xx.xx) listed in the Public IP column. It's ready!

1. Open PuTTY, and enter your server's Public IP into the Host Name bar.  Make sure Port = 22, and the Connection Type is SSH (remember the security rules we were working with?).
2. To make PuTTY aware of your key file, expand the SSH section in the left pane, and click on Auth. Enter your .ppk file as the "Private key file for authentication".
3. Once you have the IP Address and key file in place, click Open.
4. Click OK to trust the certificate, and login to your server as the default user ``ubuntu``
5. If everything goes well you should be greeted with a screen like this:

|ssh|

Congratulations! You've successfully navigated your way into a functional AWS EC2 instance.

**#4. Install Arches Dependencies on your EC2 Instance**

Now that you have a command line in front of you, the next few steps should be very familiar. Luckily, if you are coming from Windows, you'll find that installing dependencies on Ubuntu is much, much easier. Do all of the following from within the ``/home/ubuntu`` directory (which shows as ~ in the command prompt).

1. Download the install script for dependencies::

    $ wget https://bitbucket.org/arches/arches3/raw/4f8ffdafb043cf2f6ad009d4738e94202eb529dd/arches/install/ubuntu_trusty_setup.sh

2. Run it (this may take a few minutes)::

    $ source ubuntu_trusty_setup.sh

3. Download the pip install script::

    $ wget https://bootstrap.pypa.io/get-pip.py

4. Run it::

    $ sudo python get-pip.py

**#5. Install Arches and Arches-HIP on your EC2 Instance**

Once you have installed all of the Arches dependencies on your server, you should refer back to `this documentation <http://arches-hip.readthedocs.io/en/latest/getting-started/#installating-arches-hip>`_ to complete your Arches installation. However, be sure to stop before step #5, because at that point you will be transferring your existing HIP customizations.

As noted, you should end up with this file structure::

    /home
        /ubuntu
            /Projects
                /ENV

**#6. Connect to your EC2 Instance with Filezilla**

To transfer files from your computer to your EC2 instance, you'll need to use an FTP client. In this case we'll use FileZilla. 

First, we'll need to set up the authentication system to be aware of our AWS key file.

1. Open FileZilla
2. Go to Edit > Settings > SFTP and click Add key file...
3. Navigate to your .ppk file, and open it. You'll now see you file listed.
4. Click OK to close the Settings

Next, you can use the "Quickconnect" bar:

* Host = your server's Public IP
* Username = ubuntu
* Password = <leave blank> (that's what the .ppk file is for)
* Port = 22

Once connected, you'll see your server's file system on the right side, and your local file system on the left. Find your local "my_hip_app" directory, and copy the entire directory to ``/home/ubuntu/Projects/``.

Use this command to remove the elasticsearch installation from your new app on the server (because ElasticSearch should be _reinstalled_ on on your server)::

    (ENV)$ sudo rm -r my_hip_app/my_hip_app/elasticsearch

.. note::
    ElasticSearch is already installed within your local app, but that installation should not be transferred from your local machine to another operating system and expected to function properly. It may be easier to exclude this directory from the FTP transfer.
        
Now you can run these final commands from the ``/home/ubuntu/Projects/my_hip_app`` directory to complete your app's installation on the server:

1. Install ElasticSearch::

    (ENV)$ python manage.py packages -o setup_elasticsearch

2. Run ElasticSearch::

    (ENV)$ my_hip_app/elasticsearch/elasticsearch-1.4.1/bin/elasticsearch -d
    
3. Install the app::

    (ENV)$ python manage.py packages -o install

4. Run the devserver::

    (ENV)$ python manage.py runserver 0:8000

.. note::
    In this case, explicitly setting the host:port with ``0:8000`` ensures that the server is visible to us when we try to view it remotely.
    
You should now be able to open any web browser and view your app by visiting your IP address like so: http://xx.xx.xx.xx:8000. Now that you have transferred your app to a remote server, its time to use a real production-capable webserver like Apache to serve it (that's how we can get rid of the :8000 at the end of the url).

Keep in mind that you may need to have different values in your settings.py file once you have transferred it to a new operating system (GDAL_PATH, for example). To handle this, use a different settings_local.py file on each installation.

Storing Uploaded Files on AWS Simple Storage Service (S3)
-----------------------------------------

**About S3**

Amazon Simple Storage Service, or S3, is one of the many services available through Amazon Web Services.  S3 can very basically be described as a limitless (for all practical purposes) external hard-drive in the cloud.  It's a simple system that is secure and also cheap.  To read more about S3, check out the `official documentation <http://aws.amazon.com/s3/>`_.

To use S3, you will need an AWS account, which is just an extension of a normal Amazon account.  `Here's <http://aws.amazon.com/getting-started/>`_ some information on how to get started with AWS. 

**Why Use S3 with Arches**

By the time you are in a production environment, you will have configured Arches with a web server, such as Apache or nginx.  While you need a web server to serve the app itself, there are two pieces of the app that can be separated from the web server and served independently. These are the 'static' files (the css, javascript, and logos that are used throughout the app) and the 'media' files (any user uploaded files, such as images or documents).

Many of the existing tutorials are concerned with serving both static and media files, because the more load you can take off of your web server the better. However, there are some advantages to S3 that do not have to do with giving your web server some relief:

    * S3 is cheap: As per the `price chart <http://aws.amazon.com/s3/pricing/>`_, it costs just $.03 per gb/month.  So a database with 10gb of photos will have a media storage cost of $3/month, plus a small amount per transaction ($0.004 per 10,000 GET requests, e.g.).

    * S3 is scalable: You only pay for the amount of data you have stored, and you have no real limit on how much you can store.  This allows for an Arches deployment on a small server, either in-house or a small AWS EC2 or DigitalOcean instance to store hundreds of gigabytes of media--photos, audio, video, documents--without having to restructure to accommodate more data.
    
The main potential drawback is transfer speed to and from the S3 bucket, but that depends most on your what your default storage option is. If you look around, you'll find some comparison articles like `this one <http://www.tomsitpro.com/articles/cost-of-the-cloud-book,2-694-2.html>`_ that may be helpful. 

    .. note::
        You should be able to use S3 regardless of where your app is hosted, whether on an internal server, an AWS EC2 instance, a DigitalOcean droplet, etc.
    
    .. warning::
        We've found that by following the steps below, deleting an Information Resource will *not* automatically remove the file from your S3 bucket. You can manually delete files from the bucket for now, or the intrepid developer may check out the answer to `this question <https://groups.google.com/forum/#!topic/archesproject/QHKqMISRkV8>`_ on the Arches forum.
        
**Steps to Follow**

Having worked through a number of existing tutorials (mostly `here <http://dylanbfox.blogspot.com/2015/01/using-s3-to-serve-and-store-your-django.html>`_, `here <http://martinbrochhaus.com/s3.html>`_, `here <https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/>`_, and `here <http://www.holovaty.com/writing/amazon-s3-media/>`_), we've distilled these steps to show how you can use S3 in conjunction with your Arches app.  Before beginning, you will need to have set up and logged into your AWS account.

**#1. Create some new user credentials for your Arches app**

    The first step is to create some new AWS credentials that your Arches app will use to access the S3 bucket

    #. Access the AWS Identity and Access Management (IAM) Console
    #. Create a new user (named something like "arches_media"), and download the new credentials.  This will be a small .csv file that includes an Access Key ID and a Secret Key.
    #. Also, go to the new user's properties, and record the User ARN

**#2. Create a new bucket on S3**

    Next, you'll need to create a new bucket and give it the appropriate settings.

    #. Create a bucket, named something like "your-app-media"
    #. In the new bucket properties, under Permissions, create a new bucket policy with the following text, inserting your own BUCKET-NAME, and the User ARN for your new user::

        {
            "Statement": [
                {
                  "Sid":"PublicReadForGetBucketObjects",
                  "Effect":"Allow",
                  "Principal": {
                        "AWS": "*"
                     },
                  "Action":["s3:GetObject"],
                  "Resource":["arn:aws:s3:::BUCKET-NAME/*"
                  ]
                },
                {
                    "Action": "s3:*",
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:s3:::BUCKET-NAME",
                        "arn:aws:s3:::BUCKET-NAME/*"
                    ],
                    "Principal": {
                        "AWS": [
                            "USER-ARN"
                        ]
                    }
                }
            ]
        }

    #. Also, make sure that the CORS configuration (click "Add CORS Configuration") looks like this::

        <CORSConfiguration>
            <CORSRule>
                <AllowedOrigin>*</AllowedOrigin>
                <AllowedMethod>GET</AllowedMethod>
                <MaxAgeSeconds>3000</MaxAgeSeconds>
                <AllowedHeader>Authorization</AllowedHeader>
            </CORSRule>
        </CORSConfiguration>

**#3. Update the Virtual Environment**

    In order to configure Arches to use your new bucket, you need to install a couple of extra Django modules in your virtual environment.  These will augment Django's flexibility in how it stores uploaded media.

    #. Once you have activated your virtual environment, use this command::
    
        (ENV) $: pip install boto django-storages

**#4. Update settings.py**    

    Finally, you need to tell your app to use these new modules, give it the necessary credentials, and tell it where to store (and find) the uploaded media.  Open the your settings.py file...
    
    #. Find the line that defines the settings "INSTALLED_APPS" and add 'storages' to it. It should look like this::
    
        INSTALLED_APPS = INSTALLED_APPS + (PACKAGE_NAME,'storages',)
        
    #. Next, add the following lines, replacing the AWS settings values with information from earlier steps (remember the "credentials.csv" file you downloaded?)::
    
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
        AWS_STORAGE_BUCKET_NAME = 'aws_bucket_name'
        AWS_ACCESS_KEY_ID = 'aws_access_key_id'
        AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'
        S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
        MEDIA_URL = S3_URL
        
    #. Restart your web server.
    
You should be good to go!  To test, create a new Information Resource in your installation and upload a file. Now go back to check out your S3 bucket through the AWS console.  Your file should show up in a new folder called files within the bucket.  If you are encountering issues, be sure to let us know on the `forum <https://groups.google.com/forum/#!forum/archesproject>`_.


## Arches Applications

[NOT SURE HOW RELEVANT THIS IS IN V4]

Generally arches applications are installed in a folder directly under the Arches root folder.  You can install as many Arches applications as you like, and they'll all use the same Arches framework and virtual environment.  A typical Arches application installation will therefore look something like this:

    /Projects
        /ENV (virtual environment where the Arches framework is installed)
        /my_arches_app
        /another_arches_app

**Note:**
    If you want to install an existing Arches application, such as the Heritage Inventory Package (HIP), you should stop here and go to: http://arches-hip.readthedocs.org/en/latest/getting-started/#installation.
    
## Docker/AMI/...

## High Availability
