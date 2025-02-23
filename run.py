import sh

output = sh.sudo.bash("/etc/wireguard/wireguard-install.sh", _in="1\nUSERNAME\n\n", _out=True, _err=True)
print(output)
