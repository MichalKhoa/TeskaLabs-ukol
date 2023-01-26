import json
import pymongo

from datetime import datetime
start_time = datetime.now()
'''
To compare runtime of the code
'''

file = open("sample-data.json", "r")
loaded_data = json.load(file)

MongoDBlink = input('Paste a link to the MongoDB db:')
cluster = pymongo.MongoClient(MongoDBlink)
db = cluster['test_database']
col = db["test_output"]


def get_name(data):
    return data.get("name")


def get_cpu_usage(data):
    try:
        return data["state"]["cpu"].get("usage")
    except TypeError:
        return 0
    
    
def get_memory_usage(data):
    try:
        return data["state"]["memory"].get("usage")
    except TypeError:
        return 0
    

def get_status(data):
    return data.get("status")


def get_created_at(data):
    return datetime.timestamp(datetime.strptime(data.get("created_at"), "%Y-%m-%dT%H:%M:%S%z"))


def get_ip_addresses(data):
    try:
        list_of_keys = list(data["state"]["network"].keys())
        ip_addresses = []
        for j in range(len(list_of_keys)):
            for k in range(len(data["state"]["network"][list_of_keys[j]]["addresses"])):
                try:
                    ip_addresses.append(data["state"]["network"][list_of_keys[j]]["addresses"][k]["address"])
                except TypeError:
                    continue
                except IndexError:
                    ip_addresses.append(data["state"]["network"][list_of_keys[j]]["addresses"]["address"])
                    break
        return ip_addresses
    except TypeError:
        return "No assigned IP addresses"


def parse_and_extract(data):
    for i in range(len(data)):
        post = dict()

        post['name'] = get_name(data[i])
        post['cpu usage'] = get_cpu_usage(data[i])
        post['memory usage'] = get_memory_usage(data[i])
        post['status'] = get_status(data[i])
        post['created_at'] = get_created_at(data[i])
        post['assigned IP addresses'] = get_ip_addresses(data[i])

        col.insert_one(post)


def main():
    parse_and_extract(loaded_data)


if __name__ == '__main__':
    main()

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))
