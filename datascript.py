import requests
from bs4 import BeautifulSoup
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

page_url = 'http://www.physionet.org/physiobank/database/mitdb/'
page_store = 'E:\\paper_project\\MITData\\pagecontent.html'
file_directory = 'E:\\paper_project\\MITData\\'
############################download file################ ######################
  

def download_file(url, file_name, datafile):  # local variable(var) +,don't contain'.'
    datafile_name = file_name + '\\' + datafile
    data = requests.get(url)
    try:
        with open(datafile_name, 'w') as file:
            file.write(data.text)
            file.close()
    except IOError, e:
        print 'file open error!'
    return

##############################get page##########################################
# if __name__ == '__main__':
page = requests.get(page_url)
try:
    with open(page_store, 'w') as file1:
        file1.write(page.text)
        file1.close()
except IOError, e:
    print 'file open error!'
##############################get data links##############################
page_content = BeautifulSoup(page.text, 'html.parser')
for link in page_content.find_all('a'):
    if link.text.endswith('.dat')or link.text.endswith('.hea')or link.text.endswith('atr'):
        data_link = page_url + link.text
        file_name = file_directory + link.text[:3]
        # print file_name
        if os.path.exists(file_name):
            # print os.path.exists(file_name)
            print 'downloading' + '==>' + data_link + '==>' + link.text
            download_file(data_link, file_name, link.text)
        else:
            os.mkdir(file_name)
            print 'downloading' + '==>' + data_link + '==>' + link.text
            download_file(data_link, file_name, link.text)
print 'All files finished!'
