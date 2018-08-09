# -*- coding: utf-8 -*-
# Some websites needs extras.

from util.web.proxies import ProxiesRequests

from pytesseract import image_to_string
from PIL import Image

from re import findall
from io import StringIO

def ziroom_extra(rtn_data):
    '''ziroom_extra
    Ziroom Extra func.
    
    '''
    print("Test xxxxx")
    price_dict = dict()

    price, price_dict = get_price_from_png(rtn_data["price"], price_dict)
    
    rtn_data["price"] = price

    payment_rtn_list = list()
    for payment in rtn_data["paymentlist"]:
        payment_rtn = dict()
        for k, v in zip(payment.keys(), payment.values()):
            if k == "period":
                payment_rtn["period"] = v
            else:
                payment_rtn[k], price_dict = get_price_from_png(v, price_dict)
                
        payment_rtn_list.append(payment_rtn)

    rtn_data["paymentlist"] = payment_rtn_list

    return rtn_data

def get_price_from_png(price_object, price_dict):
    '''get_price_from_png
    Get price info from png files by using tesseract OCR.
    
    '''
    try:
        print("Quick DEBUG")
        price = StringIO()
        url = "http:{}".format(price_object[0])

        if url in price_dict.keys():
            t = price_dict[url]
        else:
            img_path = "_output/{}".format(findall(r"/([0-9a-zA-z]+.png)", url)[0])
            req = ProxiesRequests([url])
            ctn = req.req_content_list[0][0]

            # ctn = requests.get(url).content

            with open(img_path, "wb") as img:
                img.write(ctn)

            img         = Image.open(img_path)
            bg          = Image.new("RGBA", img.size, "white")
            merged_pic  = Image.new("RGBA", tuple([int(s*1.2) for s in img.size]), "white")
            mg          = Image.alpha_composite(bg, img)
            
            merged_pic.paste(mg)
            t = image_to_string(merged_pic)
            
            # remove(img_path)

        for idx in price_object[2]:
            price.write(t[idx])

        price_dict[url] = t

        return price.getvalue(), price_dict

    except Exception as e:
        print("Err:", e)
        return "", price_dict

    finally:
        price.close()