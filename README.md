# instagram-py

Instagram-py uses tor to conduct a simple brute force attack on any Instagram account.   
It uses python to bypass bot verification and tor to bypass login limiting,   
As tested Instagram-py tested over 6M passwords on a single account without any limitation.   
**Depends on**: python3 , requests , stem , and colorama.

# Installation   

**You should have tor server up and running**

### Configuring torrc   

**open** your tor configuration file (**/etc/tor/torrc**)   
```
 $ sudo vim /etc/tor/torrc
```

**uncomment** , ControlPort   
**restart your tor server now.**


```
 $ git clone https://github.com/deathsec/instagram-py
 $ cd instagram-py
 $ chmod +x instagram.py
 $ ./instagram.py -vvv account_username path_to_password_list.txt
```

# License   

The MIT License
Copyright (C) 2017 The Future Shell , DeathSec
