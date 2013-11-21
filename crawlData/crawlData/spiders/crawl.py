# -*- coding:UTF-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.conf import settings
from scrapy.xlib.pydispatch import dispatcher
from pymongo import Connection 
import datetime,time,re,string
from scrapy import signals
import smtplib
from email.mime.text import MIMEText
import pymongo
def connect():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    conn = pymongo.Connection()
    return conn.cnwdlm

mailto_list = ['zhouqiao0418@gmail.com','zhouqiao0418@gmail.com']

mail_host = "smtp.gmail.com"
mail_user = ""
mail_pass = ""
mail_postfix = "gmail.com"
def send_mail(to_list,sub,content):

    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    try: 
        s = smtplib.SMTP() 
        s.connect(mail_host)
        s.starttls()
        s.ehlo()
        s.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()

        return True
    except Exception, e:
        print str(e)
        return False


def saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner):
        data = {'_id':link_url,'apr':apr,'money':money,'rate_of_process':rate_of_process,'flag':flag,'create_time':create_time,'borrow_type':borrow_type,'borrow_name':borrow_name,'name':name,'link_url':link_url,'loan_period':loan_period,'borrow_id':borrow_id,'company_name':company_name,'repayment_manner':repayment_manner}
        connect().bids.save(data)
#美贷 
class Meidai(BaseSpider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider,reason):
        if reason == 'finished':
            pass
        else:
            log.msg("This crawl is broken" + reason,level=ERROR)
        connect().bids.update({"company_name":u"美贷","flag":{"$gt":0}},{"$inc":{"flag":-1}},multi=True)

    name = 'meidai' 
    allowed_domains = ['www.meidaiw.com']
    start_urls =['http://www.meidaiw.com/invest/index.html']

    def parse(self,response):       

        hxs = HtmlXPathSelector(response)
        urls = hxs.select("//table[@id='invList']/tbody/tr")
        for item in urls:
            url = item.select("td/div/div[2]/div[1]/a[2]//@href").extract()[0].strip()
            url = 'http://www.meidaiw.com' + url  
            yield Request(url,callback = self.getData)


    def getData(self,response): 
            try:
                hxs = HtmlXPathSelector(response)
                apr = hxs.select("//body/div[3]/div/div/table/tbody/tr/td[4]/span/text()").extract()[0].strip()[:-1]
                apr = float(apr)
                money = hxs.select("//body/div[3]/div/div/table/tbody/tr[2]/td[2]/span/text()").extract()[0].strip()[1:]    
                money = float(money)   
                # calculate loan rate_of_process
                alreadyLend = hxs.select("/html/body/div[3]/div/div/table/tbody/tr[2]/td[4]/text()").extract()[0].strip()   [:-1]
                surplus = hxs.select("/html/body/div[3]/div/div/table/tbody/tr[2]/td[6]/text()").extract()[0].strip()   [:-1]
                lend = ''
                beLeftOver = ''
                for i in surplus:
                    if ord(i) >= 48 and ord(i) <= 57:
                        beLeftOver += i
                for i in alreadyLend:
                    if ord(i) >= 48 and ord(i) <= 57:
                        lend += i
                total = int(lend) + int(beLeftOver)
                rate_of_process = (float(lend)/total)*100
                rate_of_process = round(rate_of_process)
                flag = 2
                create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                borrow_type = u'流转标'
                borrow_name = hxs.select("/html/body/div[3]/div[2]/div[2]/div[2]/div[1]/text()").extract()[0].strip()
                borrow_name = re.search('\w+',borrow_name).group()
                name = hxs.select("/html/body/div[3]/div[1]/div[1]/div[1]/text()").extract()[0].strip()
                link_url = response.url
                judge = hxs.select("/html/body/div[3]/div/div/table/tbody/tr[1]/td[6]/text()").extract()[0].strip()[-1:]
                loan_period = hxs.select("/html/body/div[3]/div/div/table/tbody/tr/td[6]/span/text()").extract()[0].strip() 
                if judge == u'月': 
                    loan_period = int(loan_period)*30   
                else:
                    loan_period = int(loan_period)
                borrow_id = re.search('\d+',link_url).group()
                company_name = u'美贷'
                repayment_manner = hxs.select("/html/body/div[3]/div[1]/div[1]/table/tbody/tr[3]/td[6]/text()").extract()[0].strip()
                saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner)
            except Exception,e:
                flag = 0
                e = 'meidai\'s function ge happened Exception,that Exception is:' + str(e) 
                send_mail(mailto_list,"Exception report",e)


