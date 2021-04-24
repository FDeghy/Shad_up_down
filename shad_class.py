# +------------------------------+
# |         Shad class           |
# |         version: 2           |
# |        made: DeghyOS         |
# +------------------------------+
import json, requests, base64, random, os, pathlib, math, sys, urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class encryption:
    def __init__(self, auth):
        self.key = bytearray(self.secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        raw = pad(text.encode('UTF-8'), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = aes.encrypt(raw)
        result = base64.b64encode(enc).decode('UTF-8')
        return result

    def decrypt(self, text):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8')))
        result = unpad(dec, AES.block_size).decode('UTF-8')
        return result

class file:
    def __init__(self, auth, addr):
        self.auth = auth
        self.header = {
            'Host': 'shadmessenger60.iranlms.ir',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Content-Type': 'application/json',
            'Origin': 'https://web.shad.ir',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://web.shad.ir/',
            'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
        }
        self.url = 'https://shadmessenger60.iranlms.ir'

        # upload
        self.addr = addr
        self.file_name = os.path.basename(addr)
        self.file_type = pathlib.PurePath(addr).suffix.replace('.', '')
        self.file_size = pathlib.Path(addr).stat().st_size

    def upload(self, guid, sz_prt: int):
        aes = encryption(self.auth)
        if self.file_size > 996147200:
            size = 996147200
        else:
            size = self.file_size

        data1_req_send_file = {
            "method": "requestSendFile",
            "input": {
                'file_name': self.file_name,
                'size': str(size),
                'mime': self.file_type
            },
            "client": {
                "app_name": "Main",
                "app_version": "3.1.15",
                "platform": "Web",
                "package": "web.shad.ir",
                "lang_code": "fa"
            }
        }
        data2_req_send_file = {
            'api_version': '5',
            'auth': self.auth,
            'data_enc': aes.encrypt(json.dumps(data1_req_send_file))
        }

        os.system(f'title {self.file_name}')
        print(f"[+] Send requestSendFile to get access_hash_send for upload the file ({self.file_name})")
        req_send_file = requests.post(self.url, headers=self.header, data=json.dumps(data2_req_send_file), verify=False)
        rec_data1 = json.loads(aes.decrypt(json.loads(req_send_file.text)["data_enc"]))
        file_id = str(rec_data1['data']['id'])
        dc_id = str(rec_data1['data']['dc_id'])
        hash_send = str(rec_data1['data']['access_hash_send'])
        up_url = str(rec_data1['data']['upload_url'])

        print("[+] Now received response:\n")
        print(rec_data1)

        total_part = math.ceil(self.file_size / sz_prt)
        print(f"\n[+] Start upload (size of a part: {sz_prt} byte; number of parts: {total_part})\n")
        part = 1
        with open(self.addr, 'rb') as (myfile):
            byte = myfile.read(sz_prt)
            while (byte):
                head_up = {
                    'Connection': 'keep-alive',
                    'Accept': 'application/json, text/plain, */*',
                    'file_id': file_id,
                    'total_part': str(total_part),
                    'access_hash_send': hash_send,
                    'part_number': str(part),
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                    'auth': self.auth,
                    'Origin': 'https://web.shad.ir',
                    'Sec-Fetch-Site': 'cross-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://web.shad.ir/',
                    'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
                    'Accept-Encoding': 'gzip, deflate'
                }
                done = int(50 * part / total_part)
                req_up = requests.post(up_url, headers=head_up, data=byte, verify=False)
                sys.stdout.write(f"\r{part} | {round(part / total_part * 100, 1)}% [{'█' * done}{'░' * (50 - done)}]")
                sys.stdout.flush()
                if part == total_part:
                    break
                part += 1
        print("\n\n[+] Last part uploaded")
        print("[+] Received response:")
        print('\n' + req_up.text)

        data_send_json = json.loads(req_up.text)
        access_hash_rec = str(data_send_json['data']['access_hash_rec'])
        rnd = random.randint(100000, 900000)

        data_send = {
            "method": "sendMessage",
            "input": {
                "object_guid": guid,
                "rnd": str(rnd),
                "file_inline": {
                    "dc_id": str(dc_id),
                    "file_id": str(file_id),
                    "type": "File",
                    "file_name": str(self.file_name),
                    "size": str(size),
                    "mime": str(self.file_type),
                    "access_hash_rec": str(access_hash_rec)
                },
                "text": f"{self.file_name} | {round(self.file_size / 1048576, 1)}"
            },
            "client": {
                "app_name": "Main",
                "app_version": "3.1.15",
                "platform": "Web",
                "package": "web.shad.ir",
                "lang_code": "fa"
            }
        }
        data_send_enc = aes.encrypt(json.dumps(data_send))
        url_send = 'https://shadmessenger60.iranlms.ir'
        head_send = {
            'Host': 'shadmessenger60.iranlms.ir',
             'Connection': 'keep-alive',
             'Accept': 'application/json, text/plain, */*',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
             'Content-Type': 'text/plain',
             'Origin': 'https://web.shad.ir',
             'Sec-Fetch-Site': 'cross-site',
             'Sec-Fetch-Mode': 'cors',
             'Sec-Fetch-Dest': 'empty',
             'Referer': 'https://web.shad.ir/',
             'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
             'Accept-Encoding': 'gzip, deflate'
        }
        data_ersal = {
            'api_version': '5',
            'auth': self.auth,
            'data_enc': data_send_enc
        }
        req_ersal = requests.post(url_send, headers=head_send, data=(json.dumps(data_ersal)), verify=False)
        print("\n" + aes.decrypt(json.loads(req_ersal.text)["data_enc"]) + "\n")
        dqy = {
            'dc_ic': dc_id,
            'access_hash_rec': access_hash_rec,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'file_id': file_id
        }
        with open('sh_' + self.file_name + '.json', 'w', encoding='utf8') as dghy:
            dqy2 = json.dumps(dqy)
            dghy.write(dqy2)
            print(dqy2)
        print("[+] Upload Complete!")

    def download(self, sz_prt: int):
        with open(self.addr, 'r', encoding='utf8') as dghy:
            dqy = json.loads(dghy.read())
        file_name = dqy['file_name']
        file_size = dqy['file_size']
        file_id = dqy['file_id']
        access_hash_rec = dqy['access_hash_rec']
        dc_id = dqy['dc_ic']

        print(f"[*] Start dload ({file_name}) ({round(file_size / 1048576, 1)} MB)")
        url_down = f"https://shst{dc_id}.iranlms.ir/GetFile.ashx"
        head_down = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'file-id': str(file_id),
            'access-hash-rec': str(access_hash_rec),
            'start-index': '0',
            'last-index': '131072',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'auth': self.auth,
            'Origin': 'https://web.shad.ir',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'Referer': 'https://web.shad.ir/',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
            'Accept-Encoding': 'gzip, deflate'
        }

        sz_prt2 = 13107200
        part = 0
        total_part = math.ceil(file_size / sz_prt2)
        dl = 0
        if os.path.isfile(file_name):
            mode_f = 'ab'
            part = math.ceil((pathlib.Path(file_name).stat().st_size) / sz_prt2)
            dl = pathlib.Path(file_name).stat().st_size
        else:
            mode_f = 'wb'
        print(f"part: {part}, total: {total_part}")
        with open(file_name, mode_f) as myfile:
            while part < total_part:
                try:
                    if part != 0:
                        head_down['start-index'] = str(dl)
                    head_down['last-index'] = str(dl + sz_prt2)
                    if part + 1 == total_part:
                        head_down['last-index'] = str(file_size + 1)
                    req = requests.post(url_down, stream=True, headers=head_down, verify=False, timeout=5)
                    
                    #print(head_down)
                    for byte in req.iter_content(chunk_size=sz_prt):
                        dl += len(byte)
                        myfile.write(byte)
                        done = int(math.floor(50 * dl / file_size))
                        sys.stdout.write(f"\r{round(dl / file_size * 100, 1)}% [{'█' * done}{'░' * (50 - done)}] {round(dl / 1048576, 2)}")
                        sys.stdout.flush()
                    part += 1
                except Exception as err:
                    print("\njust a error: "+str(err)+". try again\n")
                    
            print('\n[+] download complete!')
