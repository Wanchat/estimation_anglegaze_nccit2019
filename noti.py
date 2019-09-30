import notify2
import time

def noti(title, message):

    path_icon = "/home/wanchat/.icons/Arrongin-icon-theme/status/symbolic/dialog-warning-symbolic.svg"
    notify2.init('app name')
    n = notify2.Notification(title, message, path_icon)
    n.show()
    time.sleep(3)
    n.close()

if __name__ == "__main__":
    noti("hi", "hello")