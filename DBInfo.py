host = 'localhost'
dbname = 'sep_project'
user = 'postgres'
password = 'admin'

server = 'uauction.mooo.com'

import getpass
if getpass.getuser() == 'Fujiwara':
    server = 'localhost'

request_get_server_ip = 'https://freedns.afraid.org/dynamic/update.php?V3p2VTJXMmNLbEh0MUMydG5ydzM4NXp0OjE0MzE5MzI5'