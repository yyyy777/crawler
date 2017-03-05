# coding=utf-8

"""命令行火车票查看工具

Usage:
    tickets [-gdtkz] <from> <to> <date>

options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 重庆 2017-03-26
    tickets -dg 成都 重庆 2017-03-26

"""
import requests

from docopt import docopt

from prettytable import PrettyTable

from stations import stations

#因为是https，会有警告，所以加入以下参数解决警告问题
from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

class TrainsResult:

    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):

        self.available_trains = available_trains

        self.options = options

    def _get_duration(self, raw_train):

        duration = raw_train.get('lishi').replace(':', '小时') + '分'

        if duration.startswith('00'):
            return duration[4:]

        if duration.startswith('0'):
            return duration[1:]

        return duration

    @property
    def trains(self):

        for raw_train in self.available_trains:

            raw_train = raw_train['queryLeftNewDTO']

            train_code = raw_train['station_train_code']

            initial = train_code[0].lower()

            if not self.options or initial in self.options:

                train = [
                    train_code,

                    '\n'.join([raw_train['from_station_name'],
                              raw_train['to_station_name']]),

                    '\n'.join([raw_train['start_time'],
                             raw_train['arrive_time']]),

                    self._get_duration(raw_train),

                    raw_train['zy_num'],
                    raw_train['ze_num'],
                    raw_train['rw_num'],
                    raw_train['yw_num'],
                    raw_train['yz_num'],
                    raw_train['wz_num']
                ]

                yield train

    def pretty_print(self):

        pt = PrettyTable()

        pt._set_field_names(self.header)

        for train in self.trains:
            pt.add_row(train)

        print(pt)

def command():

    arguments = docopt(__doc__)

    #print(arguments)

    from_sta = stations.get(arguments['<from>'])

    to_sta = stations.get(arguments['<to>'])

    date = arguments['<date>']

    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_sta, to_sta)

    resp = requests.get(url, verify=False)

    #print(resp.json())

    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])

    available_trains = resp.json()['data']

    TrainsResult(available_trains, options).pretty_print()

if __name__ == '__main__':

    command()
