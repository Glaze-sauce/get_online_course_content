# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter


class UoocPipeline(object):

    def open_spider(self, spider):
        self.f = open(r"D:\python\reptile\4.数据定位\uooc\Uooc\1.txt", mode="w")

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        data = {}
        data["chapter_name"]=item["chapter_name"]
        data["sub_name"    ]=item["sub_name"    ]
        data["sub_url"     ]=item["sub_url"     ]
        data["caption"     ]=item["caption"     ]
        data["choice"      ]=item["choice"      ]
        self.f.write(str(list(data.values()))+"\r")
        return item