#!/bin/sh
cd /root/duqianjin/videocrawl
rm /root/duqianjin/code_file/result.csv
scrapy crawl videoyright -a start_url="http://v.youku.com/v_show/id_XMTYyMzYzNTM3Ng==.html?from=y1.6-85.3.1.514156d28e9711e5b2ad" -o /root/duqianjin/code_file/result.csv
scrapy crawl videoyright -a start_url="http://v.youku.com/v_show/id_XMTc2MzgzMjc4MA==.html?spm=a2h0j.8191423.item_XMTc2MzgzMjc4MA==.A&from=y1.2-2.4.1-1" -o /root/duqianjin/code_file/result.csv
sleep 30
#非凡娱乐
scrapy crawl video -a start_url="http://i.youku.com/i/UMjAwOTkwOTM2/videos"  -o /root/duqianjin/code_file/result.csv
sleep 30
#德云社
scrapy crawl videoyright -a start_url="http://v.youku.com/v_show/id_XNzg4Mjg0MTc2.html?spm=a2h0j.8191423.item_XNzg4Mjg0MTc2.A" -o /root/duqianjin/code_file/result.csv
scrapy crawl videoyright -a start_url="http://v.youku.com/v_show/id_XMTM0MTI0ODk1Mg==.html?spm=a2h0j.8191423.item_XMTM0MTI0ODk1Mg==.A&from=y1.2-2.4.1-1" -o /root/duqianjin/code_file/result.csv
scrapy crawl videoyright -a start_url="http://v.youku.com/v_show/id_XMTc1OTE4ODI5Ng==.html?from=y1.6-85.3.1.a71f506c904e11e6b16e" -o /root/duqianjin/code_file/result.csv
scrapy crawl videoyright -a start_url="http://v.youku.com/v_show/id_XMTcwODc1MTc2MA==.html?from=y1.6-85.3.1.ac6a0fd76ddc11e6b9bb" -o /root/duqianjin/code_file/result.csv
sleep 30
#央视春晚相声
scrapy crawl videoaright -a start_url="http://www.iqiyi.com/playlist300755002.html#vfrm=2-3-0-1" -o /root/duqianjin/code_file/result.csv
#爱奇艺-曲艺杂坛·相声小品
scrapy crawl videoaright -a start_url="http://www.iqiyi.com/playlist251961502.html#vfrm=2-3-0-1" -o /root/duqianjin/code_file/result.csv
#优酷-1TheK
scrapy crawl video -a start_url="http://i.youku.com/i/UMTI4MzI5MjExMg==/videos" -o /root/duqianjin/code_file/result.csv
#百度EXO
scrapy crawl video -a start_url="http://i.youku.com/i/UNTI4OTMwMTQ0/videos" -o /root/duqianjin/code_file/result.csv
sleep 30
#搜酷-剧能扯 放胆喷 2016 
scrapy crawl video -a start_url="http://i.youku.com/i/UMTQwOTE1ODI1Mg==/videos" -o /root/duqianjin/code_file/result.csv
sleep 30
#优酷-电影公嗨课
scrapy crawl video -a start_url="http://i.youku.com/i/UNjAwNzYwODI4/videos" -o /root/duqianjin/code_file/result.csv
sleep 30
#优酷搜-开心萌宠编辑部
scrapy crawl video -a start_url="http://i.youku.com/i/UMzIwOTExODcwNA==/videos" -o /root/duqianjin/code_file/result.csv
#优酷搜-萌宠视频
scrapy crawl video -a start_url="http://i.youku.com/i/UMTA2MzcwNDI4/videos" -o /root/duqianjin/code_file/result.csv
sleep 30
#优酷搜-萌宠视频
scrapy crawl video -a start_url="http://i.youku.com/i/UMjg3Njc0ODc1Mg==/videos" -o /root/duqianjin/code_file/result.csv
#优酷搜-敬汉卿-自频道
scrapy crawl video -a start_url="http://i.youku.com/i/UMTIwODUyMDM1Ng==/videos" -o /root/duqianjin/code_file/result.csv
sleep 30
#在优酷片库-搞笑
scrapy crawl videoygbelow -a start_url="http://list.youku.com/category/video/c_94_g_235_d_1_s_1_p_2.html"   -o /root/duqianjin/code_file/result.csv
#优酷搜-美妆师vv
scrapy crawl video -a start_url="http://i.youku.com/i/UMzMyMTIxODAxMg==/videos"  -o /root/duqianjin/code_file/result.csv
#优酷搜-抹茶美妆
scrapy crawl video -a start_url="http://i.youku.com/i/UMTU2NDgxNTEyOA==/videos"  -o /root/duqianjin/code_file/result.csv
sleep 30
#搜狐搜爱范儿视频
scrapy crawl videosohu -a start_url="http://my.tv.sohu.com/user/media/video.do?uid=232799889&page=1&sortType=2" -o /root/duqianjin/code_file/result.csvi
#今日头条搜娱乐、优酷-大嘴八号店
scrapy crawl video -a start_url="http://i.youku.com/i/UMzE3ODIzMTY2MA==/videos"  -o /root/duqianjin/code_file/result.csv
#优酷-口述历史频道（崔永元）
scrapy crawl video -a start_url="http://i.youku.com/i/UMzE3OTkxNDk4OA==/videos"  -o /root/duqianjin/code_file/result.csv
#搜狐搜幻想曲资讯
scrapy crawl video -a start_url="http://i.youku.com/i/UOTM3MTk0NA==/videos"  -o /root/duqianjin/code_file/result.csv
sleeo 30
#优酷搜-美芽美妆
scrapy crawl video -a start_url="http://i.youku.com/i/UMTY2MjU3NDU2NA==/videos"  -o /root/duqianjin/code_file/result.csv
#搜狐搜ZEALERChina
scrapy crawl videosohu -a start_url="http://my.tv.sohu.com/user/media/video.do?uid=175880212&page=1&sortType=2" -o /root/duqianjin/code_file/result.csv
#爱奇艺-何仙姑夫工作室 
scrapy crawl videoahe -a start_url="http://www.iqiyi.com/u/416391545/v"  -o /root/duqianjin/code_file/result.csv
#搜酷-剧刀叨
scrapy crawl video -a start_url="http://i.youku.com/i/UMzAwMzI5OTQxMg==/videos"  -o /root/duqianjin/code_file/result.csv
#优酷-萝卜报告
scrapy crawl video -a start_url="http://i.youku.com/i/UMTcwODYxMDY1Mg==/videos"  -o /root/duqianjin/code_file/result.csv
sleep 30
#优酷-晓敏AUTO秀
scrapy crawl video -a start_url="http://i.youku.com/u/UMTYwNTMwNzc3Mg==/videos"  -o /root/duqianjin/code_file/result.csv
#优酷搜-萌星人de那些破事
scrapy crawl video -a start_url="http://i.youku.com/i/UMzE2MDk3OTY5Mg==/videos"  -o /root/duqianjin/code_file/result.csv
#腾讯视频搜-喵星人的那些小破事儿
scrapy crawl videotenxun -a start_url="http://v.qq.com/x/cover/u3z9dt8bfxcgrr6/b0019biei32.html" -o /root/duqianjin/code_file/result.csv
#爱奇艺-泡菜帮
scrapy crawl videoabelow -a start_url="http://www.iqiyi.com/a_19rrgi9w1l.html#vfrm=2-3-0-1" -o /root/duqianjin/code_file/result.csv
#爱奇艺-综艺麻辣烫
scrapy crawl videoabelow -a start_url="http://www.iqiyi.com/a_19rrhae991.html#vfrm=2-3-0-1" -o /root/duqianjin/code_file/result.csv
#优酷-播单:【日综】【宠物当家】【中文字幕】
scrapy crawl videoymeng -a start_url="http://list.youku.com/albumlist/show?id=3076330&ascending=1&page=1" -o /root/duqianjin/code_file/result.csv
#优酷搜-美国国家地理频道
scrapy crawl video -a start_url="http://i.youku.com/i/UMzIwMzgxMzc2/videos" -o /root/duqianjin/code_file/result.csv
#今日头条搜育儿、优酷-母婴生活小百科
scrapy crawl video -a start_url="http://i.youku.com/i/UMjg2OTI4ODAzMg==/videos"  -o /root/duqianjin/code_file/result.csv
sleep 30
#今日头条搜育儿、优酷-母婴健康知识
scrapy crawl video -a start_url="http://i.youku.com/i/UMjg2OTM0OTAwNA==/videos" -o /root/duqianjin/code_file/result.csv
#今日头条搜育儿、优酷-母婴知识手册
scrapy crawl video -a start_url="http://i.youku.com/i/UMjg2OTM2OTQ4MA==/videos" -o /root/duqianjin/code_file/result.csv
#今日头条搜育儿、优酷-亲子育儿讲堂
scrapy crawl video -a start_url="http://i.youku.com/i/UMjg2OTM5MzM4MA==/videos" -o /root/duqianjin/code_file/result.csv
#腾讯-育儿奥秘
scrapy crawl videotenxunr -a start_url="http://v.qq.com/x/cover/8d2dzz0lke8sxo0/b0014x4fdwe.html"  -o /root/duqianjin/code_file/result.csv
