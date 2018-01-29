# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 上午10:31
# @Author  : Weiting
# @File    : get_train.py
# @Software: PyCharm Community Edition
import json
import requests
import time


def get_train(origin,destination,date):
    with open('stations.json', 'r') as reader:
        station = json.loads(reader.read())
        dict ={}
        origin_id = None
        destination_id =None
        for item in station:
            dict[item['name']] = str(item['id'])
        # print(dict)

        if origin in dict:
            origin_id = dict[origin]


        if destination in dict:
            destination_id = dict[destination]


        if origin_id:
            print(origin_id)
        else:
            return False,"起站不存在"

        if destination_id:
            print(destination_id)
        else:
            return False,"終站不存在"

        # print(date)
        if isVaildDate(date):
            list = date.split("/")
            if len(list)==3:

                year =list[0]
                month = date_text(list[1])
                day = date_text(list[2])


                if month and day:
                    print(year,month,day)
                    return get_train_api(origin_id,destination_id,year,month,day)
            else:
                return False,"請輸入完整正確格式的日期"
        else:
            return False,"日期有誤"






def date_text(value):
    if len(value)==1:
        value = '0'+value
    elif len(value)>3:
        value = None
    return value

def isVaildDate(date):
    try:
        time.strptime(date, "%Y/%m/%d")
        return True
    except:
        return False

def get_train_api(origin_id,destination_id,year,month,day):
    url = "http://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/OD/" + origin_id + "/to/" + destination_id + "/" + year + "-" + month + "-" + day + "?$top=20&$format=JSON"
    session = requests.Session()
    session.headers[
        'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    train_dict = session.get(url).json()
    # print(len(train_dict))

    with open('train_type.json', 'r') as reader:
        trains = json.loads(reader.read())
        dict ={}

        for item in trains:
            dict[item['車種編號']] = item['車種名稱']


    new_train = []

    for train in train_dict:
        train_type_id = train['DailyTrainInfo']['TrainTypeID']

        new_train.append({
            'train_NO': train['DailyTrainInfo']['TrainNo'],
            'train_type':dict[train_type_id],
            'origin_station': train['OriginStopTime']['StationName']['Zh_tw'],
            'origin_departure_time': train['OriginStopTime']['DepartureTime'],
            'destination_station': train['DestinationStopTime']['StationName']['Zh_tw'],
            'destination_arrival_time': train['DestinationStopTime']['ArrivalTime'],
        })
    if len(new_train)==0:
        return False,"沒有此列車"
    else:
        print(new_train)
        newlist = sorted(new_train, key=lambda k: k['origin_departure_time'])
        print(newlist)
        return True,newlist

if __name__ == "__main__":
    train = get_train("台北","台東","2018/1/29")
    # print(train)