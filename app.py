from flask import Flask, request, jsonify, render_template
from selenium.webdriver.common.by import By
import gpt
import threading


app = Flask(__name__)


# @app.route("/", methods=["GET"])
# def home():
#     return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt")
    print(prompt)
    chatgpt.send(prompt)
    response_text = chatgpt.get_last_answer()
    return jsonify({"response": response_text})


@app.route("/response")
def response():
    response_text = chatgpt.get_last_answer()
    return jsonify({"response": response_text})


@app.route('/check')
def check():
    if chatgpt.driver.find_elements(By.CSS_SELECTOR, ".result-streaming") != []:
        return jsonify({"response": "1"})
    else:
        return jsonify({"response": None})


@app.route('/transform')
def transform():
    chatgpt.transform()
    if chatgpt.model == '3':
        return "Successfully transformed to the GPT3.5"
    elif chatgpt.model == '4':
        return "Successfully transformed to the GPT4"


@app.route('/reload')
def reload():
    chatgpt.reload()
    return " Loaded successfully"


@app.route("/interview", methods=["POST"])
def interview():
    prompt = request.form.get("prompt")
    print(prompt)
    chatgpt.send(prompt)
    response_text = chatgpt.get_whole_answer()
    return jsonify({"response": response_text})


if __name__ == '__main__':
    chatgpt = gpt.ChatGPT(9222)
    app.run(debug=True, host='0.0.0.0', port=9999)
    print("程序已经成功启动！")
