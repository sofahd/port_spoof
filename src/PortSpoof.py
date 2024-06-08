import socket, argparse
from sofahutils import SofahLogger

class PortSpoof:
    """
    This class is designed to spoof banners to clients trying to connect to a port.
    
    It should be able to work both in "banner" and in "http-header" mode.
    """

    def __init__(self, mode:str, banner_header:str, ip:str, port:int, logger:SofahLogger) -> None:
        """
        This method is the constructor for the PortSpoof class.
        It is mainly used to set the mode to "banner" or "http-header", according with the appropriate parameter.

        Regarding the `banner_header`-parameter:
        here it is expected that the user passes a string only containing the banner or http-header value that is seen by nmap. (so no `\r\n` at the end or `HTTP/1.1 200 OK` at the beginning)

        :param mode: The mode to use. Should be EITHER "banner" or "http-header".
        :type mode: str
        :param banner_header: The banner or header to send to the client.
        :type banner_header: str
        :param ip: The IP address to listen on.
        :type ip: str
        :param port: The port to listen on.
        :type port: int
        :param logger: the logger to use.
        :type logger: SofahLogger
        :return: None
        """

        if mode in ["banner", "http-header", "checkpoint"]:
            self.mode = mode
        else:
            raise ValueError(f"Invalid mode: {mode}")
        
        self.banner_header = banner_header
        self.logger = logger
        self.ip = ip
        self.port = port


    def spoof(self) -> None:
        """
        Use this method to spoof an HTTP header or a banner to a client trying to connect to a port.

        :return: None
        """

        socket_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_listener.bind((self.ip, self.port))
        socket_listener.listen(5)
        self.logger.info(f"Listening on {self.ip}:{self.port}")

        while True:
            try:
                client, adress = socket_listener.accept()
                data = client.recv(1024)

                if self.mode == "banner":
                    client.send(bytes(f"{self.banner_header}\r\n\r\n", 'utf-8'))
                
                elif self.mode == "http-header":
                    if data and self.is_valid_http_request(data.decode('utf-8')):
                        client.send(bytes(f"HTTP/1.1 200 OK\r\nServer: {self.banner_header}\r\n\r\n", 'utf-8'))
                        
                elif self.mode == "checkpoint":
                    if data and data.decode('utf-8') == "\r\n\r\n":
                        client.sendall(b"Y\x00\x00\x00")
                        
                client.close()
            
            except Exception as e:
                continue
    
    def is_valid_http_request(self, request_line:str) -> bool:
        """
        This method is used to check if a given string is a valid HTTP request.

        :param request_line: The string to check.
        :type request_line: str
        :return: True if the string is a valid HTTP request, False otherwise.
        :rtype: bool
        """

        parts = request_line.split(' ')
        if len(parts) != 3:
            return False

        method, _, version = parts
        valid_methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
        if method not in valid_methods:
            return False

        if not version.startswith("HTTP/"):
            return False

        return True
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some integers.")

    # Add arguments
    parser.add_argument('-p', '--port', type=int, required=True, help='The port to listen on')
    parser.add_argument('-m', '--mode', type=str, required=True, choices=['banner', 'http-header', 'checkpoint'], help='The mode you want to run the script in')
    parser.add_argument('-b', '--banner', type=str, required=True, help='The banner or http-header to send to the client')
    parser.add_argument('-i', '--info_port', type=str, required=True, help='The actual outside port of the service for logging purposes')
    parser.add_argument('-l', '--log', type=str, required=True, help='The log server to send logs to with http and porr (e.g. http://log_api:5000)')
    args = parser.parse_args()
    logger = SofahLogger(args.log, args.info_port)
    ps = PortSpoof(ip="0.0.0.0", port=args.port, banner_header=args.banner, mode=args.mode, logger=logger)
    ps.spoof()
