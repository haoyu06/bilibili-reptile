import re
import json
import time
import requests
import schedule
import download_main
from lxml import etree

print("新型网络松鼠的自动化收割机启动，收割时间间隔为5s")
def Automatic_harvester():
    import json

    # 读取json文件
    with open('data_mid.json') as f:
        data1 = json.load(f)
    with open('data_lst_id.json') as f:
        data2 = json.load(f)
    # 遍历每个uid和mid，拼接API URL并添加到urls数组中
    urls = []
    # 用户的mid调用api：：https://api.bilibili.com/x/space/wbi/arc/search?mid=1563751305&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=44eb867d57fdaa28154beb09954311ce&wts=1698298141
    # for mid in data1:
    #     url = "https://api.bilibili.com/x/space/wbi/arc/search?mid=" + mid + "&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=44eb867d57fdaa28154beb09954311ce&wts=1698298141"
    #     urls.append(url)

    # 收藏夹的fid调用api：：https://api.bilibili.com/x/v3/fav/resource/list?media_id=2542724062&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web
    for fid in data2:
        url = "https://api.bilibili.com/x/v3/fav/resource/list?media_id=" + fid + "&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web"
        urls.append(url)

    headers_ = {
        'Cookie': '''按f12进入开发者模式后网络中web开头的文件下有cookie，替换这行文字，放在两端的三个点中间''',
        'Referer': 'https://search.bilibili.com/',
        'User-Agent': '按f12进入开发者模式后网络中web开头的文件下有User-Agent，替换这行文字，放在两端的三个点中间',
    }

    # 建立一个全局列表
    global_differ = []
    global_old_list = []
    with open('data_histo.json', 'r') as f:
        data5 = json.load(f)
    global_old_list += data5

    for url2 in urls:
        response_ = requests.get(url2, headers=headers_)
        print(url2)
        text = response_.text
        pattern = r'"bvid":"(.+?)"'
        bvid_match_data = re.findall(pattern, text)
        print("抓取到的松果位置：" + ", ".join(bvid_match_data))

        # # 与下载历史记录作比较
        with open('data_histo.json', 'r') as f:
            data1 = json.load(f)
            print("已采集过的松果位置：" + ", ".join(data1))

        # 比较两组数据，输出不同的数据
        diff = list(set(bvid_match_data) - set(data1))
        print("新松果位置" + ", ".join(diff))
        global_differ += diff

    global_old_list += global_differ

    # 传递给download_main来下载
    for bvid in global_differ:
        url_ = 'https://www.bilibili.com/video/' + bvid + '/?spm_id_from=333.999.0.0&vd_source=9c14dbce18e4fe2de7a5bb9fef5e8422'
        result = download_main.down_func(url_)

###如果收藏夹删除了以前视频，data_histo不会缺失数据
    with open('data_histo.json', 'w') as f:
        json.dump(global_old_list, f)
        print("采集过的松果位置列表已更新")
        print("任务完成，自动化收割机已休眠，5s后进行下一次采集")

if __name__ == '__main__':
    # 设置定时任务，每隔 5 秒钟执行一次 Automatic_harvester 函数，需要的可以设为3600秒（一小时运行一次）
    schedule.every(5).seconds.do(Automatic_harvester)


    # 循环执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)