#畅贷网
class cdai(BaseSpider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider,reason):
        if reason == 'finished':
            pass
        else:
            log.msg("This crawl is broken" + reason,level=ERROR)
        connect().bids.update({"company_name":u"畅贷网","flag":{"$gt":0}},{"$inc":{"flag":-1}},multi=True)
    name = 'cdai'
    allowed_domains = ['www.51qian.com']
    start_urls = ['http://www.51qian.com/Loan']

    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select("//div[@class='leftcont']/div")
        urls = urls[:-1]
        for item in urls:
            url = item.select("div[2]/div[1]/a[1]/@href").extract()[0].strip()
            url = 'http://www.51qian.com' + url
            yield Request(url,callback = self.getData)

    def getData(self,response):
        try:
            hxs = HtmlXPathSelector(response)
            try:
                apr = hxs.select("//div[@id='DetailUNRight']/div[3]/ul/li[1]/span/text()").extract()[0].strip()
                apr = apr[:-1]
                apr = float(apr)
            except:
                apr = ''
            money = hxs.select("//div[@id='DetailUNRight']/div[2]/ul/li/span/text()").extract()[0].strip()[1:]
            money = int(money)
            rate_of_process = hxs.select("//div[@id='jindutiao']/img/@width").extract()[0].strip()
            rate_of_process = float(rate_of_process)
            rate_of_process = ("%.1f" %rate_of_process)
            flag = 2
            create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            borrow_type = u'其他标'
            borrow_name = hxs.select("//*[@id='DetailNameAreaRight']/a/text()").extract()[0].strip()
            name = hxs.select("//div[@id='ListTitle']/text()").extract()[0].strip()
            link_url = response.url
            judge = hxs.select("//*[@id='ProjectContent']/ul/li[2]/text()[2]").extract()[0].strip()
            loan_period = hxs.select("//div[@id='DetailUNRight']/div/ul/li[2]/span/text()").extract()[0].strip()
            if judge[-1:] == u'月':
                loan_period = int(loan_period)*30
            else:
                loan_period = int(loan_period)
            borrow_id = hxs.select("//*[@id='DBLoan_Id']/@value").extract()[0].strip()
            company_name = u'畅贷网'
            repayment_manner = hxs.select("//*[@id='DetailUserName']/div[2]/div[4]/ul/li/text()").extract()[0].strip()
            repayment_manner = repayment_manner[5:]
            saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner)
        except:
            flag = 0
            e = 'meidai\'s function ge happened Exception,that Exception is:' + str(e) 
            send_mail(mailto_list,"Exception report",e)

