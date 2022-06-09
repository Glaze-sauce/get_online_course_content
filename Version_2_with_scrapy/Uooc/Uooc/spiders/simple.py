import re
import time
import emoji
import scrapy
import prettytable as pt
from selenium.webdriver.common.by import By

from Uooc.items import UoocItem
from Uooc.register import register

class SimpleSpider(scrapy.Spider):
    name = "simple"
    base_url = ["http://www.uooc.net.cn/home/learn/index#/223942046"]

    def start_requests(self):
        self.driver,self.chapter_names,self.chapter_ids = register()
        yield scrapy.Request(url=self.driver.current_url,callback=self.parse)


    def parse(self, response):
        
        # 结构
            # 章 chapter
            ## 节 sub
            ### 小节 sub_sub

        time.sleep(2)
        item = UoocItem()
        tb = pt.PrettyTable()
        tb.field_names = ["状态","章节","时间"]
        tb.align = "l"
        tb.min_width,tb.max_width = 25,25
        for (self.chapter_id,chapter_name) in zip(self.chapter_ids,self.chapter_names):
            self.driver.get("{}/{}".format(self.base_url[0],self.chapter_id))
            self.driver.implicitly_wait(5)
            time.sleep(3)
            tb.start
            tb.add_row(["开始抓取"+"  "+emoji.emojize(":beginner:",use_aliases=True)*3,chapter_name,time.asctime()])
            print(tb)
            tb.clear_rows()
            # 每一节
            self.subs = self.driver.find_elements(by=By.XPATH,value="//li[@class='ng-scope']")
            # 先进行视频学习，遍历每一节
            for self.sub in self.subs:
                if self.sub != self.subs[-1]:
                    # 逐个点击
                    self.sub.click()
                    time.sleep(1)
                    # 获取`节`名称
                    sub_name = self.driver.find_element(by=By.XPATH,value="//li[@class='ng-scope']//div[@class='oneline ng-binding active']").text
                    # 看看该 `节` 有没有嵌套的 `小节` 的情况
                    self.sub_subs = self.driver.find_elements(by=By.XPATH,value="//li[@class='ng-scope']//div[@class='oneline ng-binding active']/following::ul/li")
                    # print(len(sub_subs))

                    # 如果有嵌套 `小节` 
                    if self.sub_subs != []:

                        
                        # ！重点来了，这是最难的地方
                        
                        # 遍历每一个 `小节`

                        # 1. 有一些 `节` 是先有一个视频，然后再嵌套 `小节` 的  ===> try:
                        # 2. 有一些 `节` 是直接嵌套 `小节` 的
                        

                        try:
                            # 检查当前 `节` 下面有没有 `先放视频`
                            self.driver.find_element(by=By.CSS_SELECTOR,value="div.resourcelist.ng-scope > div")
                            # 如果有，就先拿这些在 `小节` 前面的视频
                            # (只有当上面这行代码没报错，下面这段 `try:` 里的代码才能被执行)
                            self.content = self.driver.find_elements(by=By.CSS_SELECTOR,value="div.resourcelist.ng-scope > div")
                            for self.i in self.content:
                                time.sleep(1)
                                self.i.click()
                                self.driver.implicitly_wait(5)
                                time.sleep(2)
                                caption_source = self.driver.find_element(by=By.CSS_SELECTOR,value="div.learn-main-left > div > div > div").get_attribute("source")
                                caption = "，".join([j.split(':"')[1][:-1] for j in re.findall(r'caption":".*?"',caption_source)])
                                item["chapter_name"] = chapter_name
                                item["sub_name"    ] = sub_name
                                item["sub_url"     ] = self.driver.current_url
                                item["caption"     ] = caption
                                item["choice"      ] = "---"
                                yield item

                            for self.sub_sub in self.sub_subs:
                                self.sub_sub.click()
                                time.sleep(1)
                                sub_sub_name = self.driver.find_element(by=By.XPATH,value="//li[@class='ng-scope']/div/div[@class='oneline ng-binding active']").text
                                time.sleep(1)
                                # 现在才获取 `小节` 里面的视频
                                self.content = self.driver.find_elements(by=By.CSS_SELECTOR,value="div.resourcelist.ng-scope > div")[1:]
                                # 遍历 `小节` 下的视频
                                for self.i in self.content:
                                    time.sleep(1)
                                    self.i.click()
                                    self.driver.implicitly_wait(5)
                                    time.sleep(5)
                                    caption_source = self.driver.find_element(by=By.CSS_SELECTOR,value="div.learn-main-left > div > div > div").get_attribute("source")
                                    caption = "，".join([j.split(':"')[1][:-1] for j in re.findall(r'caption":".*?"',caption_source)])
                                    item["chapter_name"] = chapter_name
                                    item["sub_name"    ] = sub_name+"\r"+sub_sub_name
                                    item["sub_url"     ] = self.driver.current_url
                                    item["caption"     ] = caption
                                    item["choice"      ] = "---"
                                    yield item
                        except:
                            # 如果没有在 `小节` 前放视频，就运行下面这段
                            for self.sub_sub in self.sub_subs:
                                self.sub_sub.click()
                                time.sleep(1)
                                sub_sub_name = self.driver.find_element(by=By.XPATH,value="//li[@class='ng-scope']/div/div[@class='oneline ng-binding active']").text
                                time.sleep(1)
                                # 获取 `小节` 下的 “几个”
                                self.content = self.driver.find_elements(by=By.CSS_SELECTOR,value="div.resourcelist.ng-scope > div")
                                # 遍历 `小节` 下的视频
                                for self.i in self.content:
                                    time.sleep(1)
                                    self.i.click()
                                    self.driver.implicitly_wait(5)
                                    time.sleep(5)
                                    caption_source = self.driver.find_element(by=By.CSS_SELECTOR,value="div.learn-main-left > div > div > div").get_attribute("source")
                                    caption = "，".join([j.split(':"')[1][:-1] for j in re.findall(r'caption":".*?"',caption_source)])
                                    item["chapter_name"] = chapter_name
                                    item["sub_name"    ] = sub_name+"\r"+sub_sub_name
                                    item["sub_url"     ] = self.driver.current_url# self.start_urls[0]+"/"+sub.get_attribute("id")
                                    item["caption"     ] = caption
                                    item["choice"      ] = "---"
                                    yield item
                    # 如果没嵌套 `小节`，那就简单多了
                    else:
                        self.sub_subs = [""]
                        for self.sub_sub in self.sub_subs:
                            self.content = self.driver.find_elements(by=By.CSS_SELECTOR,value="div.resourcelist.ng-scope > div")
                            for self.i in self.content:
                                self.i.click()
                                self.driver.implicitly_wait(5)
                                time.sleep(5)
                                caption_source = self.driver.find_element(by=By.CSS_SELECTOR,value="div.learn-main-left > div > div > div").get_attribute("source")
                                caption = "，".join([j.split(':"')[1][:-1] for j in re.findall(r'caption":".*?"',caption_source)])
                                item["chapter_name"] = chapter_name
                                item["sub_name"    ] = sub_name
                                item["sub_url"     ] = self.driver.current_url
                                item["caption"     ] = caption
                                item["choice"      ] = "---"
                                yield item
                # 最后一节是考试
                else:
                    self.sub.click()
                    time.sleep(1)
                    sub_name = self.driver.find_element(by=By.XPATH,value="//li[@class='ng-scope']/div/div[@class='oneline ng-binding active']").text
                    self.content  = self.driver.find_elements(by=By.CSS_SELECTOR,value="div.resourcelist.ng-scope > div")[:1]
                    for self.i in self.content:
                        self.i.click()
                        # 先填上去, 这样才不会使字典的键值对长度不齐
                        item["chapter_name"] = chapter_name
                        item["sub_name"    ] = sub_name
                        item["sub_url"     ] = self.driver.current_url
                        item["caption"     ] = "---"

                        time.sleep(1)
                        # 考试的页面是嵌套了 html 的, 所以需要转换一下 frame
                        self.driver.switch_to.frame(self.driver.find_element(by=By.CSS_SELECTOR,value="body > div.ng-scope > div > div.learn-main.clearfix > div.learn-main-left > div > div > div > iframe"))
                        
                        # 拿出所有题目
                        quesion = [ques.text for ques in self.driver.find_elements(by=By.CSS_SELECTOR,value="div.queBox > div > div > div > div.ti-q > div")]
                        
                        # 拿出题目的 ABCD 选项
                        choice_answer_A = ["A. "+ans.text for ans in self.driver.find_elements(by=By.CSS_SELECTOR,value="div.ti-alist.ng-scope > label:nth-child(1) > div")]
                        choice_answer_B = ["B. "+ans.text for ans in self.driver.find_elements(by=By.CSS_SELECTOR,value="div.ti-alist.ng-scope > label:nth-child(2) > div")]
                        choice_answer_C = ["C. "+ans.text for ans in self.driver.find_elements(by=By.CSS_SELECTOR,value="div.ti-alist.ng-scope > label:nth-child(3) > div")]
                        choice_answer_D = ["D. "+ans.text for ans in self.driver.find_elements(by=By.CSS_SELECTOR,value="div.ti-alist.ng-scope > label:nth-child(4) > div")]
                        choice_answer_true = ["正确答案: "+true.text for true in self.driver.find_elements(by=By.CSS_SELECTOR,value="div.answerBox > div:nth-child(2) > div")]

                        # 看看有没有填空题
                        fill_answer_true = [true.text for true in self.driver.find_elements(by=By.CSS_SELECTOR,value="div.answerBox > div:nth-child(2) > div > div")]
                        
                        # 如果有填空题
                        if fill_answer_true != []:

                            # 填入填空题的答案
                            fill = [n for m in [[quesion[i],fill_answer_true[i-(len(quesion)-len(fill_answer_true))]] for i in range(len(quesion)-len(fill_answer_true),len(quesion))] for n in m]
                        
                        # 如果没有填空题
                        else:
                            fill = ["没有填空题"]

                        # 把选择题的信息拼接起来
                        choice = [n for m in [[quesion[i],choice_answer_A[i]+" "+choice_answer_B[i]+" "+choice_answer_C[i]+" "+choice_answer_D[i],choice_answer_true[i]] for i in range(len(quesion)-len(fill_answer_true))] for n in m]
                        
                        # 再次覆盖
                        choice.extend(fill)
                        item["choice"] = "\r".join(choice)
                        yield item
            tb.add_row(["抓取完成"+"  "+emoji.emojize(":hotsprings:",use_aliases=True)*3,chapter_name,time.asctime()])
            print(tb)
            tb.clear_rows()


    def close(self, spider):
        self.driver.quit()
        print(emoji.emojize(":triangular_flag_on_post:",use_aliases=True)*3)
