__author__ = 'Djidiouf'

# Python built-in modules
import subprocess
import platform
import re

# Third-party modules
##

# Project modules
import modules.connection


def ping(i_hostname):
    timeout = 3  # in seconds
    speed = 0.5
    iteration = 4
    is_ipv6 = False

    # is IPv6?
    if ":" in i_hostname:
        is_ipv6 = True

    if platform.system() == "Windows":
        command = "ping " + i_hostname + " -n " + str(iteration) + " -w " + str(timeout * 1000)  # works for ipv4 or 6
    else:
        if is_ipv6:
            command = "ping6 " + i_hostname + " -i " + str(speed) + " -c " + str(iteration) + " -W " + str(timeout)
        else:
            command = "ping " + i_hostname + " -i " + str(speed) + " -c " + str(iteration) + " -W " + str(timeout)

    process = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
    matches = process.stdout.read()

    if matches:
        results = matches.decode('utf-8')  # Decode bytes
        results = results.splitlines()  # Split string when \n \r\n is detected
        return results
    else:
        results = ["An error occurred"]
        return results


def main(i_string):
    ping_results = ping(i_string)

    for e in ping_results:
        if e == "" \
                or e.startswith("PING") or e.startswith("---") \
                or e.startswith("Pinging") or e.startswith("Approximate") or e.startswith("Ping statistics"):
            continue
        else:
            modules.connection.send_message(e)
