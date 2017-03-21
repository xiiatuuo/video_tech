#!python
import os
import sys
import glob
import json

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "../../speech_recogize"))
reload(sys)
sys.setdefaultencoding('utf-8')


from speech_recognize import  analysis

def do_it(text, mid):
    try:
        result = analysis(text)
        result_dict = json.loads(result)
        if result_dict["ret"] != 0:
            return "can not analysis , with text is ["+text+"]"
    except Exception,data:
        print data
        return str(data)
    keywords = [ i["w"]+":"+i["s"] for i in result_dict["cont"]["keywords"] ]
    cate = [ i["c"]+":"+i["s"] for i in result_dict["cont"]["cate"] ]
    print "RESULT","\t", mid, "\t", ",".join(keywords),"\t",",".join(cate)
    result_list = []
    result_list.append("TEXT:["+text+"]")
    result_list.append("KEYWORDS:[" + ",".join(keywords) +"]")
    result_list.append("CATE:[" + ",".join(cate) +"]")
    res = "\n".join(result_list)
    return res

def load_result(fileno):
    try:
        f = open(fileno)
    except Exception,data:
        return None
    key_list = []
    c = 0
    for line in f:
        if c >= 5:
            break
        c+=1
        key_list.append(line.strip().split(" ")[0])
    return ",".join(key_list)

def main():
    base_dir = sys.argv[1]
    result_dict = {}
    for mid in os.listdir(base_dir):
        result_file = os.path.join(base_dir, mid, "all.txt")
        result_str = load_result(result_file)
        result_dict[mid] = result_str
        res = do_it(result_str, mid)


    #print len(result_dict)

if __name__ == "__main__":
    main()
