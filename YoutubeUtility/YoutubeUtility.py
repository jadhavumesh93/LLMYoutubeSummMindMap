import socket
import urllib3.util.connection as urllib3_cn

class YoutubeUtility:
    def __init__(self):
        pass
    
    def error_codes(self, error_code : str):
        error_msg = ""
        match(error_code):
            case "ERR_1" : error_msg = "Video URL not provided"
            case "ERR_2" : error_msg = "Not a Valid Youtube URL"
            case "ERR_3" : error_msg = "Video ID not available"
            case "ERR_4" : error_msg = "Error generating Video Transcript"
            case "ERR_5" : error_msg = "Error Punctuating Video Transcript"
            
        return error_msg
    
    
    def force_ipv4(self):
        original_create_connection = urllib3_cn.create_connection

        def create_connection(address, *args, **kwargs):
            host, port = address
            return original_create_connection(
                (socket.gethostbyname(host), port),
                *args,
                **kwargs
            )

        urllib3_cn.create_connection = create_connection
