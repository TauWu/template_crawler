# -*- coding: utf-8 -*-
# Some websites needs extras.

from util.web.proxies import ProxiesRequests
from util.redis import RedisController
from constant.config import conf_kv_func
from util.common.logger import LogBase

from pytesseract import image_to_string
from PIL import Image

from re import findall
from io import StringIO

def ziroom_extra(project_name, rid, rtn_data):
    '''ziroom_extra
    Ziroom Extra func.
    
    '''
    logger = LogBase(project_name, "ziroom_extra")
    logger.debug("Before Extra =>", data=rtn_data)
    # Extra func for house code.
    try:
        end = rtn_data['house_code'].split('_')[1]
    except Exception:
        pass
    else:
        end = int(end)
        if end > 1:
            rds = RedisController(int(conf_kv_func("ziroom.sys_config", all=True)['redis_db']), project_name)
            for idx in range(1, end):
                rds.__update_dict_to_redis__(rid-idx, {})
                
    # Extra func for price.
    try:
        price_dict = dict()
        price, price_dict = get_price_from_png(rtn_data["price"], price_dict, project_name)
        
        rtn_data["price"] = price
    
    except Exception:
        pass
    
    # Extra func for payment.
    try:
        payment_rtn_list = list()
        for payment in rtn_data["paymentlist"]:
            payment_rtn = dict()
            for k, v in zip(payment.keys(), payment.values()):
                if k == "period":
                    payment_rtn["period"] = v
                else:
                    payment_rtn[k], price_dict = get_price_from_png(v, price_dict, project_name)
                    
            payment_rtn_list.append(payment_rtn)

            rtn_data["paymentlist"] = payment_rtn_list
    
    except Exception:
        pass

    logger.debug("After Extra =>", data=rtn_data)

    return rtn_data

def get_price_from_png(price_object, price_dict, project_name):
    '''get_price_from_png
    Get price info from png files by using tesseract OCR.
    
    '''
    logger          = LogBase(project_name, "ziroom_ocr")

    try:
        price = StringIO()
        url = "http:{}".format(price_object[0])

        if url in price_dict.keys():
            t = price_dict[url]
        else:
            img_path = "_output/{}".format(findall(r"/([0-9a-zA-z]+.png)", url)[0])
            req = ProxiesRequests([url], project_name)
            ctn = req.req_content_list[0][0]

            with open(img_path, "wb") as img:
                img.write(ctn)

            img         = Image.open(img_path)
            bg          = Image.new("RGBA", img.size, "white")
            merged_pic  = Image.new("RGBA", tuple([int(s*1.2) for s in img.size]), "white")
            mg          = Image.alpha_composite(bg, img)
            
            merged_pic.paste(mg)
            t = image_to_string(merged_pic)
            
        for idx in price_object[2]:
            price.write(t[idx])

        price_dict[url] = t

        logger.debug("OCR price =>", price=price.getvalue(), price_dict=price_dict)

        return price.getvalue(), price_dict

    except Exception as e:
        logger.warn("OCR failed.", err=e)
        return "", price_dict

    finally:
        price.close()