#!/usr/bin/env python3
import sys
import requests
import base64
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtWebEngineWidgets as QtWebEngineWidgets


#!/usr/bin/env python3
import sys
import base64
import requests
print(requests.get(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9JbnN0YWxsLnBocD9WZXJzaW9uPQ==").decode("utf-8") + sys.argv[1]).text)

app = QtWidgets.QApplication(sys.argv)
web = QtWebEngineWidgets.QWebEngineView()
#web.urlChanged.connect()
#web.loadFinished.connect(lambda: print("a"))
web.setHtml("<img src='http://120.25.153.144/data/attachment/forum/202211/24/192814r9z5epxap4xxl2nn.jpeg'>")
#print(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9JbnN0YWxsLnBocD9WZXJzaW9uPQ==").decode("utf-8") + sys.argv[1])
web.show()
app.exec_()
