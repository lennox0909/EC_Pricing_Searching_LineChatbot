#!/usr/bin/env python
# coding: utf-8

# In[1]:


# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'This is Flask Server testing...'


# In[2]:


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import json

secretFileContentJson=json.load(open("./line_secret_key",'r'))
server_url=secretFileContentJson.get("server_url")

app = Flask(__name__)

line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))



# In[3]:


'''
PYMS爬蟲機器人
【PChome 24h購物】
【momo購物網】
【Yahoo奇摩購物中心】
【蝦皮購物】
'''

import requests
import json
import urllib.parse
from bs4 import BeautifulSoup


def PMY_crawler(search_key_word):
    
    '''PChome'''
    def query(search_key_word, page):
        p = requests.get(
            "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=" + search_key_word + "&page=" + page + "&sort=sale/dc",
            headers={
                "Host": "ecshweb.pchome.com.tw",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive",
                "Referer": "https://ecshweb.pchome.com.tw/search/v3.3/?q=PC",
                "Cookie": "ECC=2752f4b0986bf85b5a5e9b810032ba7e257d9401.1566461528; _gcl_au=1.1.1321705795.1566461530; gsite=shopping; _ga=GA1.3.1054014464.1566461531; _gid=GA1.3.530024540.1566461531; venguid=26faaa5b-9890-44c3-99f0-417c8346eb1d.wg1-mfrp20190822; _gat_UA-115564493-1=1; _fbp=fb.2.1566461530978.1209721921; U=9be237e08db2f6663e123d10b40913f5232f631c; ECWEBSESS=3bc8e04aca.16dae7ebef34465e8429c2ff07996585541f4e5c.1566461551",
                "TE": "Trailers"
            }
        )
        p.encoding = "utf8"
        j = json.loads(p.text)
        return j

    page = "1"

    j2 = query(search_key_word, page)
    p_name_list = []
    p_price_list = []
    p_url_list = []
    p_imgurl_list = []
    try:
        for a in j2["prods"]:
            # print(a["name"], "NT$"+str(a["price"]))
            p_name = a["name"]
            p_name_list.append(p_name)
            p_price = "$" + str(a["price"])
            p_price_list.append(p_price)
            p_imgurl = "https://b.ecimg.tw" + a["picB"]
            p_imgurl_list.append(p_imgurl)
            p_url = "https://24h.pchome.com.tw/prod/" + a["Id"]
            p_url_list.append(p_url)
    except:
        p_name_list = []
        p_price_list = []
        p_url_list = []
        p_imgurl_list = []


    '''Yahoo'''

    # y_in = str(input("search:"))
    y_query = search_key_word.replace(" ", "%20")
    yurl = "https://tw.buy.yahoo.com/search/product?p=" + y_query

    res = requests.get(yurl)
    soup = BeautifulSoup(res.text, 'html.parser')

    y_name_list = []
    y_price_list = []
    y_url_list = []
    y_imgurl_list = []
    
    try:
        for a1 in soup.find_all("li", class_="BaseGridItem__grid___2wuJ7"):
            # print(type(a1))
            y_name = a1.find("img").attrs["alt"]
            y_name_list.append(y_name)
            y_url = a1.find("a").attrs["href"]
            y_url_list.append(y_url)
            img = a1.find("img").attrs["srcset"]
            y_imgurl = img.split(" ", 20)[-4]
            y_imgurl_list.append(y_imgurl)
            y_price = a1.find("em").text
            y_price_list.append(y_price)
            # print(y_name,y_price,y_url,y_imgurl)
            # print("----------")
    except:
        y_name_list = []
        y_price_list = []
        y_url_list = []
        y_imgurl_list = []


    ''' MOMO '''

    STORE = 'momo'
    MOMO_MOBILE_URL = 'http://m.momoshop.com.tw/'
    MOMO_QUERY_URL = MOMO_MOBILE_URL + 'mosearch/%s.html'
    USER_AGENT_VALUE = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    encoded_query = urllib.parse.quote(search_key_word)
    query_url = MOMO_QUERY_URL % encoded_query
    headers = {'User-Agent': USER_AGENT_VALUE}
    resp = requests.get(query_url, headers=headers)
    resp.encoding = 'UTF-8'
    momo_bea = BeautifulSoup(resp.text, 'html.parser')

    m_name_list = []
    m_price_list = []
    m_url_list = []
    # m_imgurl_list = []
    try: 
        for element in momo_bea.find(id='itemizedStyle').ul.find_all('li'):
            m_name = element.find('p', 'prdName').text
            m_name_list.append(m_name)
            m_price = element.find('b', 'price').text.replace(',', '')
            if not m_price:
                continue
            m_price = int(m_price)
            m_price_list.append(m_price)
            m_url = MOMO_MOBILE_URL + element.find('a')['href']
            m_url_list.append(m_url)
            # m_img_url = element.a.img['src']
    except:
        m_name_list = []
        m_price_list = []
        m_url_list = []
    
    '''蝦皮購物'''
    
    serch_shopee = search_key_word.replace(" ","%20")
    url_shopee = "https://shopee.tw/api/v2/search_items/?by=relevancy&keyword="+serch_shopee+"&limit=50&newest=0&order=desc&page_type=search"
    shopee_headers={

    "Host": "shopee.tw",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Accept": "*/*",
    "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "X-API-SOURCE": "pc",
    "If-None-Match-": "55b03-27399beaee5c409d58a8c0fbe1b57eb7",
    "Cache-Control": "max-age=0",
    "TE": "Trailers"

    }
    p_shopee = requests.get(url_shopee,headers=shopee_headers)
    p_shopee.encoding = "utf8"
    j_shopee = json.loads(p_shopee.text)

    s_name_list = []
    s_price_list = []
    s_url_list = []
    try:
        for a in j_shopee["items"][5:]:
            name = a["name"]
            nameurl = name.replace(" ","-").replace("/","-")
            price = "$"+str(int(a["price"]/100000))
            price_min = a["price_min"]/100000
            price_max= a["price_max"]/100000
            brand = a["brand"]
            shopid = str(a["shopid"])
            itemid = str(a["itemid"])
            url = "https://shopee.tw/"+nameurl+"-i."+shopid+"."+itemid
            s_name_list.append(name)
            s_price_list.append(price)
            s_url_list.append(url)
    
    except:
        try:
            for a in j_shopee["items"][5:]:
                name = a["name"]
                nameurl = name.replace(" ","-").replace("/","-")
    #             price = "$"+str(int(a["price"]/100000))
    #             price_min = a["price_min"]/100000
    #             price_max= a["price_max"]/100000
                brand = a["brand"]
                shopid = str(a["shopid"])
                itemid = str(a["itemid"])
                url = "https://shopee.tw/"+nameurl+"-i."+shopid+"."+itemid
                s_name_list.append(name)
    #             s_price_list.append(price)
                s_url_list.append(url)
                for i in range(len(s_name_list)):
                    s_price_list.append("點連結看價格")
                
            
        except:
            s_name_list = []
            s_price_list = []
            s_url_list = []
    
    
    
    return [p_name_list,
            p_price_list,
            p_url_list,
            m_name_list,
            m_price_list,
            m_url_list,
            y_name_list,
            y_price_list,
            y_url_list,
            s_name_list,
            s_price_list,
            s_url_list
            ]


# In[4]:


# test = input("key:")
# PMYresult = PMY_crawler(test)
# print(PMYresult[0][0])
# print(PMYresult[9][0])


# In[5]:


'''

handler處理文字消息
收到用戶回應的文字消息，
進行爬蟲後，
將消息回傳給用戶

'''

# 引用套件
from linebot.models import (
    MessageEvent, TextMessage
)



# 文字消息處理
@handler.add(MessageEvent,message=TextMessage)
def process_text_message(event):

    # 讀取本地檔案，並轉譯成消息
#     result_message_array =[]
#     replyJsonPath = "./dynamic_reply/"+event.message.text+"/reply.json"
#     result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

    PMYresult = PMY_crawler(event.message.text)
    count = 5    
    
    
    '''PChome 24h購物'''
    try:
        pc_len = len(PMYresult[0])
        print("PChome 24h購物",pc_len)
        for i in range(pc_len):
            PMYresult[0][i]="\n"+PMYresult[0][i]
            PMYresult[1][i]="\n價格："+str(PMYresult[1][i])
            PMYresult[2][i]="\n"+PMYresult[2][i]+"\n"

        pp =["【PChome 24h購物】\n"]
        pchome=""
        if pc_len>=count:
            j=0
            while j<count:
                i=0
                while i <=2:
                    a = str(PMYresult[i][j])
                    pp.append(a)
                    i = i+1
                j = j+1

            for i in pp:
                pchome+=i
        else:
            j=0
            while j<pc_len:
                i=0
                while i <=2:
                    a = str(PMYresult[i][j])
                    pp.append(a)
                    i = i+1
                j = j+1

            for i in pp:
                pchome+=i
        
        if pc_len ==0:
            pchome = "【PChome 24h購物】\n未找到商品；嘗試不同或更常見的關鍵字"


    except:
        pchome = "【PChome 24h購物】\n未找到商品；嘗試不同或更常見的關鍵字"

    '''momo購物網'''
        
    try:
        mo_len = len(PMYresult[3])
        print("momo購物網",mo_len)
        for i in range(mo_len):
            PMYresult[3][i]="\n"+PMYresult[3][i]
            PMYresult[4][i]="\n價格："+str(PMYresult[4][i])
            PMYresult[5][i]="\n"+PMYresult[5][i]+"\n"

        
        mm =["【momo購物網】\n"]
        momo=""
        if mo_len>=count:
            j=0
            while j<count:
                i=3
                while i <=5:
                    b = str(PMYresult[i][j])
                    mm.append(b)
                    i = i+1
                j = j+1

            for i in mm:
                momo+=i
        else:
            j=0
            while j<mo_len:
                i=3
                while i <=5:
                    b = str(PMYresult[i][j])
                    mm.append(b)
                    i = i+1
                j = j+1

            for i in mm:
                momo+=i
                
        if mo_len ==0:
            momo = "【momo購物網】\n未找到商品；嘗試不同或更常見的關鍵字"

    except:
        momo = "【momo購物網】\n未找到商品；嘗試不同或更常見的關鍵字"

    '''Yahoo奇摩購物中心'''
        
    try:
        ya_len = len(PMYresult[6])
        print("Yahoo奇摩購物中心:",ya_len)
        for i in range(ya_len):
            PMYresult[6][i]="\n"+PMYresult[6][i]
            PMYresult[7][i]="\n價格："+str(PMYresult[7][i])
            PMYresult[8][i]="\n"+PMYresult[8][i]+"\n"

        
        yy =["【Yahoo奇摩購物中心】\n"]
        yahoo=""
        if ya_len>=count:
            j=0
            while j<count:
                i=6
                while i <=8:
                    c = str(PMYresult[i][j])
                    yy.append(c)
                    i = i+1
                j = j+1

            for i in yy:
                yahoo+=i
        else:
            j=0
            while j<ya_len:
                i=6
                while i <=8:
                    c = str(PMYresult[i][j])
                    yy.append(c)
                    i = i+1
                j = j+1

            for i in yy:
                yahoo+=i
        if ya_len == 0:
            yahoo = "【Yahoo奇摩購物中心】\n未找到商品；嘗試不同或更常見的關鍵字"

    except:
        yahoo = "【Yahoo奇摩購物中心】\n未找到商品；嘗試不同或更常見的關鍵字"
    
    '''蝦皮購物'''
    
    try:
        sho_len = len(PMYresult[9])
        print("蝦皮購物:",sho_len)
        print(PMYresult[10])
        for i in range(sho_len):
            PMYresult[9][i]="\n"+PMYresult[9][i]
            PMYresult[10][i]="\n價格："+str(PMYresult[10][i])
            PMYresult[11][i]="\n"+PMYresult[11][i]+"\n"

        
        ss =["【蝦皮購物】\n"]
        shopee=""
        if sho_len>=count:
            j=0
            while j<count:
                i=9
                while i <=11:
                    d = str(PMYresult[i][j])
                    ss.append(d)
                    i = i+1
                j = j+1

            for i in ss:
                shopee+=i
        else:
            j=0
            while j<sho_len:
                i=9
                while i <=11:
                    d = str(PMYresult[i][j])
                    ss.append(d)
                    i = i+1
                j = j+1

            for i in ss:
                shopee+=i
        if sho_len == 0:
            shopee = "【蝦皮購物】\n未找到商品；嘗試不同或更常見的關鍵字"

    except:
        shopee = "【蝦皮購物】\n未找到商品；嘗試不同或更常見的關鍵字"
        
    
    
    
    
    
    
#     print(PMYresult[9])
    
    # 消息清單
    reply_message_list = [
    TextSendMessage(text= pchome),
    TextSendMessage(text= momo),
    TextSendMessage(text= yahoo),
    TextSendMessage(text= shopee),
#     TextSendMessage(text="您查詢的關鍵字："),
    TextSendMessage(text=event.message.text)
#     TextSendMessage(text="請輸入商品名，繼續查詢\n可運用空格 區隔多組關鍵字")
    ]
#     print("pchome==>",pp)
#     print("momo==>",mm)
#     print("yahoo==>",yy)

    # 發送
    line_bot_api.reply_message(
        event.reply_token,
        reply_message_list
    )


# In[6]:


'''

消息判斷器

讀取指定的json檔案後，把json解析成不同格式的SendMessage

讀取檔案，
把內容轉換成json
將json轉換成消息
放回array中，並把array傳出。

'''

# 引用會用到的套件
from linebot.models import (
    ImagemapSendMessage,TextSendMessage,ImageSendMessage,LocationSendMessage,FlexSendMessage
)

from linebot.models.template import (
    ButtonsTemplate,CarouselTemplate,ConfirmTemplate,ImageCarouselTemplate
    
)

from linebot.models.template import *

import json

def detect_json_array_to_new_message_array(fileName):
    
    #開啟檔案，轉成json
    with open(fileName, encoding='utf8') as f:
        jsonArray = json.load(f)
    
    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')
        
        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))    

    # 回傳
    return returnArray


# In[7]:


'''

handler處理文字消息

收到用戶回應的文字消息，
按文字消息內容，往素材資料夾中，找尋以該內容命名的資料夾，讀取裡面的reply.json

轉譯json後，將消息回傳給用戶



# 引用套件
from linebot.models import (
    MessageEvent, TextMessage
)

# 文字消息處理
@handler.add(MessageEvent,message=TextMessage)
def process_text_message(event):

    # 讀取本地檔案，並轉譯成消息
    result_message_array =[]
    replyJsonPath = "./dynamic_reply/"+event.message.text+"/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

    # 發送
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )
'''


# In[8]:


'''

handler處理Postback Event

載入功能選單與啟動特殊功能

解析postback的data，並按照data欄位判斷處理

現有三個欄位
menu, folder, action, fontcolor, fontsize

若folder欄位有值，則
    讀取其reply.json，轉譯成消息，並發送

若menu欄位有值，則
    讀取其rich_menu_id，並取得用戶id，將用戶與選單綁定
    讀取其reply.json，轉譯成消息，並發送

'''
from linebot.models import (
    PostbackEvent
)

from urllib.parse import parse_qs 

from linebot.models import (CameraRollAction,QuickReplyButton, QuickReply)
from linebot.models import TextSendMessage

@handler.add(PostbackEvent)
def process_postback_event(event):
    
    user_profile = line_bot_api.get_profile(event.source.user_id)
    print(user_profile)
    print(type(user_profile))
#     print(user_profile["userId"])

    # 解析data
    query_string_dict = parse_qs(event.postback.data)
    
    print(query_string_dict)
    #在data欄位裡面有找到folder
    #folder=abcd&tag=xxx
    if 'folder' in query_string_dict:
    
        result_message_array =[]

        # 去素材資料夾下，找abcd資料夾內的reply,json
        replyJsonPath = 'dynamic_reply/'+query_string_dict.get('folder')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
  
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )
    elif 'menu' in query_string_dict:

        linkRichMenuId = open("./richmenu/"+query_string_dict.get('menu')[0]+'/rich_menu_id', 'r').read()
        line_bot_api.link_rich_menu_to_user(event.source.user_id,linkRichMenuId)
        

    elif 'action' in query_string_dict:
        
        if query_string_dict.get('action')[0] == 'usr_upload_pic':

            print("請執行usr_upload_pic()")
            print(query_string_dict.get('action')[0])
#             usr_upload_pic()
            
            
            '''
            準備QuickReply的Button
            '''
            # 創建QuickReplyButton
            ## 點擊後，切換至照片相簿選擇
            cameraRollQRB = QuickReplyButton(
                action=CameraRollAction(label="選擇照片")
            )
            '''
            以QuickReply封裝該些QuickReply Button
            '''
            quickReplyList = QuickReply(
                items = [cameraRollQRB]
            )
            '''
            製作TextSendMessage，並將剛封裝的QuickReply放入
            '''
            ## 將quickReplyList 塞入TextSendMessage 中 
            
            
            quickReplyTextSendMessage = TextSendMessage(text='請點↓選擇照片↓', quick_reply=quickReplyList)  
            '''
            設計一個字典
            '''
            template_message_dict = {
                "我要上傳照片":quickReplyTextSendMessage
            }
            '''
            用戶發送文字消息時，會按此進行消息處理
            '''
            # 用戶發出文字消息時， 按條件內容, 回傳合適消息
            @handler.add(MessageEvent, message=TextMessage)
            def handle_message(event):
                line_bot_api.reply_message(
                    event.reply_token,
                    template_message_dict.get(event.message.text)
                )
        
        


# In[9]:


'''
用戶follow事件
'''

'''

製作文字與圖片的教學訊息

'''
# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

# 消息清單
# welcome_message_list = [
# TextSendMessage(text="一鍵查詢三大購物網！/n規格/n價格、商品比一比/n查詢商品是否上架"),
# TextSendMessage(text="【PChome 24h購物】/n【Yahoo奇摩購物中心】/n【momo購物網】"),
#     ImageSendMessage(original_content_url='https://%s/images/003.jpeg' %server_url ,
#     preview_image_url='https://%s/images/001.jpg' %server_url),
#     ImageSendMessage(original_content_url='https://%s/images/004.png' %server_url,
#     preview_image_url='https://%s/images/005.jpg' %server_url)
# ]


from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage)

# 載入Follow事件
from linebot.models.events import (
    FollowEvent
)

# 載入requests套件
import requests


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
        
     # 將用戶資訊存在檔案內
    with open("./users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile),sort_keys=True))
        myfile.write('\r\n')
        
        
    # 將菜單綁定在用戶身上
    linkRichMenuId=secretFileContentJson.get("rich_menu_id")
    linkMenuEndpoint='https://api.line.me/v2/bot/user/%s/richmenu/%s' % (event.source.user_id, linkRichMenuId)
    linkMenuRequestHeader={'Content-Type':'image/jpeg','Authorization':'Bearer %s' % secretFileContentJson["channel_access_token"]}
    lineLinkMenuResponse=requests.post(linkMenuEndpoint,headers=linkMenuRequestHeader)
    
    # 去素材資料夾下，找abcd資料夾內的reply,json
    replyJsonPath = "./dynamic_reply/UserGuide/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
    
    # 回覆文字消息與圖片消息
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )


# In[10]:



# def usr_upload_pic():
    
#     # 引入相關套件
#     from linebot.models import (CameraRollAction,QuickReplyButton, QuickReply)
#     '''
#     準備QuickReply的Button
#     '''
#     # 創建QuickReplyButton
#     ## 點擊後，切換至照片相簿選擇
#     cameraRollQRB = QuickReplyButton(
#         action=CameraRollAction(label="選擇照片")
#     )
#     '''
#     以QuickReply封裝該些QuickReply Button
#     '''
#     quickReplyList = QuickReply(
#         items = [cameraRollQRB]
#     )
#     '''
#     製作TextSendMessage，並將剛封裝的QuickReply放入
#     '''
#     ## 將quickReplyList 塞入TextSendMessage 中 
#     from linebot.models import TextSendMessage
    
#     quickReplyTextSendMessage = TextSendMessage(text='請點↓選擇照片↓', quick_reply=quickReplyList)

#     def handle_message(event):
#         line_bot_api.reply_message(
#             user_profile,
#             quickReplyTextSendMessage)

    

#     '''
#     設計一個字典
#     '''
#     template_message_dict = {
#         "0909":quickReplyTextSendMessage
#     }
#     '''
#     用戶發送文字消息時，會按此進行消息處理
#     '''
#     # 用戶發出文字消息時， 按條件內容, 回傳合適消息
#     @handler.add(MessageEvent, message=TextSendMessage)
#     def handle_message(event):
#         line_bot_api.reply_message(
#             event.reply_token,
#             quickReplyTextSendMessage
#         )


# In[11]:


# app.run()


# In[12]:


'''
Application 運行（heroku版）
'''

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])


# In[ ]:


'''
Mac local端啟動Server
'''

# if __name__=="__main__":
#     app.run(host='0.0.0.0')


# In[ ]:




