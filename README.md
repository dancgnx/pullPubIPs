# pullPubIPs.py

This is a script to list all public IP addresses on all CloudGenix devices

Use python3 to run this code.

pullPubIPs.py looks for the following for AUTH, in this order of precedence:

* --email or --password options on the command line.
* CLOUDGENIX_USER and CLOUDGENIX_PASSWORD values imported from cloudgenix_settings.py
* CLOUDGENIX_AUTH_TOKEN value imported from cloudgenix_settings.py
* X_AUTH_TOKEN environment variable
* AUTH_TOKEN environment variable
* Interactive prompt for user/pass (if one is set, or all other methods fail.)
