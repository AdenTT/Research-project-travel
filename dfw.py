import requests
import time
import urllib.parse
import json
import pymysql


class ShangHaiLand():
    def __init__(self): 
        self.db = pymysql.connect(host='119.23.39.100', user='root', password='123456',  # 连接数据库（地址，用户名，密码，端口，数据库名）
                                  port=3306, db='TMS')

        self.cursor = self.db.cursor()


    def get_mes(self):
        '''获取信息的方法'''

        while True:  
            try:
               

                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October',
                          'November',
                          'December']  
                list = [{'上海博物馆': 'json_2_18'}, {'上海野生动物园': 'json_1_2'}, {'东方明珠广播电视塔': 'json_1_3'},
                        {'上海科技馆': 'json_1_4'},
                        {'上海海洋水族馆': 'json_1_7'}, {'上海世纪公园': 'json_1_6'}, {'上海鲜花港': 'json_1_8'}]  
                timestamp = int(time.time() * 1000)  

                month = time.strftime("%m", time.localtime(time.time()))  
                e_month = month.replace('01', months[0]).replace('02', months[1]).replace('03', months[2]).replace('04',
                                                                                                                   months[
                                                                                                                       3]).replace(
                    '05', months[4]).replace('06', months[5]).replace('07', months[6]).replace('08', months[7]).replace(
                    '09',
                    months[
                        8]).replace(
                    '10', months[9]).replace('11', months[10]).replace('12', months[11])  
                formatTime = time.strftime(" %d %Y %H:%M:%S", time.localtime(time.time()))  
                update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                item = {
                    't': timestamp,
                    'noCache': 'thu ' + e_month + formatTime + ' GMT+0800 (中国标准时间)', 
                }

                urllib_mes = urllib.parse.urlencode(item)
                print(timestamp) 
                com_url = 'http://lysh.eastday.com/lyj/WebApiService/api/GetSpots' + '?' + urllib_mes   
                print(com_url)
                res = requests.get(com_url)
                if res.text.startswith(u'\ufeff'):     
                    text = res.text.encode('utf8')[3:].decode('utf8')
                else:
                    print('null')
                    text = ''
                message = json.loads(text, encoding='utf8')

                sahnghai_museum = message.get('json_2_18')[0].get('num')  
                Shanghai_wildlife_park = message.get('json_1_2')[0].get('num')
                oriental_pearl_TV_tower = message.get('json_1_3')[0].get('num')
                shanghai_science_and_technology_museum = message.get('json_1_4')[0].get('num')
                shanghai_ocean_aquarium = message.get('json_1_7')[0].get('num')
                shanghai_century_park = message.get('json_1_6')[0].get('num')
                shanghai_flower_port = message.get('json_1_8')[0].get('num')

                item = {
                    '上海博物馆': [sahnghai_museum, 'L201900001'],
                    '上海野生动物园': [Shanghai_wildlife_park, 'L201900002'],
                    '东方明珠广播电视塔': [oriental_pearl_TV_tower, 'L201900003'],
                    '上海科技馆': [shanghai_science_and_technology_museum, 'L201900004'],
                    '上海海洋水族馆': [shanghai_ocean_aquarium, 'L201900005'],
                    '上海世纪公园': [shanghai_century_park, 'L201900006'],
                    '上海鲜花港': [shanghai_flower_port, 'L201900007']
                }
                print(item)
                print(update_time)
                self.update_mysql(item)
                break
            except:
                print('request failed')
                time.sleep(1)


    def update_mysql(self, item):
        try:
            self.db.ping(reconnect=True)   
        except:
            pass
        for one in item.items():
            up_sql = """update TMS_LAND set custFlow='%s' where landID='%s'""" % (
                one[1][0], one[1][1])
            try:
                self.cursor.execute(up_sql)
                self.db.commit()
                print('Update Success')
            except Exception as e:
                print(e)

    def run(self):
        while True:
            self.get_mes()
            print('Wait for 15 min')
            time.sleep(900)    

a = ShangHaiLand()  
a.run()    
