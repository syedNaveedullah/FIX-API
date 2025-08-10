# import ssl

# # SSL Configuration
# ssl_context = ssl.create_default_context()
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE  # Adjust if using real SSL certs

# # FIX API Credentials (Replace with actual credentials)
# FIX_CONFIG = {
#     "host": "pxmdemouk.primexm.com",
#     "port": 32477,  # Use 32478 for trading
#     "sender": "Q004",
#     "target": "XCD191",
#     "username": "your_username",
#     "password": "your_password",
#     "ssl": ssl_context
# }
import json
import ssl

# Load config.json
with open("config.json", "r") as file:
    CONFIG = json.load(file)

# SSL Configuration
def get_ssl_context(use_ssl: bool):
    """Set up SSL context based on config."""
    if use_ssl:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE  # Adjust if using real SSL certs
        return context
    return None  # No SSL

# Extract Pricing and Trading configurations
PRICING_CONFIG = CONFIG["Pricing"]
TRADING_CONFIG = CONFIG["Trading"]

# Get SSL context for Trading (since Pricing does not use SSL)
TRADING_CONFIG["ssl"] = get_ssl_context(TRADING_CONFIG["SocketUseSSL"] == "Y")
