from urllib.request import urlopen

while True:
    url = input("FULL URL OF TARGETED WEBSITE: ")
    url.rstrip()
    header = urlopen(url).info()
    print(str(header))