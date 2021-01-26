import socket
import sys
import threading

#thread methode
def get_response():
    while True:
        response=(s.recv(1024).decode('utf-8'))
        server_response=format(response)
        server_response_split=server_response.split('\r\n')
        print(server_response_split[5])


message_type=['group join\r\n','group notify\r\n', 'group leave\r\n', 'user join\r\n' ]
head='dslp-3.0\r\n'
body='dslp-body\r\n'
group_name='Uebung\r\n'

#request to server function
def request_to_server(message_type_in,group_name_in,s):
    try:
        print('Test')
        request=head+message_type_in+group_name_in+body
        s.send(bytes(request.encode('utf-8')))
    except:
        print('Senden nicht möglich')
        sys.exit()

    response=(s.recv(1024).decode('utf-8'))
    server_response=format(response)
    print('Antwort des Servers:\n'+server_response)
    return server_response

#create socket
def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ('Socket erfolgreich erstellt')
    except socket.error as err:
        print ('Socket nicht erstellt, Error: ', err)
    return s


s=create_socket()

#connect to server and join the group
def connect_to_server(server_name, port_number,user_name,s):
    try:
        s.connect((server_name, int(port_number)))
        try:
            print('\nIP-Adresse des Kommunikationspartners '+server_name+': ' + socket.gethostbyname(server_name) + ':'+str(port_number)+'\n')
        except socket.gaierror:
            print('Hostname kann nicht ermittelt werden')
            sys.exit()
    except socket.error as msg:
        print ('Nicht verbunden')   
    join_test=request_to_server(message_type[3],user_name,s)
    join_split=join_test.split('\r\n')
    if join_split[1]=='group join ack':
        print('Erfolgreich der Gruppe '+group_name+' beigetreten. Chat beenden mit x. Tippe deine Nachricht:\r\n')
    else:
        print('Beitreten der Gruppe '+group_name+' nicht möglich: Überprüfe deine Anfrage')



connect_to_server(sys.argv[1], sys.argv[2],sys.argv[3],s)

thread1=threading.Thread(target=get_response)
thread1.daemon=True
thread1.start()


#notify send message
def send_message(para_message_type, para_group_name,line_count,message_in,sck):
    request=head+para_message_type+para_group_name+str(line_count)+'\r\n'+body+message_in
    try:
        sck.send(bytes(request.encode('utf-8')))
    except socket.error:
        print('Senden nicht möglich')
        sys.exit()
    
#send message and exit
while True:
    message1=input()
    message=message1+'\r\n'
    if message1=='x':
        leave_test=request_to_server(message_type[2],group_name,s)
        leave_split=leave_test.split('\r\n')
        if leave_split[1]=='group leave ack':
            print('Gruppe '+group_name+' erfolgreich verlassen\r\n')
        else:
            print('Verlassen der Gruppe '+group_name+' nicht möglich: Überprüfe deine Anfrage')
        s.close()
        sys.exit()
    else:
        n_lines=message.count('\r\n')
        send_message(message_type[1],group_name,n_lines,message,s)


