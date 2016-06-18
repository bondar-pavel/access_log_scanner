=======================================
Apache access_log scanner
=======================================

A simple python script to scan apache access_log for frequently met ip addresses
(attacker ips) and build iptables commands to block them.

* Free software: MIT License


What does it do?
----------------

If your site is under attack, this script will help you to identify attacker's
ips and block them via iptables. You need to point the script to access_log and
set a threshold. If some ip is met in access_log more than the threshold
it is treated as the attacker ip.

The script generates iptables commands to block attacker ips. Two types of
access limitation for attacker ips are currently supported: 'full' and 'http'.
By default 'full' is used, it blocks any access from the attacker ip.
'http' blocks only the port 80 for the attacker ip.


Installation
------------

Clone repository:

::

  $ git clone https://github.com/bondar-pavel/access_log_scanner


Usage
-----

Once repository is cloned script is ready for use.

::

  $ cd access_log_scanner
  $ python access_log_scanner.py -h
  Usage: access_log_scanner.py [options]

  Options:
    -h, --help            show this help message and exit
    -l APACHE_LOG, --log_file=APACHE_LOG
                          Path to apache access_log file.
    -t THRESHOLD, --threshold=THRESHOLD
                          If ip address is met in log more than this level ip is
                          treated as malicious.
    -b BLOCK_TYPE, --block_type=BLOCK_TYPE
                          Type of access limitation to use. 'http' and 'full' are
                          available for now. 'http' restricts access to port 80,
                          'full' restricts any access.

Default values for options are the following:

::

  $ python access_log_scanner.py -l /var/log/httpd/access_log -t 50 -b full

Due to default values this is effectively the same:

::

  $ python access_log_scanner.py

An example of the script output for the analysed acces_log file
from the real site under attack.
It was taken from my website http://pitank.com:

::

  $ python access_log_scanner.py -l ~/access_log -t 100
  IPs met more than 100 times in /home/pavel/access_log
  104.233.88.236: 64015
  64.137.235.207: 45653
  64.137.235.218: 42814
  52.28.202.161: 5306
  ::1: 795
  86.57.255.92: 738
  151.80.14.133: 512
  86.57.255.91: 304
  191.96.249.54: 229
  69.10.153.124: 185
  86.57.255.90: 167
  115.146.123.157: 100
  To block access to these ips use next command
  iptables -A INPUT -s 104.233.88.236 -j DROP
  iptables -A INPUT -s 64.137.235.207 -j DROP
  iptables -A INPUT -s 64.137.235.218 -j DROP
  iptables -A INPUT -s 52.28.202.161 -j DROP
  iptables -A INPUT -s 86.57.255.92 -j DROP
  iptables -A INPUT -s 151.80.14.133 -j DROP
  iptables -A INPUT -s 86.57.255.91 -j DROP
  iptables -A INPUT -s 191.96.249.54 -j DROP
  iptables -A INPUT -s 69.10.153.124 -j DROP
  iptables -A INPUT -s 86.57.255.90 -j DROP
  iptables -A INPUT -s 115.146.123.157 -j DROP


Analysis of script output can provide more clear understanding of what ips
belong to attackers. See top 3 ips, they are met more than 40.000 times in
access_log, so they are clearly recognized as attackers.
Then script parameters can be adjusted to generate iptables commands for them only:

::

  $ python access_log_scanner.py -l ~/access_log -t 10000
  IPs met more than 10000 times in /home/pavel/access_log
  104.233.88.236: 64015
  64.137.235.207: 45653
  64.137.235.218: 42814
  To block access to these ips use next command
  iptables -A INPUT -s 104.233.88.236 -j DROP
  iptables -A INPUT -s 64.137.235.207 -j DROP
  iptables -A INPUT -s 64.137.235.218 -j DROP

