from plyer import notification
import Config

def throw(Title, Message, Timeout=3):

    notification.notify(
        title=Title,
        message=Message,
        app_icon=Config.SmallIcon,
        timeout=Timeout,
    )
