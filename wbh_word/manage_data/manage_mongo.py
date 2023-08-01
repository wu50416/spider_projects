import time

from pymongo import MongoClient


def connect_mongodb():
    handler = MongoClient("192.168.1.1", 38017).anhua
    return handler


def save_mongodb_data(table,data):
    '''
    save_mongodb_data("wbh_FP_data", {'商品id':id,"qwer": html_data})
    '''
    client = connect_mongodb()
    collection = client[table]
    collection.insert_one(data)


def Update_mongodb_data(table,where_dict,updata_dict):
    '''
    table = "wbh_ZGPMXH_details"
    where_dict = {'id':'68707','meetId':'12070'}
    updata_dict = {'city_Name': '123123abc','asdasd': '123123abc'}
    '''
    client = connect_mongodb()
    collection = client[table]
    # data = "{'id': '925887','meetId':'117752'},{'city_Name': 'abc'}"
    # collection.update_one(filter={'id':'68707','meetId':'12070'},update={"$set": {'city_Name': '123123abc',}})
    collection.update_one(filter=where_dict, update={"$set": updata_dict})


def read_mongodb_data(table):
    '''
    查询全部数据
    '''
    client = connect_mongodb()
    collection = client[table]
    results = collection.find()
    # {'id': '283558441', 'title': '【服装百货】零售价338元派克乔特笔套系列一个', 'city_Name': '深圳市', 'searchLabel_Name': '商业资产', 'searchCategory_Name': '库存物资', 'down_time': '2022-11-18', 'update_time': '2022-11-18'}
    # for res in results:
    #     print(res)
    return results


#   多条件查询.默认为 与 ,同单条件查询通用
def read_more_where_data(table,where_dict,Type='and'):
    '''
    Type :  and / or
    where_dict : [{"status_Update": 0}, {"status_analysis": 0}]
    results = db.getCollection("wbh_JD_details_new_copy1").find({$and:[{"status_Update":0},{"status_analysis":0}]})
    '''
    client = connect_mongodb()
    collection = client[table]
    #         collection.find({"$and":[{"status_Update":0},{"status_analysis":0}]})
    results = collection.find({f"${Type}":where_dict})
    for i in results:
        print("i: ",i)
    return results


# 单条件范围查询   $lt（小于）， $gt（大于）， $lte（小于等于）， $gte（大于等于）， $ne（不等于）
def read_one_where_data(table,find_data):
    '''
    输入find内的参数
    find_data = {"status_analysis":{"$ne":0}}
    results = collection.find({"status_analysis":{"$ne":0}})
    '''
    client = connect_mongodb()
    collection = client[table]
    # find_data
    # $lt（小于）， $gt（大于）， $lte（小于等于）， $gte（大于等于）， $ne（不等于）， {'item_id':item_id}（等于）
    results = collection.find(find_data)
    return results


# 批量单字段数据对比，
def contrast_mongo_data(table,contrast_field,data_list):
    '''
    传入主体数据库name，待对比字段名，对比数据列表
    contrast_field = ItemID
    data_list = ['688110777781', '688785670654', '689122403025']
    $exists = True 存在则返回
    results = collection.find({"ItemID": {"$in": data_list, "$exists": True}})
    '''
    client = connect_mongodb()
    collection = client[table]
    results = collection.find({contrast_field: {"$in": data_list, "$exists": True}})
    return results


def get_mongo_name():
    pass


if __name__ == '__main__':
    # Mongo_table = 'wbh_GPW_detail'
    # find_dict = {"ItemID":"27300"}
    # res = read_one_where_data(Mongo_table,find_dict)
    # for i in res:
    #     print(i)
    pass


