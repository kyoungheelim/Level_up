import sys, os
import win32serviceutil, win32service, win32event, win32api
import servicemanager
import logging, configparser, traceback

class Service(win32serviceutil.ServiceFramework):
    _svc_name_= 'SVC'
    _svc_display_name_= 'Service'

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.haltEvent = win32event.CreateEvent(None,0,0,None)
        self.is_running = False
        self.cur_path = os.path.dirname(os.path.abspath(__file__))

        config = configparser.ConfigParser()
        config.read(self.cur_path + '/opp.ini')

        str_log_level = config['GENERAL']['LOGLEVEL']
        self._timeout = int(config['GENERAL']['CHECK_TERM'])
        log_level = 0

        if str_log_level == 'DEBUG':
            log_level = logging.DEBUG
        elif str_log_level == 'ERROR':
            log_level = logging.ERROR
        elif str_log_level == 'WARN':
            log_level = logging.WARN
        else:
            log_level = logging.INFO


    def SvcStop(self):
        self.ReportServiceStatus((win32service.SERVICE_STOP_PENDING))
        self.is_running = False
        win32event.SetEvent(self.haltEvent)

    def SvcDoRun(self):
        self.is_running = True
        logging.info("[SERVICE] let's start")

        while self.is_running:
            rc = win32event.WaitForMultipleObjects(self.haltEvent, self._timeout)

            if rc == win32event.WAIT_OBJECT_0:
                logging.info("[SERVICE] Stop Signal")
                break
            else:
                try:
                    logging.info("[SERVICE] RUN function.")
                    #수행 method 실행
                except:
                    logging.warning("[SERVICE] %s" % traceback.format_exc())
                logging.warning("[SERVICE] RETURN of function is : %s")



def ctrlHandelr(strlType):
        return True
if  __name__=='__main__':

    if getattr(sys, 'frozen', False):
        if len(sys.argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(Service)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32api.SetConsoleCtrlHandler(ctrlHandelr(),True)
            win32serviceutil.HandleCommandLine(Service)

    else:
        win32api.SetConsoleCtrlHandler(ctrlHandelr,True)
        win32serviceutil.HandleCommandLine(Service)







