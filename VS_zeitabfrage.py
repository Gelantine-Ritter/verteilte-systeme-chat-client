import socket
import sys
from datetime import datetime



server_name=name=sys.argv[1]
port_number=int(sys.argv[2])

#create socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket erfolgreich erstellt')
except socket.error as err:
    print ('Socket nicht erstellt, Error: ', err) 

#connection 
try:
    s.connect((server_name, port_number))
    print ('Verbunden')
    try:
        print('\nIP-Adresse des Kommunikationspartners '+server_name+': ' + socket.gethostbyname(server_name) + ':'+str(port_number)+'\n')
    except socket.gaierror:
        print('Hostname kann nicht ermittelt werden')
        sys.exit()
except socket.error as msg:
    print ('Nicht verbunden')

#send message
try:
    request = 'dslp-3.0\r\nrequest time\r\ndslp-body\r\n'
    s.send(bytes(request.encode('utf-8')))
except socket.error:
    print ('Senden nicht möglich')
    sys.exit()

#server response
response = (s.recv(1024).decode('utf-8'))
server_response=format(response)
print ('Antwort des Servers:\n'+server_response)

split_request=request.split('\r\n')
split_response=response.splitlines()

#server date
if split_response[0] == split_request[0] and split_response[0] == split_request[0] and split_response[0] == split_request[0]:
    
    server_date=split_response[3] 
    final_split=server_date.split('T')

    s_date=final_split[0]
    s_time_split=final_split[1]
    s_time=s_time_split.replace('+00:00','+0000')

    final_date=datetime.strptime(s_date, '%Y-%m-%d')
    final_time=datetime.strptime(s_time, '%H:%M:%S%z')

    date_output=final_date.strftime('%a %b %d')+final_time.strftime(' %H:%M:%S %Z')+final_date.strftime(' %Y')

    print('Aktuelle Zeit auf dem Server: '+date_output)
else:
    print('Server antworet nicht: Überprüfe deine Nachricht!')

s.close()
