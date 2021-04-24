import shad_class as shad
import os, sys

AUTH = "YOUR DECRYPTED AUTH"
GUID = "CHAT GUID" # https://web.shad.ir/#c=CHAT GUID

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press any key to exit...")
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

os.system("title WELCOME")
while True:
    mode = input("Upload(1) or Download(2): ")
    if mode == "1":
        break
    elif mode == "2":
        break
    else:
        print("Enter Valid Number :/")

addr = input("drag and drop file: ").replace("\"", "")
sz_prt = int(input("size of a part (bytes): "))
file = shad.file(AUTH, addr)
if mode == "1":
    file.upload(GUID, sz_prt)
elif mode == "2":
    file.download(sz_prt)
input("Press any key to exit...")
