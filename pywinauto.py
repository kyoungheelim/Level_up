import win32com.client as win32
import time

outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
messages = inbox.Items
message = messages.GetFirst()
while message:
    if message.Unread == True:
     print (message.body)
     message = messages.GetNext()

