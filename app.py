from flask import Flask, render_template, request
import requests
import uuid, time, json, numpy
from werkzeug.utils import secure_filename
#임경희 찬양?!

URL = "https://31f5f933d64446b2a3e48fb118946790.apigw.ntruss.com/custom/v1/1994/7eb60930f549092a92229c1ae3918daa20b418bfe1bc002d1de7a9146db248f5/infer"
KEY = "WGdQbVFxb1JkSlR3Vm9kSlpnaXpYU1hnbEhiSHNNZ28="
api_url = URL
secret_key = KEY
tmp_file = '.'
#tmp_file = 'C:\Users\user\Desktop\untitle\untitled2'

app = Flask(__name__)
# OCR부분


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

#        response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
        response = requests.post(api_url, data=payload, headers=headers, files=files)
        json_data = response.json()

        from collections import OrderedDict

        file_data = OrderedDict()

#        file_data[json_data.get("title").get("name")] = json_data.get("title").get("inferText")
#        jsonArray = json_data.get("fields")

#        for i, item in enumerate(jsonArray):
#            file_data[item.get("name")] = item.get("inferText")


        jsonArray = json_data.get("images")
        for i, item in enumerate(jsonArray):
            file_data[item.get("title").get("name")] = item.get("title").get("inferText")
            jsonArray2 = item.get("fields")
            for j, item2 in enumerate(jsonArray2):
                file_data[item2.get("name")] = item2.get("inferText")

        print(json.dumps(file_data, ensure_ascii=False, indent='\t'))

        with open('words.json', 'w', encoding="utf-8") as make_file:
            json.dump(file_data, make_file, ensure_ascii=False, indent="\t")

        return '파일 업로드 성공!!!'
        # return 'upload 디렉토리 -> 파일 업로드 성공!'


@app.route('/result', methods=['POST'])
def result():
    return open('words.json', 'r', encoding="utf-8").read()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
