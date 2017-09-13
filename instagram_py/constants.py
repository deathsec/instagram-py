# Intagram-py , Copyright (C) 2017 The Future Shell , DeathSec
# filename : constants.py
# Useful constants most needed for Instagram-py

appInfo = { # App information that are useful
    "version"     : "0.3.2", # semver!
    "name"        : "Instagram-py",
    "description" : " Simple Instagram brute force attacker script",
    "author"      : "The Future Shell , DeathSec",
    "year"        : "2017",
    "example"     : "example: instagram-py -v instatestgod__ rockyou.txt"
}

app_error = {
    "no_config"         : "\nIntagram-py::error: cannot open config file -> instapy-config.json",
    "invalid_config"    : "\nInstagram-py::error: invalid json in config file -> instapy-config.json",
    "magic_fail"        : "\nInstagram-py::error: cannot get the magic cookie!",
    "tor_down"          : "\nInstagram-py::fatal error: cannot connect to tor server , check your config file!",
    "no_file_p"         : "\nInstagram-py::fatal error: cannot find password list file!",
    "user_cancel"       : "\nInstagram-py::error: attack canceled by the user!",
    "invalid_p_file"    : "\nInstagram-py::error: if you resume the attack please use the same password list file!",
    "no_pass_in_p_file" : "\n[-] Sorry , correct password was not present in the file!"
}

current_session = { # session configuration , very important
    "username"             : "", # empty entries are left in purpose
    "passwordFile"         : "",
    "checkpoint"           : "",
    "save"                 : "none",
    "start"                : "now",
    "proceedWith"          : False,
    "resume"               : False,
    "password_file_length" : -1,
    "progress_status"      : "none",
    "tor_controller"       : "none", # the tor openned controller comes here!
    "bot"                  : "none", # requests session
    "magic_cookie"         : "", # the authentication cookie for instagram api v1
    "verbose"              : -1,
    "config"               : "none" # master configuration 
}
