import socket
import struct
import log_message_pb2

import config


def send_message(sock, log_message):
    # Serialize the protobuf message
    payload = log_message.SerializeToString()

    # Send the length-prefixed message to the server
    message_length = len(payload)
    sock.sendall(struct.pack('>L', message_length) + payload)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((config.SERVER_ADDRESS, config.SERVER_PORT))

        lm = log_message_pb2.LogMessage()
        lm.log_level = 'ERROR'
        lm.logger = 'main'
        lm.mac = bytes([0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff])
        i = 0
        while i < 4:
            message = input("enter message:")
            lm.message = message
            send_message(sock, lm)
            i += 1


if __name__ == "__main__":
    main()
