
import requests
import re
import time
from node_vm2 import NodeVM



def get_vf(url):
    print('vfurl:',url)
    with open('295_decrypt.js', 'r', encoding='utf-8') as f:
        js = f.read()
    module = NodeVM.code(js)
    vf = module.call_member('cmd5x', url)
    return f'{url}&vf={vf}'

title = ''


# 获取链接中内容，因不好转换，写的比较复杂
def getm3u8(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75',
        'cookie': Cookie
    }
    try:
        response = requests.get(url=url, headers=headers).text
        m3u8 = re.findall('"m3u8":"(.+?)"', response)[0].replace('/', '').replace('\\', '/')
        m3u8s = m3u8.split('/n')
        m3u8 = '\n'.join(m3u8s)
        global title
        vsizes = re.findall('"vsize":(\d+)', response)
        vs = []
        for vsize in vsizes:
            vs.append(int(int(vsize) / 1024 / 1024))
        vssize = str(max(vs)) + 'MB'
        scrsz = re.findall('"scrsz":"(.+?)"', response)[0]
        ####
        title = title + '_' + scrsz + '_' + vssize
        print(title)
        with open(f'{title}.m3u8', 'w', encoding='utf-8') as f:
            f.write(m3u8)
    except:
        print('不支持此链接！')


def parse(shareurl):
    response = requests.get(url=shareurl).text
    try:
        global title
        title = re.findall('<meta  name="irTitle" content="(.+?)" />', response)[0]
    except:
        title = ''

    tvid = re.findall('"tvId":(\d+)', response)[0]

    vid = re.findall('"vid":"(.+?)"', response)[0]
    print()
    tm = int(time.time() * 1000)
    # k_ft2 = 8191
    url_with_dash_but_vf2 = f'/jp/dash?tvid={tvid}&bid=860&vid={vid}&src=03020031010000000000&vt=0&rs=1&uid={Cookie_P00003}&ori=pcw&ps=0&k_uid={Cookie_QC005}&pt=0&d=0&s=&lid=&cf=&ct=&k_tag=1&ost=0&ppt=0&dfp={Cookie_dfp}&locale=zh_cn&k_err_retries=0&qd_v=2&tm={tm}&qdy=a&qds=0&k_ft2=8191&callback=Nchujx&ut=1'
    vf = get_vf(url_with_dash_but_vf2)

    infourl = 'https://cache.video.iqiyi.com' + vf
    print(infourl)

    getm3u8(infourl)


if __name__ == '__main__':
    print('爱奇艺视频解析')
    # Cookie 只填P00001 即可
    # Cookie = 'P00001=dbDGm3tbOctQELNen4XiwyzaLzc3Sm1AaLjdhrwm24bgKivBbMNXyv0YLxOSkdKlwEPUl2d'
    Cookie = 'P00001=dbDGm3tbOctQELNen4XiwyzaLzc3Sm1AaLjdhrwm24bgKivBbMNXyv0YLxOSkdKlwEPUl2d'
    Cookie_P00003 = ''
    Cookie_QC005 = ''
    Cookie_dfp = ''
    while True:
        shareurl = input('输入爱奇艺视频网址：')
        parse(shareurl)
