#https://www.youtube.com/watch?v=IEEhzQoKtQU&t=883s&ab_channel=CoreySchafer
import requests
import sys
from clint.textui import progress
import time
import  concurrent.futures

url=["https://www.python.org/static/community_logos/python-logo-master-v3-TM.png","https://file-examples.com/wp-content/storage/2017/10/file_example_TIFF_10MB.tiff","https://file-examples.com/wp-content/storage/2017/11/file_example_MP3_5MG.mp3","https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_1920_18MG.mp4"]
start = time.time()


def file_download(url):
    file = f'download_{time.time() + 1}.file'
    print(url)
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
# t1=threading.Thread(target=file_download,args=(url1))
# t2=threading.Thread(target=file_download,args=(url2))
# t3=threading.Thread(target=file_download,args=(url3))
# t4=threading.Thread(target=file_download,args=(url4))
threads=[]

with concurrent.futures.ThreadPoolExecutor() as Executor:
    # for index,i in enumerate([url1,url2,url3,url4]):
        f1= Executor.map(file_download,url)
        # threads.append(f1)
        # f1


# for thread in concurrent.futures.as_completed(threads):
#     thread.result()


# threads=[]

# for index,i in enumerate( [url1,url2,url3,url4]):
#     # i
#     print(index)
#     t=threading.Thread(target=file_download,args=(i,index))
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join()

# t1.start()
# t2.start()
# t3.start()
# t4.start()

# t1.join()
# t2.join()
# t3.join()
# t4.join()


end = time.time()
print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")