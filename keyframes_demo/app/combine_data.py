#!python
#coding=utf-8
import sys

def parse_result(filename, mid_info_dict):
    f = open(filename)
    for line in f:
        if line.find("RESULT") == -1:
            continue
        info_list = line.strip().split("\t")
        '''
        try:
            n = int(info_list[1])
        except Exception,data:
            continue
        #mid = int(info_list[1])
        '''
        mid = info_list[1].strip()

        if len(info_list) <= 3:
            if mid in mid_info_dict:
                mid_info_dict[mid]["text"] = "\t".join(info_list[2:])
            else:
                mid_info_dict[mid] = {}
                mid_info_dict[mid]["text"] = "\t".join(info_list[2:])
        else:
            if mid in mid_info_dict:
                mid_info_dict[mid]["result"] = "\t".join(info_list[2:])
            else:
                mid_info_dict[mid] = {}
                mid_info_dict[mid]["result"] = "\t".join(info_list[2:])




def get_mids(filename):
    mid_list = []
    f = open(filename)
    for line in f:
        #mid_list.append(int(line.strip()))
        mid_list.append(line.strip())
    return mid_list

def main():
    mid_info_dict = {}
    mid_list = get_mids(sys.argv[1])
    for f in sys.argv[2:]:
        parse_result(f, mid_info_dict)
    for mid in mid_list:
        if mid in mid_info_dict:
            result = mid_info_dict[mid].get("result", "")
            text = mid_info_dict[mid].get("text", "")
            print mid,"\t", result,"\t", text
        else:
            print mid,"\t\t"
            #print "EMPTY\t",mid


if __name__ == "__main__":
    main()
