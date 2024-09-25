import json

path = 'json_full/merged_physics.json'
with open(path, 'r', encoding='utf-8') as file:
    data = json.load(file)

for item in data:
    l = int(item['id'][5:])
    if l % 5 == 0 :
        l = l//5
    else:
        l = int(item['id'][5:])//5+1
    f = item['id'][:3]
    s = item['id'][5:]
    l = '{:02}'.format(l)
    item['id'] = f+l+s

with open(path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