#你我贷
class nwdai(BaseSpider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider,reason):
        if reason == 'finished':
            pass
        else:
            log.msg("This crawl is broken" + reason,level=ERROR)
        connect().bids.update({"company_name":u"你我贷","flag":{"$gt":0}},{"$inc":{"flag":-1}},multi=True)
    name = 'nwdai'
    allowed_domains = ['www.niwodai.com']
    start_urls = ['http://www.niwodai.com/touzi/']

    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select("//div[@class='contentLeft']/div")
        for item in urls:
            url = item.select("div[2]/h2/a/@href").extract()[0].strip()
            url = 'http://www.niwodai.com' + url
            yield Request(url,callback=self.getData)

    def getData(self,response):
        try:
            hxs = HtmlXPathSelector(response)
            apr = hxs.select("//div[@id='detail']/ul[1]/li[2]/strong/text()").extract()[0].strip()
            money = hxs.select("//div[@id='detail']/ul[1]/li/strong/text()").extract()[0].strip()
            money = float(money)
            rate_of_process = hxs.select("//div[@id='detail']/ul[1]/li[7]/i/text()").extract()[0].strip()
            rate_of_process = re.search("\d+.?\d*",rate_of_process).group()
            rate_of_process = float(rate_of_process)
            flag = 2
            create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            borrow_type = hxs.select("//*[@id='detail']/div/a[1]/@class").extract()[0].strip()
            if borrow_type == 'xyb':
                borrow_type = u'信用标'
            else:
                borrow_type = u'其他标'
            borrow_name = hxs.select("//*[@id='item']/div[1]/div[1]/text()").extract()[1].strip()
            name = hxs.select("//*[@id='detail']/div/h2/text()").extract()[0].strip()
            link_url = response.url
            loan_period = hxs.select("//div[@id='detail']/ul[1]/li[5]/text()").extract()[0].strip()
            if loan_period[-1:] == u'月':
                loan_period = float(loan_period[-3:-2])*30
            else:
                loan_period = float(loan_period[-3:-2])
            borrow_id = str(response.url.split(r'/')[-1:])
            borrow_id = borrow_id.split(r'.')[0]
            borrow_id = borrow_id[2:-1]
            company_name = u'你我贷'
            repayment_manner = hxs.select("//*[@id='detail']/ul/li[3]/text()").extract()[0].strip()[-4:]
            saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner)
        except:
            flag = 0
            e = 'meidai\'s function ge happened Exception,that Exception is:' + str(e) 
            send_mail(mailto_list,"Exception report",e)

#拍拍贷
class ppdai(BaseSpider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider,reason):
        if reason == 'finished':
            pass
        else:
            log.msg("This crawl is broken" + reason,level=ERROR)
        connect().bids.update({"company_name":u"拍拍贷","flag":{"$gt":0}},{"$inc":{"flag":-1}},multi=True)
    name = 'ppdai'
    allowed_domains = ['www.ppdai.com']
    start_urls = ['http://www.ppdai.com/lend/default.aspx?page=1&']

    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        loanPage = hxs.select("//div[@class='listpage']/table[1]/tr[1]/td[1]/text()").extract()[0].strip()[1:-1]
        sumPage = int(loanPage)
        for i in xrange(0,(sumPage+1)):
            item = str(i)
            item = 'http://www.ppdai.com/lend/default.aspx?page='+ item +'&'
        # get sumPage  and circulate
            yield Request(item,callback = self.getLoanList)
    def getLoanList(self,response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select("//div[@class='Listings_Lend']/table/tr[@class='tr']")
 
        for item in items:
            url = item.select("td[2]/div/a/@href").extract()[0]
            url = 'http://www.ppdai.com' + url
            yield Request(url,callback = self.getData)
    def getData(self,response):
        try:
            hxs = HtmlXPathSelector(response)
            apr = hxs.select("//table[@class='listInfo']/tr[2]/td[2]/span[1]/text()").extract()[0].strip()
            apr = float(apr)
            money = hxs.select("//table[@class='listInfo']/tr[1]/td[2]/span[1]/text()").extract()[0][1:].strip()[1:]
            money = money.replace(',','')
            money = float(money)
            rate_of_process = hxs.select("//table[@class='listInfo']/tr[5]/td[2]/div[2]/span[1]/text()").extract()[0].strip()
            rate_of_process = float(rate_of_process)
            flag = 2
            create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            borrow_type = u'其他标'
            borrow_name = hxs.select("//div[@class='smallInfo']/ul/li[1]/a/text()").extract()[0].strip()
            name = hxs.select("//h1[@class='listTitleNew']/text()").extract()[0].strip()
            link_url = response.url
            loan_period = hxs.select("//table[@class='listInfo']/tr[2]/td[4]/text()").extract()[0].strip()
            if loan_period[-1:] == u'月':
                loan_period = float(loan_period[:-2])*30
            else:
                loan_period = float(loan_period[:-2])
            print loan_period
            borrow_id = re.search("\d+",link_url).group()
            company_name = u'拍拍贷'
            repayment_manner = hxs.select("//table[@class='listInfo']/tr[3]/td[2]/text()").extract()[0].strip()
            saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner)
        except:
            flag = 0
            e = 'meidai\'s function ge happened Exception,that Exception is:' + str(e) 
            send_mail(mailto_list,"Exception report",e)

