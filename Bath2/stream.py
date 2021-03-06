'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Takes the input frame from the camera
Output: Streams the frame using Raspberrypi on the screen
Requirements:
This function shall perform the following:
1) The socket makes the connection between NX device and Raspberrypi
2)Streams the frames on the web application
'''
import cv2
import error
import socket
import struct
import time
import pickle
'''
client_socket = This variable shall create a socket pair and connect IP address and port.
encode_param = This variable shall be used to change the quality of the frame

'''
class VideoStream:
    """
    doc string
    """

    def __init__(self, host, port):
        """
        Intialize the socket.
        :param host:
        :param port: 
        """
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    
    def create_socket(self):
        """
        function to create socket
        """
        self.client_socket.close()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)  # set timeout

    def connect(self):
        """
        function to connect remote address
        """
        try:
            self.client_socket.connect((self.host, self.port))
            self.client_socket.settimeout(None)
            conn = self.client_socket.makefile('wb')
        except Exception as err:
            # print("Error - connecting: {}".format(err.__str__()))
            error.raised(4,"Error in socket creation")
            self.create_socket()
    
    def screening(self, frame):
        """
        function to send frame
        :param frame:
        """
        try:
            result, frame = cv2.imencode('.jpg', frame, self.encode_param)
            data = pickle.dumps(frame, 0)
            size = len(data)  # size of the frame
            #print(size,data)
            self.client_socket.sendall(struct.pack(">L", size) + data)
            # img_counter += 1
            time.sleep(0.1)
        except Exception as err:
            print("all ok")
            error.raised(2,"Error in Screening")
            print("Error - sending frame: {}".format(err.__str__()))
            self.connect()
