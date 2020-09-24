import win32com.client
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# os.startfile("outlook")
options = Options()
options.headless = True

outlook=win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox=outlook.GetDefaultFolder(6)


inbox.Display
messages=inbox.Items
messages.Sort("[ReceivedTime]", True)

for message in messages:

    if message.Unread==True:
        print(message.body)
        for att in message.Attachments:
            message.Display(True)
            att.SaveAsFile('C:\\Users\\user\\Desktop\\level_up' + '\\' + str(att))
            driver=webdriver.Chrome('C:\\Users\\user\\Desktop\\untitle\\chromedriver.exe')
            driver.get('http://49.50.164.42:5000/upload')

            time.sleep(2)

            #파일 업로드 영역
            driver.find_element_by_css_selector("input[type='file']").send_keys('C:\\Users\\user\\Desktop\\level_up' + '\\' + str(att))
            time.sleep(2)
            #제출 클릭
            driver.find_element_by_css_selector("input[type='submit']").click()
            time.sleep(2)
            #업로드 성공 확인 버튼 클릭
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(2)
            #결과 클릭
            driver.find_element_by_css_selector("input[type='button']").click()