#融信贷
class rxdai(BaseSpider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider,reason):
        if reason == 'finished':
            pass
        else:
            log.msg("This crawl is broken" + reason,level=ERROR)
        connect().bids.update({"company_name":u"融信贷","flag":{"$gt":0}},{"$inc":{"flag":-1}},multi=True)
    name = 'rxdai'
    allowed_domains = ['www.rxdai.com']
    start_urls = ['http://www.rxdai.com/invest/index.html']

    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select("//div[@id='investListPage']/table[1]/tr[1]/td[1]/div[1]/b/text()").extract()[0].strip()[1:-1]
        num = int(urls)/10 + 2
        for url in range(1, num):
            item = 'http://www.rxdai.com/invest/index'+ str(url) + '.html'
            yield Request(item,callback = self.getLoanList) 
 
        #yield Request('http://www.rxdai.com/invest/index.html',callback=self.parse_detail) 

    def getLoanList(self,response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select("//div[@id='investListMid']/div[@class='investList']") 

        for item in items:
            url = item.select("div[2]/ul[1]/li[1]/label[1]/a/@href").extract()[0][:5]
            url = 'http://www.rxdai.com/invest/'+url+'.html' 
            yield Request(url,callback = self.getData)  

    def getData(self,response):
        try:
            hxs = HtmlXPathSelector(response)
            apr = hxs.select("//div[@id='investMoney']/span[2]/font/text()").extract()[0].strip()[:-1]
            apr = float(apr) 
            money = hxs.select("//div[@id='investMoney']/span[1]/font/text()").extract()[0].strip()[1:]
            money = float(money) 
            rate_of_process = hxs.select("//div[@id='investOther']/span[1]/font[2]/text()").extract()[0].strip()[:-1]
            rate_of_process = float(rate_of_process)
            flag = 2
            create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            borrow_type = hxs.select("//*[@id='investTitle2']/img[1]/@src").extract()[0].strip()
            borrow_type = str(borrow_type.split('/')[-1:])
            if 'jin' in borrow_type:
                borrow_type = u'净值标'
            elif 'miao' in borrow_type:
                borrow_type = u'秒还标'
            else:
                borrow_type = u'其他标'
            borrow_name = hxs.select("//*[@id='investContent3_Up']/span[1]/a/text()").extract()[0].strip()
            name = hxs.select("//*[@id='investTitle2']/text()").extract()[1].strip()
            link_url = response.url
            loan_period = hxs.select("//div[@id='investMoney']/span[2]/text()").extract()[1].strip()[-3:]
            if loan_period[-1:] == u'月':
                loan_period = ''.join([i for i in loan_period if i.isdigit()])
                loan_period = float(loan_period)*30
            else:
                loan_period = ''.join([i for i in loan_period if i.isdigit()])
                loan_period = float(loan_period)
            print loan_period
            borrow_id = re.search('\d+',link_url).group()
            company_name = u'融信贷'
            repayment_manner = hxs.select("//*[@id='investOther']/span[4]/text()").extract()[0].strip()
            saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner)
        except:
            flag = 0
            e = 'meidai\'s function ge happened Exception,that Exception is:' + str(e) 
            send_mail(mailto_list,"Exception report",e)


