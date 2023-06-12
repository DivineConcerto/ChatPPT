import time
import datetime
import schedule
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def log(str=""):
    print("[%s] %s" % (datetime.datetime.now(), str))


class ChatGPT(object):

    def __init__(self,port):
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:%d" % port)
        log("尝试在端口 %d 上连接浏览器" % port)
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}
        self.ask_cnt = 0
        self.model = '3'
        self.reply_cnt = 0
        self.wait_time = 0
        self.check_thread = threading.Thread(target=self.not_wait)
        self.check_thread.start()

    def __del__(self):
        self.driver.quit()

    def send(self, str="你好", delay=0.25):
        # 向GPT发送信息
        self.ask_cnt = self.ask_cnt+1
        txtbox = self.driver.find_element(By.CSS_SELECTOR, ".m-0")
        txtbox.click()
        time.sleep(delay)
        log("发送内容:"+repr(str))
        txtlines = str.split('\n')
        for txt in txtlines:
            txtbox.send_keys(txt)
            time.sleep(delay)
            txtbox.send_keys(Keys.SHIFT, Keys.ENTER)
            time.sleep(delay)
        txtbox.send_keys(Keys.ENTER)
        # 发送消息后，将等待时间清零。
        self.wait_time = 0
        time.sleep(delay)

    def get_answer_old(self):
        # 获取最近的一条回复（哪怕没有GPT没有说完）
        reply_str = self.driver.find_element(By.XPATH,f"/html/body/div[1]/div[2]/div/div/main/div[2]/div/div/div/div[{2*self.ask_cnt+1}]").text
        print(f"当前div值{2*self.ask_cnt+1}")
        return reply_str

    def transform(self):
        # 切换GPT3和GPT4模型
        if self.model == '3':
            self.ask_cnt = 0
            self.driver.get("https://chat.openai.com/?model=gpt-4")
            self.model = '4'
        elif self.model == '4':
            self.ask_cnt = 0
            self.driver.get("https://chat.openai.com/")
            self.model = '3'

    def reload(self):
        # 重新加载当前模型
        if self.model == '3':
            self.ask_cnt = 0
            self.driver.get("https://chat.openai.com/")

        elif self.model == '4':
            self.ask_cnt = 0
            self.driver.get("https://chat.openai.com/?model=gpt-4")

    def get_whole_answer(self):
        # 一次完整的问答，等待GPT回答完全后返回回答。（用于项目对接）
        log("等待回复中...")
        reply_str = ""
        # 判断ChatGPT是否正忙
        while self.driver.find_elements(By.CSS_SELECTOR, ".result-streaming") != []:
            pass
        elem_list = self.get_reply_list()
        for i in range(self.reply_cnt, len(elem_list)):
            reply_str += elem_list[i].text
            reply_str += "\n"
        log(reply_str)
        self.reply_cnt = len(elem_list)
        return reply_str, True

    def get_last_answer(self):
        reply_str = ""
        elem_list = self.get_reply_list()
        for i in range(self.reply_cnt, len(elem_list)):
            reply_str += elem_list[i].text
            reply_str += '\n'
        log(reply_str)
        self.reply_cnt = len(elem_list)
        return reply_str

    def get_reply_list(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".markdown > p")

    def not_wait(self):
        while True:
            time.sleep(5)
            self.wait_time += 5
            # 如果超过五分钟没有发消息，那么自动发送一条信息，防止GPT休眠。
            if self.wait_time >= 300:
                self.send(self.get_last_answer())


if __name__ == '__main__':
    chatgpt = ChatGPT(9222)
    time.sleep(10)
