import json
import os
import uuid

from flask import Flask, jsonify
from flask import request
from flask import send_from_directory

import danmaku2ass

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    return "<p>Hello, World!</p>"


@app.route("/clear", methods=['POST'])
def clear():
    if request.form.get('token', 'none') not in tokens:
        return jsonify({
            "status": 503,
            "info": "拒绝访问"
        })
    for file in tempFiles:
        os.remove(file)
    return jsonify({
        "status": 200
    })


@app.route("/makeAss", methods=['POST'])
def makeAss():
    if request.form.get('token', 'none') not in tokens:
        return jsonify({
            "status": 503,
            "info": "拒绝访问"
        })
    f = request.files['file']
    inputArgs = request.form.to_dict()
    tempFileName = str(uuid.uuid4()) + ".xml"
    tempOutput = str(uuid.uuid4()) + ".ass"
    f.save(tempFileName)
    f.close()
    danmaku2ass.Danmaku2ASS(input_files=tempFileName,
                            input_format=inputArgs.get("format", "autodetect"),
                            output_file=tempOutput,
                            stage_width=int(inputArgs.get("width", 1920)),
                            stage_height=int(inputArgs.get("height", 1080))
                            )
    tempFiles.append(tempFileName)
    tempFiles.append(tempOutput)
    return send_from_directory(os.getcwd(), tempOutput, as_attachment=True)


with open("../conf/tokens.json") as f:
    tokens = json.load(f).get('tokens', [])
tempFiles = []
if __name__ == '__main__':
    app.run("0.0.0.0", 7082, debug=False)
