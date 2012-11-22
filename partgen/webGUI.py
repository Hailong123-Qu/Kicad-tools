#!/usr/bin/python
############################################################################
############################################################################
"""
##  webGUI - Example of Web Browser Based GUI for PartGen
## 
##  Designed by
##         A.D.H.A.R Labs Research,Bharat(India)
##            Abhijit Bose( info@adharlabs.in )
##                http://ahdarlabs.in
##
## License:
## Apache License, Version 2.0
"""
##
## Version History:
## version 0.0 - Initial Release (2012-11-22)
##
############################################################################
############################################################################
#IMPORTS>
############################################################################
import BaseHTTPServer
import urlparse
############################################################################
#EXPORT>
############################################################################
__author__      = "Abhijit Bose(info@adharlabs.in)"
__author_email__= "info@adharlabs.in"
__version__     = "0.0"
__copyright__   = "Copyright (c) 2012, ADHAR Labs Research"
__license__     = "Apache License, Version 2.0"
############################################################################
#DEFINES>
############################################################################
HOST_NAME   = ''
PORT_NUMBER = 9090
PAGE_TEMPLATE = ''
############################################################################
#CLASSES>Lib
############################################################################
## Handler Class for the Web Interface
class WebGUIHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  #{
    def do_HEAD(s):
      #{
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")
        s.end_headers()
      #}

    def do_GET(s):
      #{
        """Respond to a GET request."""      
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")
        s.end_headers()
        
        url = urlparse.urlsplit(s.path)
        if url.path != '/':
          #{
            return
          #}            
        query = url.query
        args = urlparse.parse_qsl(query)
        
        say_what = ''
        for arg in args:
          #{
            if arg[0] == 'say_what':
              #{
                say_what = arg[1].strip().replace('\r', '')
                notice = '%s says:\n\n%s' % (s.client_address[0], say_what)
                print(notice)
                break
              #}
          #}

        html = PAGE_TEMPLATE % say_what
        s.wfile.write(html)
      #}
    #}
############################################################################
# Main FUNCTION>
############################################################################
if __name__ == "__main__" :
  #{
    #Load Page Template
    f = open("page.html","r")
    PAGE_TEMPLATE = f.readlines()
    f.close()
    PAGE_TEMPLATE = "".join(PAGE_TEMPLATE)

    #Tell The socket Name
    print('web server running on port %s' % PORT_NUMBER)
    print("Type address http://localhost:%s in your Internet Browser" %
          PORT_NUMBER)
    
    #Run the Server
    server = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), WebGUIHandler)
    server.serve_forever()
  #}
############################################################################
