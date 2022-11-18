import socket
from threading import Thread


class WebServer:

    def __init__(self, address='localhost', port=5678):
        self.port = port
        self.address = address

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.address, self.port))
            s.listen(10)

            while True:
                print('Waiting connections...')
                conn, addr = s.accept()
                req = HttpRequest(conn, addr)
                req.start()


class HttpRequest(Thread):

    def __init__(self, conn, addr):
        super(HttpRequest, self).__init__()
        self.conn = conn
        self.addr = addr
        self.CRLF = '\r\n'
        self.buffer_size = 4096

    def run(self):
        request = self.conn.recv(self.buffer_size)
        print(request)

        rstring = request.decode('utf-8')
        if(rstring.find('.html', 0, rstring.find('HTTP')) != -1):
            response = HttpResponse(self.conn, self.addr, open('stuff/' + rstring[(rstring.find('/')+1):(rstring.find('HTTP')-1)], 'rb'), '', 'html')
        elif(rstring.find('.png', 0, rstring.find('HTTP')) != -1):
            response = HttpResponse(self.conn, self.addr, open('stuff/' + rstring[(rstring.find('/')+1):(rstring.find('HTTP')-1)], 'rb'), 'png', '')
        elif(rstring.find('.jpeg', 0, rstring.find('HTTP')) != -1):
            response = HttpResponse(self.conn, self.addr, open('stuff/' + rstring[(rstring.find('/')+1):(rstring.find('HTTP')-1)], 'rb'), 'jpeg', '')    
        elif(rstring.find('.ico', 0, rstring.find('HTTP')) != -1):
            response = HttpResponse(self.conn, self.addr, open('stuff/' + rstring[(rstring.find('/')+1):(rstring.find('HTTP')-1)], 'rb'), 'ico', '')
        elif(rstring.find('.js', 0, rstring.find('HTTP')) != -1):
            response = HttpResponse(self.conn, self.addr, open('stuff/' + rstring[(rstring.find('/')+1):(rstring.find('HTTP')-1)], 'rb'), '', 'js')
        else:
            response = HttpResponse(self.conn, self.addr, open('stuff/index.html', 'rb'), '', 'html')
        
        response.processRespose()

        self.conn.close()


class HttpResponse:

    def __init__(self, conn, addr, file, image, text):
        self.conn = conn
        self.addr = addr
        self.file = file
        self.image = image
        self.text = text

    def processRespose(self):
        file_string = self.file.read()
        if(self.image != ''):
            self.conn.sendall(
            ('HTTP/1.0 200 OK\r\nContent-Type: image/' + self.image + '\r\n\r\n').encode(
                'utf-8'))
            self.conn.sendall(file_string)
            
        else:
            file_string = file_string.decode('utf-8')
            self.conn.sendall(
                ('HTTP/1.0 200 OK\r\nContent-Type: text/' + self.text + '\r\n\r\n' + file_string + '').encode(
                    'utf-8'))