#安心贷
class axdai(BaseSpider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider,reason):
        if reason == 'finished':
            pass
        else:
            log.msg("This crawl is broken" + reason,level=ERROR)
        connect().bids.update({"company_name":u"安心贷","flag":{"$gt":0}},{"$inc":{"flag":-1}},multi=True)
    name = 'axdai'
    allowed_domains = ['www.anxin.com']
    start_urls = ['http://www.anxin.com/invest/default.html']

    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select("//table[@id='invList']/tr")
        for item in urls:
            url = item.select("td/div[1]/div[2]/div[1]/a[2]/@href").extract()[0]
            url = 'http://www.anxin.com' + url
            yield Request(url,callback = self.getData)

    def getData(self,response):
        try:
            hxs = HtmlXPathSelector(response)
            apr = hxs.select("//div[@class='dv_detail_5']/table/tr/td[4]/span/text()").extract()[0].strip()[:-1]
            apr = float(apr)
            money = hxs.select("//div[@class='dv_detail_5']/table/tr[2]/td[2]/span/text()").extract()[0].strip()
            money = money[1:]
            money = money.replace(',','')
            money = float(money)

            alreadyLend = hxs.select("//div[@class='dv_detail_5']/table/tr[2]/td[4]/text()").extract()[0].strip()[:-1]
            surplus = hxs.select("//span[@id='Span1']/text()").extract()[0].strip()[:-1]
            loanSum = float(alreadyLend) + float(surplus)
            rate_of_process = (float(alreadyLend)/loanSum)*100.0 
            rate_of_process = ('%.2f' %rate_of_process)
            flag = 2
            create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            borrow_type = u'流转标'
            borrow_name = hxs.select("//div[@class='dv_r_7']/div[1]/text()").extract()[0].strip()
            borrow_name = re.search('\w+',borrow_name).group()
            name = hxs.select("//div[@class='dv_detail_5']/div/text()[1]").extract()[0].strip()
            link_url = response.url
            loan_period = hxs.select("//div[@class='dv_detail_5']/table/tr[1]/td[6]/span/text()").extract()[0].strip()
            loan_period = float(loan_period)*30
            borrow_id = re.search('\d+',link_url).group()
            company_name = u'安心贷'
            repayment_manner = u'其他标'
            saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner)
        except:
            flag = 0
            e = 'meidai\'s function ge happened Exception,that Exception is:' + str(e) 
            send_mail(mailto_list,"Exception report",e)

