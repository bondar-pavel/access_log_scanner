from collections import defaultdict
import operator
from optparse import OptionParser
from os import path
import sys


parser = OptionParser()
parser.add_option("-l", "--log_file", dest="apache_log",
                  default="/var/log/httpd/access_log",
                  help="Path to apache access_log file.")
parser.add_option("-t", "--threshold", dest="threshold",
                  default=50, help="If ip address is met in log more than "
                  "this level ip is treaded as malicious.")
parser.add_option("-b", "--block_type", dest="block_type",
                  default="full", help="Type of access limiting to use. "
                  "'http' and 'full' are available for now. 'http' restricts "
                  "access to port 80, 'full' restricts any access. ")

(options, args) = parser.parse_args()

# Exclude local acesses
white_list = ['::1', '127.0.0.1']
block_patterns = {'full': 'iptables -A INPUT -s {} -j DROP',
                  'http': 'iptables -A INPUT -p tcp --dport 80 -s {} -j DROP'}
ip_tables_commands = []
ip_access = defaultdict(int)

if options.block_type not in block_patterns:
    print("'%s' is unknown blocking type, "
          "use 'full' or 'http'" % options.block_type)
    sys.exit(255)

if path.isfile(options.apache_log):
    with open(options.apache_log) as f:
        for line in f:
            ip = line.split(' ')[0]
            ip_access[ip] += 1
    print("IPs met more than %s times in %s" % (options.threshold,
                                                options.apache_log))
    for ip in sorted(ip_access, key=ip_access.get, reverse=True):
        if ip_access[ip] < options.threshold:
            break
        print("%s: %s" % (ip, ip_access[ip]))
        if ip not in white_list:
            pattern = block_patterns[options.block_type]
            ip_tables_commands.append(pattern.format(ip))

    print("To block access to these ips use next command")
    print('\n'.join(ip_tables_commands))
else:
    print("Error! File %s is not found!" % options.apache_log)

