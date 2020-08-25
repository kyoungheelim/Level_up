from flask import Flask, render_template, request
import requests
import uuid, time, json, numpy, hmac, hashlib, base64, random
from datetime import datetime
from werkzeug.utils import secure_filename

# open api 추가부분
timeStamp = datetime.today().strftime("%Y%m%d%H%M%S")
appKey = "l7xxsu3frR8WTl45Mcp0o9BQo2wGW54tyA4H"
secretKey = "AZvhnwYWU89EnUnEdR8RubyAQGv1CP57"

trnsDldt = datetime.today().strftime("%Y%m%d")
trnsDlngTime = datetime.today().strftime("%H%M%S")
rannum = trnsDlngTime[:5]

refno = trnsDldt + rannum
url = "https://gwapid.hanwhalife.com:8080/ldi/v1/hamldi_if_dev"

app_time = appKey + timeStamp

signiture = hmac.new(secretKey.encode(), app_time.encode(), digestmod=hashlib.sha512).digest()
hash_value = base64.b64encode(signiture).decode()
token = appKey + '|' + timeStamp + '|' + hash_value
# open api 추가부분

URL = "https://31f5f933d64446b2a3e48fb118946790.apigw.ntruss.com/custom/v1/1994/7eb60930f549092a92229c1ae3918daa20b418bfe1bc002d1de7a9146db248f5/infer"
KEY = "WGdQbVFxb1JkSlR3Vm9kSlpnaXpYU1hnbEhiSHNNZ28="
api_url = URL
secret_key = KEY
tmp_file = '.'
#tmp_file = 'C:\Users\user\Desktop\untitle\untitled2'

app = Flask(__name__)
# OCR부분

#환율 -> 나중에 실시간 데이터 받던지 하기
KHWKURS = 1189.1000


@app.route('/upload', methods=['GET', 'POST'])
def render_file():
    return render_template('upload.html')


@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

        image_file = tmp_file + '/' + f.filename
        request_json = {
            'images': [
                {
                    'format': 'png',
                    'name': 'demo'
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }

        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = [
            ('file', open(image_file, 'rb'))
        ]
        headers = {
            'X-OCR-SECRET': secret_key
        }

        response = requests.post(api_url, data=payload, headers=headers, files=files)
        json_data = response.json()

        from collections import OrderedDict

        file_data = OrderedDict()

        jsonArray = json_data.get("images")
        for i, item in enumerate(jsonArray):
            file_data[item.get("title").get("name")] = item.get("title").get("inferText")
            jsonArray2 = item.get("fields")
            for j, item2 in enumerate(jsonArray2):
                file_data[item2.get("name")] = item2.get("inferText")

        print(json.dumps(file_data, ensure_ascii=False, indent='\t'))

        yjamtK = round(float(str(file_data['YJAMT']).replace(',','')) * KHWKURS)
        idxamtK = round(float(str(file_data['IDXAMT']).replace(',','')) * KHWKURS)
        susuryoK = round(float(str(file_data['SUSURYO']).replace(',','')) * KHWKURS)
        segumK = round(float(str(file_data['SEGUM']).replace(',','')) * KHWKURS)
        fiamtK = round(abs(float(str(file_data['FIAMT']).replace(',',''))) * KHWKURS)
        dbestand = str(file_data['DBESTAND']).replace('-','')
        dzterm = str(file_data['DZTERM']).replace('-','')

        payload = {
            'key': 'l7784e582f9cfd4af79163d2033951c40f',
            'callType': 'R',
            'refid': 'HAMRST030',
            'refno': refno , #'2020072110065',  # 날짜 변경
            'funcNm': '',
            'trnsDldt': str(trnsDldt),#'20200721',
            'trnsDlngTime': str(trnsDlngTime), #'175357',
            'procGb': 'C',
            'rfha': '',
            'ranl': '0000100002291',
            'rldepo': 'AZ0015S101',
            'sfhaart': '100',
            'sfhazba': '0100',
            'dbestand': dbestand, #'20200805',
            'wgschft': str(file_data['WGSCHFT']),
            'khwkurs': str(KHWKURS),#'1189.1000',  # 환율
            'setlType': '06',
            'dzterm': dzterm, #'20200807',
            'yjqty': str(file_data['YJQTY']).replace(',',''),#'1330.0000',  # 금융상품 단위수 - 주수
            'yjamt': str(file_data['YJAMT']).replace(',',''),#'4163133.15',  # 약정금액(외화)
            'idxamt': str(file_data['IDXAMT']),#'31301753.01',  # 약정단가 (외화)
            'susuryo': str(file_data['SUSURYO']).replace(',',''),#'1665.25',  # 수수료(외화)
            'segum': str(file_data['SEGUM']),#'0',  # 세금 (외화)
            'fiamt': str(file_data['FIAMT']).replace(',','').replace('-',''),#'4164798.40',  # 정산금액(외화)
            'yjamtK': str(yjamtK) , #'4950381628',  # 약정금액(원화)
            'idxamtK': str(idxamtK) ,#'3722091',  # 약정단가(원화)p
            'susuryoK': str(susuryoK), #'1980148',  # 수수료(원화)
            'segumK': str(segumK),#'0',  # 세금(원화)
            'fiamtK': str(fiamtK),#'4952361776',  # 정산금액(원화)
            'appmStAmt': '0',
            'appmAddAmt': '0',
            'rportb': 'A0000',
            'accountGroup': 'AZ0015',
            'valuationClass1039': '0005',
            'operPart': '00377',
            'manager': '190006A',
            'taxPayType': '01',
            'lastTr': 'N',
            'kontrh': '9051496379',
            'hbkid': 'JPMLO',
            'hktid': 'USD01',
            'sglzb': '1010',
            'trustAccountNum': '',
            'accNo': '',
            'accPttn': '01',
            'hybridYn': 'N',
            'sharDebtDvsn': '01',
            'valuationClass1109': '0002',
            'fvociAsmtYn': '02',
            'bsnsId': '',
            'agreId': '',
            'localCurr': 'KRW'
        }

        payloadJson = json.dumps(payload).encode('UTF-8')
        print(payloadJson)
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'Authorization': token,
            'HLI-Authorization': token,
            'cryp_dv_cd': '0'
        }
        response = requests.request("POST", url, headers=headers, data=payloadJson)
        print(response.text)

       # with open('words.json', 'w', encoding="utf-8") as make_file:
       #     json.dump(file_data, make_file, ensure_ascii=False, indent="\t")

        open('words.json', 'w', encoding="utf-8").write(response.text)
        #with open('words.json', 'w', encoding="utf-8") as make_file:
            #json.dump(response, make_file, ensure_ascii=False, indent="\t")

        return '파일 업로드 성공!!!'
        # return 'upload 디렉토리 -> 파일 업로드 성공!'


@app.route('/result', methods=['POST'])
def result():
    return open('words.json', 'r', encoding="utf-8").read()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
