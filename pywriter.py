#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from random import choice
import time
import jieba
import jieba.posseg as pseg


prompt = '>'

print '请输入语料库文件名（包括后缀比如.txt）'
library = raw_input(prompt)
print '请输入模板文件名（包括后缀比如.txt）'
model = raw_input(prompt)
print '想要 Python 为你写几首/篇呢？请输入阿拉伯数字'
times = input(prompt)
print '如果语料库内容很多，请输入yes;内容不多直接回车'
unique = raw_input(prompt)
print '需要将 Python 写出的内容保存吗？\n需要保存输入保存文件名（包括后缀，建议.txt），不需要直接回车'
save_file = raw_input(prompt)

dict = {}
m_processed = ''
old = []
dict['x'] = ['\n']
record_time = True
record_time_file = True
ISOTIMEFORMAT = '%Y-%m-%d %X'


# 将语料库分词并按词性归入不同的数组，词性和数组构成字典的键值对
with open(library, 'rb') as l:
    prel_text = l.read()
    # 防止 library 没有 model 的内容，先把 m 内容加到 l 里，以防 l 的词性不足以覆盖 m 包含的词
    with open(model, 'rb') as m:
        m_text = m.read()
    l_text = prel_text + m_text

    # 词性作为字典的 key，其 value 是数组，为具有此词性的分词
    words = pseg.cut(l_text)
    for word, flag in words:
        if flag == 'x':
            continue
        if not flag in dict:
            dict[flag] = []
            dict[flag].append(word)
            continue
        # 保证 value 里的值是惟一的
        if not word in dict[flag]: 
            dict[flag].append(word)

# 将模型所有分词后对应的词性计入字符串，再变成数组
m_words = pseg.cut(m_text)
for word, flag in m_words:
    m_processed += flag + ' '

mdl = m_processed.rstrip().split(' ')


for count in range(times):
    pywriter = ''
    for i in mdl:
        all = dict[i]
        # 从语料库中同一词性的词随机选一个填进来
        i_text = choice(all)
        # 如果语料库多选择填词时不重复用词
        if unique == 'yes':
            if (i != 'x') and (i != 'xx'):
                if not i_text in old:
                    pywriter += i_text
                    old.append(i_text)
            else:
                pywriter += i_text
        else:
            pywriter += i_text

    localtime = '\n\n'  + '''* =========================
* 时间: ''' + time.strftime(ISOTIMEFORMAT, time.localtime(time.time())) + '''
* 语料库文件名: ''' + library + '''
* 模板文件名: ''' + model + '''
* 本次共 ''' + str(times) + ''' 首/篇
* ========================= ''' + '\n\n' 
    separator = '-----------  No.' + str(count+1) + '  -----------' + '\n\n' 
    result = separator + pywriter + '\n\n'
    
    if record_time:
        # record_time 和下面的 record_time_file 保证写一次只记一次
        record_time = False
        print localtime
    print result

    # 指定了保存文件名则保存，不论保不保存在上面都会在终端输出结果
    if save_file:        
        with open(save_file, 'a') as sf:
            if record_time_file:
                record_time_file = False
                sf.write(localtime)
            sf.write(result.encode('utf-8'))





