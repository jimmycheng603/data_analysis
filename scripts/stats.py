from sys import argv

import pandas as pd


if __name__ == '__main__':
    inputfile = argv[1]
    feature = argv[2]
    outputfile = argv[3]
    data = pd.read_csv(inputfile, sep=',')

    # cnt_rec
    counts_feature = data.groupby(feature).size().rename("cnt_rec")
    df_counts_feature = pd.DataFrame(counts_feature);

    # target
    feature_target = data.loc[data['is_dft'] == 1, :]
    df_feature_target = pd.DataFrame(feature_target.groupby(feature).size().rename("cnt_target"));

    # concat
    df_result = pd.concat([df_counts_feature, df_feature_target], axis=1);

    # cnt_target/cnt_rec
    df_result['%target'] = (df_result['cnt_target'] / df_result['cnt_rec']).map('{:.2%}'.format);

    cnt_rec = df_result['cnt_rec'] / df_result['cnt_rec'].sum()
    # cnt_rec/sum(cnt_rec)
    df_result['%cnt_rec'] = cnt_rec.map('{:.2%}'.format);

    cnt_target = df_result['cnt_target'] / df_result['cnt_target'].sum()
    # cnt_target/sum(cnt_target)
    df_result['%cnt_target'] = cnt_target.map('{:.2%}'.format);

    # %cum_cnt_rec
    df_result['%cum_cnt_rec'] = (cnt_rec.cumsum()).map('{:.2%}'.format);

    # %cum_cnt_target
    df_result['%cum_cnt_target'] = cnt_target.cumsum().map(
        '{:.2%}'.format);

    # cnt_nontarget
    df_result['cnt_nontarget'] = df_result['cnt_rec'] - df_result['cnt_target'];

    cnt_nontarget = df_result['cnt_nontarget'] / df_result['cnt_nontarget'].sum()
    # %cnt_nontarget
    df_result['%cnt_nontarget'] = cnt_nontarget.map('{:.2%}'.format);

    # %cum_nontarget
    df_result['%cum_nontarget'] = cnt_nontarget.cumsum().map(
        '{:.2%}'.format);

    # % cum_target - % cum_nontarget
    df_result['%cum_target-%cum_nontarget'] = (cnt_target
                                               - cnt_nontarget).map(
        '{:.2%}'.format)

    df_result.to_csv(outputfile, encoding='gb2312')
