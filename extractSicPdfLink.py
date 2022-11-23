import urllib.request
import PyPDF2
import io

URL = 'https://www.sic.gov.co/sites/default/files/estados/112022/ESTADO%20215.pdf'
req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
remote_file = urllib.request.urlopen(req).read()
remote_file_bytes = io.BytesIO(remote_file)
pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes)

for i in range(pdfdoc_remote.numPages):
    current_page = pdfdoc_remote.getPage(i)
    print("===================")
    print("Content on page:" + str(i + 1))
    print("===================")
    print(current_page.extractText())