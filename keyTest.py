import requests, hmac, hashlib, base64, json
from datetime import datetime

timeStamp = datetime.today().strftime("%Y%m%d%H%M%S")
appKey = "l7xxsu3frR8WTl45Mcp0o9BQo2wGW54tyA4H"
secretKey = "AZvhnwYWU89EnUnEdR8RubyAQGv1CP57"

url = "https://gwapid.hanwhalife.com:8080/ldi/v1/hamldi_if_dev"

app_time = appKey + timeStamp

signiture = hmac.new(secretKey.encode(), app_time.encode(), digestmod=hashlib.sha512).digest()
hash_value = base64.b64encode(signiture).decode()
token = appKey + '|' + timeStamp + '|' + hash_value


payload= {
'key':'l7784e582f9cfd4af79163d2033951c40f',
'callType':'R',
'refid':'HAMRST030',
'refno':'2020072110065', # 날짜 변경
'funcNm':'',
'trnsDldt':'20200721',
'trnsDlngTime':'175357',
'procGb':'C',
'rfha':'',
'ranl':'0000100002291',
'rldepo':'AZ0015S101',
'sfhaart':'100',
'sfhazba':'0100',
'dbestand':'20200805',
'wgschft':'USD',
'khwkurs':'1189.1000', #환율
'setlType':'06',
'dzterm':'20200807',
'yjqty':'1330.0000', #금융상품 단위수 - 주수
'yjamt':'4163133.15', #약정금액(외화)
'idxamt':'31301753.01', #약정단가 (외화)
'susuryo':'1665.25', #수수료(외화)
'segum':'0', #세금 (외화)
'fiamt':'4164798.40',#정산금액(외화)
'yjamtK':'4950381628', #약정금액(원화)
'idxamtK':'3722091', #약정단가(원화)
'susuryoK':'1980148', #수수료(원화)
'segumK':'0', #세금(원화)
'fiamtK':'4952361776',#정산금액(원화)
'appmStAmt':'0',
'appmAddAmt':'0',
'rportb':'A0000',
'accountGroup':'AZ0015',
'valuationClass1039':'0005',
'operPart':'00377',
'manager':'190006A',
'taxPayType':'01',
'lastTr':'N',
'kontrh':'9051496379',
'hbkid':'JPMLO',
'hktid':'USD01',
'sglzb':'1010',
'trustAccountNum':'',
'accNo':'',
'accPttn':'01',
'hybridYn':'N',
'sharDebtDvsn':'01',
'valuationClass1109':'0002',
'fvociAsmtYn':'02',
'bsnsId':'',
'agreId':'',
'localCurr':'KRW'
}
payloadJson = json.dumps(payload).encode('UTF-8')
headers = {
  'Content-Type': 'application/json; charset=utf-8',
  'Accept': 'application/json',
  'Authorization': token,
  'HLI-Authorization': token,
  'cryp_dv_cd': '0'
}
response = requests.request("POST", url, headers=headers, data = payloadJson)
#json_data = response.json()
#with open('j.json','w',encoding='UTF-8-sig')as file:
#  print(file.write(json.dumps(json_data,ensure_ascii=False,indent='\t')))
print(response.text)