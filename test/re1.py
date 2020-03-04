import re

with open('re.txt','r+',encoding='UTF-8') as f:

    datas = f.read()
    pattern_id = re.compile('\d{1,2}. ')
    pattern_name = re.compile("[\u4E00-\u9FA5]+")
    pattern_tem = re.compile('\d{2}\.\d{1}')
    ids = re.findall(pattern_id,datas)
    names = re.findall(pattern_name,datas)
    temperature = re.findall(pattern_tem,datas)
    print(ids)
    print(len(ids))
    print(len(names))
    print(names)
    print(len(temperature))

    p1 = re.compile('(\d{1,2})(.+)(\d{2}\.\d{1})')
    p1.search(datas).group(1)
    p1.search(datas).group(2)
    p1.search(datas).group(3)



