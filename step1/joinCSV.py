import pandas as pd
import os

types = {
        1: "公开招标",
        2: "询价公告",
        3: "竞争性谈判",
        4: "单一来源",
        5: "资格预审",
        6: "邀请招标公告",
        7: "中标公告",
        8: "更正公告",
        9: "其他公告",
        10: "竞争性磋商",
        11: "成交公告",
        12: "终止公告"
    }

for i in range(1, 13):
    
    # 读取第一个CSV文件
    file_path1 = os.path.join(os.path.join('data', types[i]), str(i) + 'filenew.csv')
    df1 = pd.read_csv(file_path1)

    # 读取第二个CSV文件，跳过表头
    file_path2 = os.path.join(os.path.join('data', types[i]), str(i) + 'file.csv')
    df2 = pd.read_csv(file_path2)

    # 获取第一个表的最大序号
    max_seq = df1['序号'].max()
    print(f"第一个表的最大序号为: {max_seq}")

    # 更新第二个表的序号，使其从max_seq + 1开始
    if '序号' in df2.columns:
        df2['序号'] = df2['序号'] + max_seq
    else:
        print(f"第二个表中没有 '序号' 列，跳过序号更新")

    # 合并两个表格
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # 保存合并后的表格到新的CSV文件
    combined_df.to_csv(os.path.join(os.path.join('data', types[i]), str(i) + '.csv'), index=False, encoding='utf-8')

    print(f"合并完成，已保存为 '{i}.csv'")
