def convert_gbk_to_utf8(input_file, output_file):
    with open(input_file, 'r', encoding='gbk') as f:
        content = f.read()
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":

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
        if i==5:
            continue
        input_file = f"data/{types[i]}/{i}.csv"
        output_file =f"data/{types[i]}/{i}file.csv"
        convert_gbk_to_utf8(input_file, output_file)
        print(types[i], "转换完成")