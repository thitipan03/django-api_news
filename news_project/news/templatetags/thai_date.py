from django import template
from datetime import datetime
import pytz

register = template.Library()

def getdate(date):
        thai_tz = pytz.timezone('Asia/Bangkok')
        if isinstance(date, datetime):
                date = date.astimezone(thai_tz)  
        else:
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc).astimezone(thai_tz)
        day = date.day
        year = date.year
        hour = date.strftime('%H') 
        minute = date.strftime('%M') 
        second = date.strftime('%S') 
        thai_month_dict = {
        1:"มกราคม",
        2:"กุมภาพันธ์",
        3:"มีนาคม",
        4:"เมษายน",
        5:"พฤษภาคม",
        6:"มิถุนายน",
        7:"กรกฎาคม",
        8:"สิงหาคม",
        9:"กันยายน",
        10:"ตุลาคม",
        11:"พฤศจิกายน",
        12:"ธันวาคม",}
        get_month = thai_month_dict[date.month]
        return f'{day} {get_month} {year} เวลา {hour}:{minute}:{second} น.'

@register.filter
def thai_date(value):
    return getdate(value)