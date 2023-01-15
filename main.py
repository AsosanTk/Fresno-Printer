# Fresno Printer for Raspberry Pi zero 
import sys
sys.path.append('/home/aso2023/.local/lib/python3.9/site-packages')
# escpos
from escpos.printer import Usb
from escpos import *

from time import sleep
# Pillow
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# Firebase
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("fresno-b2d00-firebase-adminsdk-pf0lo-4985caec23.json")
firebase_admin.initialize_app(cred)
#default_app = firebase_admin.initialize_app()
db = firestore.client()
ref = db.collection('ReceiptData')



# createReceipt
def createReceipt(doc):
    data = doc.to_dict()
    date = data['date']
    time = data['time']
    num = data['num']
    name = data['name']
    type = data['type']
    sum = data['sum']
    paid = data['paid']
    orderlist = data['orders']
    # head part: タイトル周辺
    head = Image.new('1', (width, 210), 255)
    drawhead = ImageDraw.Draw(head)
    drawhead.text((0,25), "Navy Bottle Coffee Kyoto", font=titlefont , fill=0)
    drawhead.text((0,80), "東京都世田谷区池尻4-7-1", anchor="ls", font=textfont , fill=0)
    drawhead.text((0,96), "筑駒高3喫茶班",  anchor="ls", font=textfont , fill=0)
    drawhead.text((width,80), date, anchor="ls", font=numberfont , fill=0)
    drawhead.text((width,96), time,  anchor="ls", font=numberfont , fill=0)
    drawhead.text((width/2,120), "お支払い", anchor="ms", font=textfont , fill=0)
    drawhead.line(((0,130), (width, 130)), fill=0, width=3)
    drawhead.text((0,144), "伝票名：", font=textfont , fill=0)
    drawhead.text((0,160), "レシート番号：", font=textfont , fill=0)
    drawhead.text((50,144), name, font=textfont , fill=0)
    drawhead.text((86,160), num, font=textfont , fill=0)
    drawhead.line(((0, 176), (width, 176)), fill=0, width=1)
    drawhead.text((width/2,190), type, anchor="lm", font=textfont, fill=0)
    drawhead.line(((0, 200), (width, 200)), fill=0, width=4)
    # body part: 項目の部分
    height = 50 * len(orderlist)
    body = Image.new('1', (width, height), 255)
    bodyhead = ImageDraw.Draw(body)
    for index, order in enumerate(orderlist):
        l = order.split(',')
        bodyhead.text((0, index*50 + 10), l[0] + " × " + str(l[1]), anchor="lm", font=textfont, fill=0)
        bodyhead.text((width, index*50 + 10), "¥"+str(l[2]), anchor="rm", font=numberfont, fill=0)
        bodyhead.text((0, index*50 + 28), l[3], anchor="lm", font=textfont, fill=0)

    # foot part: 合計金額のあたり
    foot = Image.new('1', (width, 90), 255)
    foothead = ImageDraw.Draw(foot)
    foothead.line(((0, 6), (width, 6)), fill=0, width=3)
    foothead.text((0,20), "合計", anchor="lm", font=textfont, fill=0)
    foothead.text((width,20), "¥"+str(sum), anchor="rm", font=largefont, fill=0)
    foothead.text((0,44), "現金", anchor="lm", font=textfont, fill=0)
    foothead.text((width,44), "¥"+str(paid), anchor="rm", font=largefont, fill=0)
    foothead.text((0,64), "お釣り", anchor="lm", font=textfont, fill=0)
    foothead.text((width,64), "¥"+str(paid-sum), anchor="rm", font=largefont, fill=0)
    # Print
    p = Usb(0x0416, 0x5011, 0)
    p.image(head)
    p.image(body)
    p.image(foot)
    p.cut()
    p.close()
    #head.save("head.jpg")
    #body.save("body.jpg")
    #foot.save("foot.jpg")
    db.collection("ReceiptData").document(num).delete()




# onUpdate
def onUpdate(docs, changes, read_time):
    docs = ref.get()
    for doc in docs:
        createReceipt(doc)
        



# 監視の開始、サブプロセスで動く
watcher = ref.on_snapshot(onUpdate)



# Print Settings
width = 384
titlefont = ImageFont.truetype('ZenKakuGothicNew-Medium.ttf', 34, encoding='unic')
largefont = ImageFont.truetype('ZenKakuGothicNew-Medium.ttf', 30, encoding='unic') # 合計金額
numberfont = ImageFont.truetype('ZenKakuGothicNew-Medium.ttf', 20, encoding='unic')
textfont = ImageFont.truetype('ZenKakuGothicNew-Regular.ttf', 18, encoding='unic')


while True:
    sleep(1)