#中融资本
class zrzb(BaseSpider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider,reason):
        if reason == 'finished':
            pass
        else:
            log.msg("This crawl is broken" + reason,level=ERROR)
        connect().bids.update({"company_name":u"中融资本","flag":{"$gt":0}},{"$inc":{"flag":-1}},multi=True)
    name = 'zrzb'
    allowed_domains = ['www.zhongrongziben.com']
    start_urls = ['http://www.zhongrongziben.com/invest/index.html']

    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        loanSum = hxs.select("/html/body/div[2]/div[2]/div[13]/text()").extract()[0].strip()[:5]
        loanSum = int(re.search('\d+',loanSum).group())
        loanPage = loanSum/10 + 2
        for i in range(1,loanPage):
            url = 'http://www.zhongrongziben.com/invest/index.html?page=' + str(i)
            yield Request(url,callback = self.getLoanList)

    def getLoanList(self,response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select("/html/body/div[2]/div[2]/div[@class='credit']")
        for item in items:
            url = item.select("div/ul[1]/li/a[1]/@href").extract()[0].strip()
            url = 'http://www.zhongrongziben.com' + url
            yield Request(url,callback = self.getData)

    def getData(self,response):
        try:
            hxs = HtmlXPathSelector(response)
            apr = hxs.select("//*[@id='main']/div[2]/div[1]/div[2]/ul[1]/li[2]/strong/text()").extract()[0].strip()[:-1]
            apr = float(apr)
            money = hxs.select("//*[@id='main']/div[2]/div[1]/div[2]/ul[1]/li[1]/strong/text()").extract()[0].strip()[:-1]
            money = int(money)
            rate_of_process = hxs.select("//*[@id='main']/div[2]/div[1]/div[2]/ul[2]/li[2]/div[2]/text()").extract()[0].strip()
            rate_of_process = float(re.search('\d+',rate_of_process).group())
            flag = 2
            create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            borrow_type = hxs.select("//*[@id='main']/div[2]/div[1]/div[2]/h2/a[2]/img/@src").extract()[0].strip()
            if 'jin' in borrow_type:
                borrow_type = u'净值标'
            elif 'xiang' in borrow_type:
                borrow_type = u'流转标'
            else:
                borrow_type = u''
            borrow_name = hxs.select("//*[@id='main']/div[2]/div[1]/div[1]/p[1]/a/text()").extract()[0].strip()
            name = hxs.select("//*[@id='main']/div[2]/div[1]/div[2]/h2/span/text()").extract()[0].strip()
            link_url = response.url
            loan_period = hxs.select("//*[@id='main']/div[2]/div[1]/div[2]/ul[1]/li[5]/text()").extract()[0].strip()
            if loan_period[-1:] == u'月':
                loan_period = re.search('\d+',loan_period).group()
                loan_period = float(loan_period)*30
            else:
                loan_period = re.search('\d+',loan_period).group()
                loan_period = float(loan_period)
            borrow_id = re.search('\d+',link_url).group()
            company_name = u'中融资本'
            repayment_manner = hxs.select("//*[@id='main']/div[2]/div[1]/div[2]/ul[1]/li[3]/text()").extract()[0].strip()[5:]
            saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner)
        except:
            flag = 0
            e = 'meidai\'s function ge happened Exception,that Exception is:' + str(e) 
            send_mail(mailto_list,"Exception report",e)

#

class RenJuSpider(BaseSpider): 

    '''
    人人聚财贷爬虫.编号:NO.8,此虫特点：取出各元素集合，如titles
    '''

    name = 'renju'
    allowed_domains = ['renrenmoney.com']
    start_urls = ['http://www.renrenmoney.com/tender/index.html']

    def get_sql(self, block):
        name = block.select("td[2]/ul/li[1]/a/text()").extract()[0].strip()
        borrow_id = block.select("td[2]/ul/li[1]/a/@href").extract()[0].split('/')[-1].split('.')[0][1:].strip()
        url = 'http://www.renrenmoney.com/invest/a' + borrow_id + '.html'
        money = ''.join([ i for i in block.select("td[3]/ul/li[1]/font/text()").extract()[0].strip() if i.isdigit() or i=='.'])
        money = float(money)
        money = int(money)
        # 年化，double类型
        temp = block.select("td[3]/ul/li[2]/font/text()").extract()[0]
        apr = temp.split(u'，')[0].strip()[:-1].strip()
        apr = float(apr)
        #print title + '  ' + borrow_id + '  ' + url + '  '+ money + '   '  + apr 
        ## 还款类型： eg. 按月分期还款
        repayment_type = block.select("td[5]/ul/li[2]/text()").extract()[0][5:].strip()
        ## 借款期限 eg.1天  1个月  varchar类型
        loan_period = temp.split(u'，')[-1].strip()
        if loan_period[-1:] == u'月':
            loan_period = re.search(r'\d+',loan_period).group()
            loan_period = int(loan_period)*30
        else:
            loan_period = re.search(r'\d+',loan_period).group()
            loan_period = int(loan_period)
        ## 借款时间 eg: YYYY-mm-dd HH:ii:ss
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        ## 借款进度 double类型
        rate_of_process = block.select("td[4]/ul/li[2]/span/text()").extract()[0].split('%')[0].strip() 
        rate_of_process = float(rate_of_process)
        data ={"_id":url,"apr":apr,"money":money,"rate_of_process":rate_of_process,"create_time":create_time,"name":name,"link_url":url,"loan_period":loan_period,"borrow_id":borrow_id,"repayment_type":repayment_type,"flag":3,"company_name":'人人聚财'}
        connect().bids.save(data)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        biaos = hxs.select("//div[@id='intd1']/div[@class='invest_list']/table/tr[@class='tr1']")
        for biao in biaos:
            self.get_sql(biao)



