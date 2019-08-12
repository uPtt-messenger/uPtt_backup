from plyer import notification

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def throw(Title, Message, Timeout=3):
    print(dir_path)

    notification.notify(
        title=Title,
        message=Message,
        app_icon='./src/res/Small.ico',  # e.g. 'C:\\icon_32x32.ico'
        timeout=Timeout,  # seconds
    )
