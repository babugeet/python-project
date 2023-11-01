import requests
import sys
from clint.textui import progress
import time

url1="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
url2="https://file-examples.com/wp-content/storage/2017/10/file_example_TIFF_10MB.tiff"
url3="https://file-examples.com/wp-content/storage/2017/11/file_example_MP3_5MG.mp3"
url4="https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_1920_18MG.mp4"
start = time.time()
def file_download(url,file):
    
    # path=
    with open(file, 'wb') as f:
        response=requests.get(url,stream=True)
        total_length = int(response.headers.get('content-length'))
        for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

        # total_length = response.headers.get('content-length')
        # f.write(response.content)
        # if total_length is None: # no content length header
        #     f.write(response.content)
        # else:
        #     dl = 0
        #     total_length = int(total_length)
        #     for data in response.iter_content(chunk_size=4096):
        #         dl += len(data)
        #         f.write(data)
        #         done = int(50 * dl / total_length)
        #         sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
        #         sys.stdout.flush()
# time=time
file_download(url1,"python-logo-master-v3-TM.png")
file_download(url2,"file_example_TIFF_10MB.tiff")
file_download(url3,"file_example_MP3_5MG.mp3")
file_download(url4,"file_example_MP4_1920_18MG.mp4")
end = time.time()
print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")