#红岭创投
class HLingSpider(BaseSpider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider,reason):
        if reason == 'finished':
            pass
        else:
            log.msg("This crawl is broken" + reason,level=ERROR)
        connect().bids.update({"company_name":u"红岭创投","flag":{"$gt":0}},{"$inc":{"flag":-1}},multi=True)
    '''
    红岭爬虫.编号NO.3，该爬虫特点，模拟登录，模拟post请求获取各页内容，然后吞噬数据！
    '''

    name = 'hling'
    
    allowed_domains = ['www.my089.com']
    start_urls = ['https://www.my089.com/login.aspx']

    def parse(self, response):
        return [FormRequest.from_response(response, formdata={'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtUserName':'klokkl','ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtPwd':'klokkl'},callback = self.after_login)]
    
    def after_login(self, response):
        yield Request(url='http://www.my089.com/Loan/Default.aspx',callback = self.parse_list)

    def parse_list(self, response):
        hxs = HtmlXPathSelector(response)
        vs = hxs.select("//body/form//input[@id='__VIEWSTATE']/@value").extract()[0]
        ea = hxs.select("//body/form//input[@id='__EVENTVALIDATION']/@value").extract()[0]
        count =  len(list(hxs.select("//div[@id='main']/div[2]/div[2]/div/div/div/a")))# count of page
        count = string.atoi(str(count))# 获取 页码数
        # 提交每页的 请求
        for i in xrange(count):
            yield FormRequest(url='http://www.my089.com/Loan/Default.aspx', formdata = {
                                '__EVENTTARGET':'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$Pagination1$lBtn'+str(i+1),
                                '__EVENTARGUMENT':'',
                                '__EVENTVALIDATION':ea,
                                '__VIEWSTATE':vs,
                                },
                                callback = self.parse_test)
    def parse_test(self, response):
        hx = HtmlXPathSelector(response)
        items = hx.select("//div[@id='main']/div[2]/div[2]/table/tr")
        for item in items:
            #标题
            # 标种
    
            apr_temp = item.select("td/div/span/text()").extract()[1].strip()
            apr = apr_temp[3:-3] if apr_temp[-1]==u'年' else string.atof(apr_temp[3:-3])*12
            apr = float(apr)
            #金钱 （格式化）
            money = ''.join([ i for i in item.select("td/div/span/text()").extract()[0].strip() if i.isdigit() or i=='.' ])
            money = float(money)
            rate_of_process = item.select("td/div/span[2]/span/span/text()").extract()[0].strip()[:-1]
            rate_of_process = int(rate_of_process)
            flag = 2
            create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            borrow_type = u'净值标'
            borrow_name = item.select("td/div/span[3]/span/text()").extract()[0].strip()
            name = item.select("td/div/dl/dt/span[1]/a/text()").extract()[0]
            link_url = response.url
            loan_period = item.select("td/div/span/text()").extract()[7].strip()
            if loan_period[-1:] == u'月':
                loan_period = re.search(r'\d+',loan_period).group()
                loan_period = float(loan_period)*30
            else:
                loan_period = re.search(r'\d+',loan_period).group()
                loan_period = float(loan_period)
            borrow_id = ''
            company_name = u'红岭创投'
            repayment_manner = item.select("td/div/span[3]/span/text()").extract()[0].strip()
            saveData(apr,money,rate_of_process,flag,create_time,borrow_type,borrow_name,name,link_url,loan_period,borrow_id,company_name,repayment_manner)

            # print title,money,apr,loan_period,rate_of_process

