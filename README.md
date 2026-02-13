🐾 My First IoT Project: Web-Controlled Pet Feeder

This is my first Internet of Things (IoT) project! 🎉 I built an automatic pet feeder using a Raspberry Pi Pico W that detects my pet, waits a set time, dispenses food using a servo, and even responds to commands from a website.

It’s been a journey full of challenges and learning, and I’m excited to share what I’ve done so far.

⚡ Features

    • Automatic Feeding: Detects your pet with an ultrasonic sensor and waits the required time before dispensing food.

    • Servo Precision: Fine-tuned servo range and timing for smooth and accurate gate movement.

    • Web Control: Control the feeder remotely using a simple website via WiFi sockets.

    • LCD Display: Shows real-time system status, including WiFi, feeding status, and errors.

    • Threshold Control: Adjust the detection distance using a potentiometer.

    • Reliable Network Handling: Non-blocking sockets ensure the device continues working even when handling web requests.

🛠 Hardware Needed

    • Raspberry Pi Pico W

    • Ultrasonic Sensor (HC-SR04 or similar)

    • Servo Motor

    • 16x2 I2C LCD Display

    • Potentiometer (1K)

    • LED (optional, as a status indicator)

    • Power Source: 5V recommended for the LCD

📁 Project Structure

      project/
      ├─ main.py            # Main program: sensor reading, servo & web control
      ├─ us_functions.py    # Ultrasonic sensor, potentiometer, timer logic
      ├─ servo_functions.py # Servo motor control & food dispensing
      ├─ pico_server.py     # WiFi connection & HTTP server for web control
      └─ README.md          # Project documentation
      
🚀 How to Use

Wire your components according to the pins:

    • Servo: GPIO 14

    • Ultrasonic: Trigger GPIO 17, Echo GPIO 16

    • Potentiometer: ADC GPIO 26

    • LCD: I2C SDA GPIO 0, SCL GPIO 1

    • LED: GPIO 15

    • Make sure to ground everything!

    • Install MicroPython on the Pico W.

    • Copy all project files to the Pico W.

    • Power the Pico W and wait for it to initialize. The LCD will show:

          "Connecting to WiFi..."

          "Can drop food." once ready

    • Errors if WiFi or socket fails

Control via web browser:

    http://<PICO_IP>/servo

This will trigger the feeder to dispense food.

💡 How It Works

    • Sensor Loop: Continuously reads the ultrasonic sensor and calculates a stable distance using averaging logic.

    • Servo Control: Dispenses food after the pet is detected for the configured time.

    • Web Interface: The Pico listens for HTTP requests via a WiFi socket. When it receives a /servo request, it dispenses food.

    • LCD Display: Provides live updates, including feeding status, WiFi connection, and errors.

    • Error Handling: Uses non-blocking sockets and proper initialization to prevent freezing or crashes.

🔧 Challenges & Lessons Learned

    • Initialization Issues: At first, the Pico only worked when connected to my laptop. I fixed this by adding a small time.sleep() at startup to let it initialize and connect to WiFi.

    • LCD Glitches: Sometimes showed weird characters. Solved by clearing/re-initializing the display on startup.

    • Erratic Sensor Readings: Stabilized using averaging logic for more reliable detection.

    • Non-Blocking Sockets: Learned how to handle web requests without freezing the main sensor loop.

🌐 What I Learned About IoT

    • I really got to experience the magic of IoT: connecting a physical device to the internet. I learned:

    • Sockets: A socket is like a “door” that lets apps communicate with your device. My website sends a request through the socket, the Pico opens the door, reads the request, moves the servo, and sends back a response.

    • Device-to-Web Control: I can now control a real-world device from my browser!

    • MicroPython & Embedded Systems: Practical experience with PWM, ADC, I2C, and timers.

✅ Next Steps / Future Improvements

    • Mobile-friendly web interface

    • Adjustable feeding timer

    • Multiple feeding zones

    • Logging feed times and pet activity

🏷 Keywords & Tags

#IoT #RaspberryPiPico #MicroPython #EmbeddedSystems #ServoMotor #Sensors #WebControl #WiFi #I2C #MakerProject #DIYTech #FirstIoTProject #LearningByDoing #TechInnovation #Sockets #DIYElectronics
