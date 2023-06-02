import time
import datetime
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
        time.sleep(delay)

    def getAnswer(self):
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

    def GetWholeAnswer(self):
        # 一次完整的问答，等待GPT回答完全后返回回答。（用于项目对接）
        log("等待回复中...")
        reply_str = ""
        # 判断ChatGPT是否正忙
        while self.driver.find_elements(By.CSS_SELECTOR, ".result-streaming") != []:
            pass
        elemList = self.getReplyList()
        for i in range(self.reply_cnt, len(elemList)):
            reply_str += elemList[i].text
            reply_str += "\n"
        log(reply_str)
        self.reply_cnt = len(elemList)
        return reply_str, True

     # 获取ChatGPT回复列表
    def getReplyList(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".markdown > p")


if __name__ == '__main__':
    chatgpt = ChatGPT(9222)
    time.sleep(10)
