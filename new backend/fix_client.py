import socket
import logging
from config import FIX_CONFIG

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FixClient:
    def __init__(self):
        self.host = FIX_CONFIG["host"]
        self.port = FIX_CONFIG["port"]
        self.sender = FIX_CONFIG["sender"]
        self.target = FIX_CONFIG["target"]
        self.username = FIX_CONFIG["username"]
        self.password = FIX_CONFIG["password"]
        self.ssl_context = FIX_CONFIG["ssl"]
        self.sock = None

    def connect(self):
        """Establish connection to FIX server."""
        try:
            self.sock = socket.create_connection((self.host, self.port))
            self.sock = self.ssl_context.wrap_socket(self.sock, server_hostname=self.host)
            logger.info("Connected to FIX server.")

            # Send Logon message
            logon_message = self.create_logon_message()
            self.send_fix_message(logon_message)
        except Exception as e:
            logger.error(f"FIX connection error: {e}")

    def disconnect(self):
        """Close FIX connection."""
        if self.sock:
            self.sock.close()
            logger.info("Disconnected from FIX server.")

    def send_fix_message(self, message: str):
        """Send a FIX message."""
        try:
            if self.sock:
                self.sock.sendall(message.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error sending message: {e}")

    def receive_fix_message(self):
        """Receive a FIX message."""
        try:
            if self.sock:
                return self.sock.recv(4096).decode('utf-8')
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            return None

    def create_logon_message(self):
        """Create a FIX logon message."""
        return f"8=FIX.4.4|9=112|35=A|49={self.sender}|56={self.target}|34=1|52=20240308-12:34:56|98=0|108=30|141=Y|553={self.username}|554={self.password}|10=128|"

    def send_market_data_request(self, symbol: str):
        """Request market data for a symbol."""
        md_request = f"8=FIX.4.4|9=92|35=V|49={self.sender}|56={self.target}|34=2|52=20240308-12:34:56|262=1|263=1|264=1|146=1|55={symbol}|10=128|"
        self.send_fix_message(md_request)
        return self.receive_fix_message()

    def send_new_order(self, symbol: str, side: str, quantity: int, price: float, order_type: str):
        """Place a new order."""
        side_map = {"buy": "1", "sell": "2"}
        order_type_map = {"market": "1", "limit": "2"}
        new_order = f"8=FIX.4.4|9=120|35=D|49={self.sender}|56={self.target}|34=3|52=20240308-12:34:56|11=1234|55={symbol}|54={side_map[side]}|38={quantity}|40={order_type_map[order_type]}|44={price}|10=128|"
        self.send_fix_message(new_order)
        return self.receive_fix_message()

    def is_connected(self):
        """Check if FIX session is connected."""
        return self.sock is not None

# Create a single instance for use
fix_client = FixClient()


# import socket
# import logging
# from config import PRICING_CONFIG, TRADING_CONFIG

# # Logger setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class FixClient:
#     def __init__(self, config):
#         """Initialize FIX client with the given configuration (Pricing or Trading)."""
#         self.host = config["SocketConnectHost"]
#         self.port = config["SocketConnectPort"]
#         self.sender = config["SenderCompID"]
#         self.target = config["TargetCompID"]
#         self.username = config["LoginUsername"]
#         self.password = config["LoginPassword"]
#         self.ssl_context = config.get("ssl")
#         self.sock = None

#     def connect(self):
#         """Establish connection to FIX server."""
#         try:
#             self.sock = socket.create_connection((self.host, self.port))
#             if self.ssl_context:
#                 self.sock = self.ssl_context.wrap_socket(self.sock, server_hostname=self.host)
#             logger.info(f"Connected to FIX server at {self.host}:{self.port}")

#             # Send Logon message
#             logon_message = self.create_logon_message()
#             self.send_fix_message(logon_message)
#         except Exception as e:
#             logger.error(f"FIX connection error: {e}")

#     def disconnect(self):
#         """Close FIX connection."""
#         if self.sock:
#             self.sock.close()
#             logger.info("Disconnected from FIX server.")

#     def send_fix_message(self, message: str):
#         """Send a FIX message."""
#         try:
#             if self.sock:
#                 self.sock.sendall(message.encode('utf-8'))
#         except Exception as e:
#             logger.error(f"Error sending message: {e}")

#     def receive_fix_message(self):
#         """Receive a FIX message."""
#         try:
#             if self.sock:
#                 return self.sock.recv(4096).decode('utf-8')
#         except Exception as e:
#             logger.error(f"Error receiving message: {e}")
#             return None

#     def create_logon_message(self):
#         """Create a FIX logon message."""
#         return f"8=FIX.4.4|9=112|35=A|49={self.sender}|56={self.target}|34=1|52=20240308-12:34:56|98=0|108=30|141=Y|553={self.username}|554={self.password}|10=128|"

#     def send_market_data_request(self, symbol: str):
#         """Request market data for a symbol."""
#         md_request = f"8=FIX.4.4|9=92|35=V|49={self.sender}|56={self.target}|34=2|52=20240308-12:34:56|262=1|263=1|264=1|146=1|55={symbol}|10=128|"
#         self.send_fix_message(md_request)
#         return self.receive_fix_message()

#     def send_new_order(self, symbol: str, side: str, quantity: int, price: float, order_type: str):
#         """Place a new order."""
#         side_map = {"buy": "1", "sell": "2"}
#         order_type_map = {"market": "1", "limit": "2"}
#         new_order = f"8=FIX.4.4|9=120|35=D|49={self.sender}|56={self.target}|34=3|52=20240308-12:34:56|11=1234|55={symbol}|54={side_map[side]}|38={quantity}|40={order_type_map[order_type]}|44={price}|10=128|"
#         self.send_fix_message(new_order)
#         return self.receive_fix_message()

#     def is_connected(self):
#         """Check if FIX session is connected."""
#         return self.sock is not None

# # Create Pricing and Trading FIX clients
# pricing_client = FixClient(PRICING_CONFIG)
# trading_client = FixClient(TRADING_CONFIG)
