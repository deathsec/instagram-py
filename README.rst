==============
 Instagram-Py 
==============
.. image:: https://img.shields.io/github/issues/deathsec/instagram-py.svg?style=flat-square   
      :target: https://github.com/deathsec/instagram-py/issues

.. image:: https://img.shields.io/github/forks/deathsec/instagram-py.svg?style=flat-square   
      :target: https://github.com/deathsec/instagram-py/network
      
.. image:: https://img.shields.io/github/stars/deathsec/instagram-py.svg?style=flat-square
      :target: https://github.com/deathsec/instagram-py/stargazers

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square   
      :target: https://raw.githubusercontent.com/deathsec/instagram-py/master/LICENSE

..

    | Instagram-py performs slick brute force attack on Instagram without any type of password limiting
    | and also resumes your attack in ease. 
    
    --DeathSec

  
.. image:: https://raw.githubusercontent.com/deathsec/instagram-py/master/preview.png

.. image:: http://forthebadge.com/images/badges/built-with-love.svg
      :target: #
.. image:: http://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg
      :target: #
      
.. image:: http://forthebadge.com/images/badges/made-with-python.svg
      :target: #
|
| **Instagram-Py** is a simple python script to perform basic **brute force** attack against **Instagram** ,   
| this script can **bypass** login limiting on wrong passwords ,  so basically it can test **infinite number of passwords**.
| Instagram-Py is **proved** and can test **over 6M** passwords on a single instagram account with **less resource** as possible
| This script mimics the activities of the official **instagram android app** and sends request over **tor** so you are secure ,
| but if your **tor** installation is **misconfigured** then the blame is on you.

|
**Depends on**: python3 , tor ,  requests , requests[socks] , stem

==============
 Installation
==============

-------------------------------------
 Using Static Compiled Instagram-Py
-------------------------------------   

**For 32 bit Linux users(i386)**

::

 $ sudo wget -O /usr/bin/instagram-py "https://git.io/v5DsL"
 $ sudo chmod +x /usr/bin/instagram-py


**For 64 bit Linux users(x86_64)**

::
 
 $ sudo wget -O /usr/bin/instagram-py "https://git.io/v5Ds3"
 $ sudo chmod +x /usr/bin/instagram-py
 

**If that did not work then use pip to install Instagram-Py, Just follow the instructions bellow!**


::

 $ sudo easy_install3 -U pip # you have to install python3-setuptools
 $ sudo pip3 install requests --upgrade
 $ sudo pip3 install requests[socks]
 $ sudo pip3 install stem
 $ sudo pip3 install instagram-py
 $ instagram-py # installed successfully
 $ # Now lets copy the config file to your hard drive!
 $ cd
 $ # This is the important thing , your configuration lies here!
 $ wget https://raw.githubusercontent.com/deathsec/instagram-py/master/instapy-config.json

------------------------------
    Configuring Instagram-Py
------------------------------

Open your configuration file found in your home directory , this file is **very important**
located at **~/instapy-config.json** , do not change anything except tor configuration

::

 $ vim ~/instapy-config.json # open it with your favorite text editior!

**The configuration file looks like this**

::

 {
  "api-url" : "https://i.instagram.com/api/v1/",
  "user-agent" : "Instagram 10.26.0 Android (18/4.3; 320dp..... ",
  "ig-sig-key" : "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178",
  "ig-sig-version" : "4",
  "tor" : { 
     "server" : "127.0.0.1",
     "port" : "9050",
     "protocol" : "socks5",
     "control" : {
           "password" : "",
           "port" : "9051"
       }
   }
    
 }


**api-url** : do not change this unless you know what you are doing

**user-agent** : do not change this unless you know your stuff

**ig-sig_key** : never change this unless new release, this is extracted from the instagram apk file

**tor** : change everything according to your tor server configuration , do not mess up!

--------------------------------------------
 Configuring Tor server to open control port
--------------------------------------------

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

::

 $ instagram-py your_account_username path_to_password_list


=============
   License
=============

The MIT License,

Copyright (C) 2017 The Future Shell , DeathSec
