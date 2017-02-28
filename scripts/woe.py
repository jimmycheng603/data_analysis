# -*- coding: utf-8 -*-

__author__ = 'chengjunjie'

from sys import argv

import math
import pandas as pd

if __name__ == '__main__':
    """
        inputfile:dataframe所在输入文件
        feture:需要分析的特征变量
        sep 分段表达式
        target y变量
        """
    inputfile = argv[1]
    feature = argv[2]
    sep = argv[3]
    target = argv[4]

    data = pd.read_csv(inputfile, sep=',')
    # woe
    sep_value = sep.split(',')
    sep_len = len(sep_value)
    dict_bin = {}
    class_bin = {}
    len_dict_bin = {}
    len_dict_bin_0 = {}
    len_dict_bin_1 = {}
    woe_bin = {}
    iv_bin = {}
    if sep_len == 1:
        dict_bin[0] = data.loc[data[feature] <= float(sep_value[0]), :]
        dict_bin[1] = data.loc[data[feature] > float(sep_value[0]), :]
        dict_bin[2] = sum(data[feature].isnull())
        len_dict_bin[0] = len(dict_bin[0])
        len_dict_bin[1] = len(dict_bin[1])
        len_dict_bin[2] = len(dict_bin[2])
        class_bin[0] = "(0," + sep_value[0] + "]"
        class_bin[1] = "(" + sep_value[0] + "...)"
        class_bin[2] = "NA"
    else:
        for index, item in enumerate(sep_value):
            if index == 0:
                dict_bin[0] = data.loc[data[feature] <= float(item), :]
                len_dict_bin[0] = len(dict_bin[0])
                class_bin[0] = "(0," + str(float(item)) + "]"
            else:
                dict_bin[index] = (
                    data.loc[(data[feature] >= float(sep_value[index - 1])) & (data[feature] < float(item)),
                    :])
                len_dict_bin[index] = len(dict_bin[index])
                class_bin[index] = "(" + str(sep_value[index - 1]) + "," + str(sep_value[index]) + "]"
        dict_bin[index + 1] = data.loc[data[feature] > float(item), :]
        dict_bin[index + 2] = data.loc[data[feature].isnull()]
        len_dict_bin[index + 1] = len(dict_bin[index + 1])
        len_dict_bin[index + 2] = len(dict_bin[index + 2])
        class_bin[index + 1] = "(" + str(sep_value[index]) + "...)"
        class_bin[index + 2] = "NA"

    for index, item in enumerate(dict_bin):
        len_dict_bin_0[index] = len(dict_bin[index][dict_bin[index][target] == 0])
        len_dict_bin_1[index] = len(dict_bin[index][dict_bin[index][target] == 1])

    len_data_0 = len(data[data[target] == 0])
    len_data_1 = len(data[data[target] == 1])
    for index, item in enumerate(dict_bin):
        try:
            woe_bin[index] = math.log(math.e, (float(len_dict_bin_1[index]) / float(len_data_1)) / (
                float(len_dict_bin_0[index]) / float(len_data_0)))
            iv_bin[index] = ((float(len_dict_bin_1[index]) / float(len_data_1)) - (
                float(len_dict_bin_0[index]) / float(len_data_0))) * math.log(math.e, (
                float(len_dict_bin_1[index]) / float(len_data_1)) / (
                                                                                  float(len_dict_bin_0[index]) / float(
                                                                                      len_data_0)))
        except Exception, e:
            iv_bin[index] = 0

    dict_result = {}
    len_dict_bin_0[" "] = len_data_0
    len_dict_bin_1[" "] = len_data_1
    woe_bin[" "] = ""
    iv_bin[" "]=sum(iv_bin.values())
    class_bin[" "] = ""
    len_dict_bin[" "] = len(data)
    dict_result["bad"] = len_dict_bin_0
    dict_result["good"] = len_dict_bin_1
    dict_result["all"] = len_dict_bin
    dict_result["woe"] = woe_bin
    dict_result["iv"] = iv_bin
    dict_result["class"] = class_bin
    df = pd.DataFrame(dict_result)

    dict_result["%good"] = (df['good'] / df['all']).map('{:.2%}'.format);
    dict_result["%bad"] = (df['bad'] / df['all']).map('{:.2%}'.format);
    df["%good"] = dict_result["%good"]
    df["%bad"] = dict_result["%bad"]

    # 调整列的顺序
    df = df.ix[:, ['class', 'good', 'bad', '%good', '%bad', 'all', 'woe', 'iv']]
    print df
