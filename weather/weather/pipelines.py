# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class WeatherPipeline(object):

    header = '日期 白天 晚上'.split()

    def __init__(self):

        pass

    def process_item(self, item, spider):

        with open('local_weather.txt', 'w+') as f:

            city = item['city'].encode('utf-8')

            f.write('city:' + str(city) + '\n\n')

            date = item['date']

            desc = item['dayDesc']

            dayDesc = desc[1::2]

            nightDesc = desc[0::2]

            dayTemp = item['dayTemp']

            weaitem = zip(date, dayDesc, nightDesc, dayTemp)

            for i in range(len(weaitem)):

                item = weaitem[i]

                d = item[0]

                dd = item[1]

                nd = item[2]

                ta = item[3].split('/')

                #判断以下白天还是晚上，晚上爬的时候当天白天的温度没有数据
                if len(ta) == 1:
                    dt = 'None'
                    nt = ta[0]
                else:
                    dt = ta[0]
                    nt = ta[1]

                txt = 'data:{0}\t\tday:{1}({2})\t\tnight:{3}({4})\n\n'.format(
                        d,
                        dd.encode('utf-8'),
                        dt.encode('utf-8'),
                        nd.encode('utf-8'),
                        nt.encode('utf-8')
                )

                f.write(txt)

        return item
