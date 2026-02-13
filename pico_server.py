import network
import time
import socket
import servo_functions as sf

wifi_name = "EagleNet"
wifi_password = None # None --> Open Network
ip = "0.0.0.0"
connection = None

# Making connection to the WiFi
def connect_wifi(lcd):
    global ip
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    time.sleep(1)
    lcd.clear()
    lcd.putstr("Connecting WiFi")

    # Trying to connect to the WiFi in 15 times
    i = 0
    max_attempts = 15  # try for 15 seconds
    while not wlan.isconnected() and i < max_attempts:
        lcd.clear()
        wlan.connect(wifi_name, wifi_password)
        lcd.putstr("Connecting WiFi")
        lcd.move_to(0, 1)
        lcd.putstr(f"Attempt {i+1}/{max_attempts}")
        print(f"Connecting WiFi... Attempt {i+1}")
        time.sleep(1)
        i += 1

    if wlan.isconnected():
        # WiFi connection succeed
        ip = wlan.ifconfig()[0]
        lcd.clear()
        lcd.putstr("WiFi Connected")
        print("Connected to WiFi:", wlan.ifconfig())
        return True
    else:
        # WiFi connection faild
        lcd.clear()
        lcd.putstr("WiFi Failed")
        print("Could not connect to WiFi.")
        return False
        
# This function returns the IP
def get_ip():
    global ip
    return ip
    
# This function opens the sockets and returns the connection
def open_socket():
    global ip, connection
    try:
        address = (ip, 80)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.bind(address)
        connection.listen(5)
        connection.settimeout(0.3) # Allowing the browser to send the request
        print('Listening on', address)
        return connection
    except OSError as e:
        if e.errno == 98: # EADDRINUSE, port is in use
            print("Address already in use. Ensure previous processes are stopped or wait a moment.")
        else:
            raise e
        return None

# This function closes the socket and the connection
def close_socket_gracefully():
    global connection
    print("[!] Closing socket...")

    if connection is None:
        print("[!] No socket to close.")
        return

    try:
        connection.close()
    except OSError:
        pass

    connection = None
    print("[!] Socket closed.")

# This function handles the requests
def handle_requests(path, seconds):
    if path == "servo":
        print("Servo!")
        sf.dispense_food(seconds)
        return 200
    
    return 404

# This is the loop function that accept the requests and returns the outputs
def loop(seconds):
    global connection

    if connection is None:
        return

    try:
        client, addr = connection.accept()
    except OSError as e:
        # ETIMEDOUT = 110 → no client tried to connect in timeout period
        if e.args[0] == 110:
            return
        else:
            raise

    print("Got connection from", addr)

    # Accepts the request
    try:
        request = client.recv(1024)
    except OSError as e:
        # No data found
        print("No data", e)
        client.close()
        return
    
    if not request:
        # Closing the client connection
        client.close()
        return
    
    request_str = request.decode()
    # Get the first line
    first_line = request_str.split("\r\n")[0]
    raw_path = first_line.split(" ")[1]   # "/servo?x=2"

    # Remove leading slash
    raw_path = raw_path.lstrip("/")

    # Remove query parameters
    path = raw_path.split("?")[0]

    print("Requested path:", path)
    
    # Getting response code
    response_code = handle_requests(path, seconds)
    
    # Client response
    status_text = "OK" if response_code == 200 else "Not Found"
    client.send(f'HTTP/1.0 {response_code} {status_text}\r\nContent-type: text/html\r\n\r\n')
    client.close()
