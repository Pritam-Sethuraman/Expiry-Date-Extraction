from flask import Flask, jsonify, request

from genericpath import isfile
import json
import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./CloudVisionAPI-Key.json"

def find_mfg_exp(str):
    str = str.replace('\n',"  ")
    str = str.upper()

    mfg_date = None
    exp_date = None


    ## BEST BEFORE 
    dur = 0
    dur_in_years = 0
    word_to_num = ["ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN","ELEVEN","TWELVE","THIRTEEN","FOURTEEN","FIFTEEN","SIXTEEN","SEVENTEEN","EIGHTEEN","NINETEEN","TWENTY"]
    x = re.search("BEST BEFORE .* MONTHS", str)
    if x:
        # print(str)
        print(x.span())
        date = str[x.start() + 12:x.end() -7]
        date = date.replace(" ","")
        print(date)
        print("BEST BEFORE " + date + " MONTHS")
        if(date.isdigit()):
            duration = int(date)
            print(duration)
            dur = duration
        elif(date in word_to_num):
            dur = word_to_num.index(date)+1
        elif(date == "TWENTY FOUR"):
            dur = 24
        elif(date == "THIRTY SIX"):
            dur = 36
        print(dur)
    else:
        print("no best before in months")

    x = re.search("BEST BEFORE .* YEARS", str)
    if x:
        #print(x.span())
        date = str[x.start() + 12:x.end() -6]
        print(date)
        print("BEST BEFORE " + date + " YEARS")
        if(date.isdigit()):
            duration = int(date)
            print(duration)
            dur_in_years = duration
        elif(date in word_to_num):
            dur_in_years = word_to_num.index(date)+1
        elif(date == "TWENTY FOUR"):
            dur_in_years = 24
        elif(date == "THIRTY SIX"):
            dur_in_years = 36
        print(dur_in_years)
    else:
        print("no best before in years")

    x = re.search("EXPIRY .* MONTHS", str)
    if x:
        #print(x.span())
        date = str[x.start() + 7:x.end() -7]
        print(date)
        print("BEST BEFORE " + date + " MONTHS")
        if(date.isdigit()):
            duration = int(date)
            print(duration)
            dur = duration
        elif(date in word_to_num):
            dur = word_to_num.index(date)+1
        elif(date == "TWENTY FOUR"):
            dur = 24
        elif(date == "THIRTY SIX"):
            dur = 36
        print(dur)
    else:
        print("no expiry in months")


    x = re.search("EXPIRY .* YEARS", str)
    if x:
        #print(x.span())
        date = str[x.start() + 7:x.end() -6]
        print(date)
        print("BEST BEFORE " + date + " YEARS")
        if(date.isdigit()):
            duration = int(date)
            print(duration)
            dur_in_years = duration
        elif(date in word_to_num):
            dur_in_years = word_to_num.index(date)+1
        elif(date == "TWENTY FOUR"):
            dur_in_years = 24
        elif(date == "THIRTY SIX"):
            dur_in_years = 36
        print(dur_in_years)
    else:
        print("no expiry in years")


    ## DD MM YYYY
    x = re.findall("[0-3][0-9][.\s/-][0-1][0-9][.\s/-][0-2][09][0-9][0-9]", str)
    if x:
        print(x)
        for d in x:
            if(int(d[:2]) > 0 and int(d[:2]) < 32 and int(d[3:5]) > 0 and int(d[3:5]) < 13 and d[2] == d[5]):
                d = d[:2] + "/" + d[3:5] + "/" + d[6:]
                date = datetime.strptime(d,'%d/%m/%Y')
                # print(date)
                if(mfg_date is None):
                    mfg_date = date
                elif(mfg_date != date):
                    exp_date = date
    else:
        print("NO {DD MM YYYY}")

    # DD MM YY
    if(mfg_date is None and exp_date is None):
        x = re.findall("[0-3][0-9][.\s/-][0-1][0-9][.\s/-][0-9][0-9]", str)
        if x:
            print(x)
            for d in x:
                if(int(d[:2]) > 0 and int(d[:2]) < 32 and int(d[3:5]) > 0 and int(d[3:5]) < 13 and d[2] == d[5]):
                    d = d[:2] + "/" + d[3:5] + "/" + d[6:]
                    date = datetime.strptime(d,'%d/%m/%y')
                    print(date)
                    if(mfg_date is None):
                        mfg_date = date
                    elif(mfg_date != date):
                        exp_date = date
        else:
            print("NO {DD MM YY}")

    ## DD MON YYYY
    for2 = False
    months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","0CT","NOU","N0U","N0V","DEC"]
    if(mfg_date is None and exp_date is None):
        for mon in months:
            x = re.findall("[0-3][0-9][.\s-]{0,1}"+mon+"[.\s-]{0,1}[0-2][09][0-9][0-9]", str)
            if x:
                print(x)
                for2 = True
                x[0] = x[0].replace("0CT","OCT")
                x[0] = x[0].replace("NOU","NOV")
                x[0] = x[0].replace("N0U","NOV")
                x[0] = x[0].replace("N0V","NOV")
                for d in x:
                    print(d)
                    if(int(d[:2]) > 0 and int(d[:2]) < 32):
                        if(d[2] == "-" or d[2] == " "):
                            d = d[:2] + " " + d[3:]
                            date = datetime.strptime(d,'%d %b %Y')
                        elif(d[2] != " "):
                            date = datetime.strptime(d,'%d%b%Y')
                        # print("MFG: ")
                        print(date)
                        if(mfg_date is None):
                            mfg_date = date
                        elif(mfg_date != date):
                            exp_date = date
                    
        if (for2 == False):
            print("No Month in words")

    ## MM/YYYY
    if(mfg_date is None and exp_date is None):
        x = re.findall("[0-1][0-9][\s/-][0-2][09][0-9][0-9]", str)
        if x:
            for d in x:
                if(int(d[:2]) < 13 and int(d[:2]) > 0):
                    d = d[:2] + "/" + d[3:]
                    date = datetime.strptime(d,'%m/%Y')
                    print(date)
                    if(mfg_date is None):
                        mfg_date = date
                    elif(mfg_date != date):
                        exp_date = date
        else:
            print("NO {MM/YYYY}")

    ## MM YY
    if(mfg_date is None and exp_date is None):
        x = re.findall("[0-1][1-9][\s/-][0-9][0-9]", str)
        if x:
            print(x)
            
            for d in x:
                if(int(d[:2]) < 13 and int(d[:2]) > 0):
                    d = d[:2] + "/" + d[3:]
                    date = datetime.strptime(d,'%m/%y')
                    print(date)
                    if(mfg_date is None):
                        mfg_date = date
                    elif(mfg_date != date):
                        exp_date = date
        else:
            print("NO {MM YY}")

    ## EXPIRY DATE CALC
    expd = None
    if(dur != 0 and mfg_date is not None):
        expd = mfg_date + relativedelta(months=dur)
        print(expd)
    elif(dur_in_years != 0 and mfg_date is not None):
        expd = mfg_date + relativedelta(years=dur_in_years)
        print(expd)

    if(expd is not None):
        exp_date = expd

    if(exp_date is not None and mfg_date is not None and exp_date < mfg_date):
        t = exp_date
        exp_date = mfg_date
        mfg_date = t
    print("\nMANUFACTURING DATE IS ")
    print(mfg_date)
    print("EXPIRY DATE IS ")
    print(exp_date)
    print()
    return [mfg_date,exp_date]

def detect_text(path):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = path


    response = client.text_detection(image=image)
    texts = response.text_annotations
    if(len(texts) > 0):
        print('Text: '+texts[0].description+"\n")
        outputs = find_mfg_exp(texts[0].description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return outputs    

app = Flask(__name__)

# FOR TESTING: https://drive.google.com/file/d/1OW2bXINWlPGk8s2EqsB9gBIjGbowRs1c/view?usp=sharing 
@app.route("/")
def home_view():
        return "<h1>FYP 2022</h1>"

@app.route("/find", methods=["POST"])
def find_from_url():
        if 'url' in request.json:
                out = detect_text(request.json['url'])
                return jsonify(mfg_date = out[0], exp_date = out[1])
