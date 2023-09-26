import json
import array as arr

# Opening JSON file
f = open("E:/project-3-at-2023-01-03-13-40-ddd008ba-COCO/result.json")


data = json.load(f)
cat = arr.array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# Calculate the number of instances for each class
for i in data['annotations']:
    cat[i['category_id']] = cat[i['category_id']] + 1

for i in range(18):
    print(data['categories'][i]['name'] + ": " + str(cat[i]))

'''
Correcting the name of the images and create new json as new_result.
It is the true annotation file for our dataset.
'''
for img in data['images']:
    img['file_name'] = img['file_name'].replace('images\\3/', '')

with open("E:/project-3-at-2023-01-03-13-40-ddd008ba/new_result.json", 'w') as f:
    json.dump(data, f)

# Closing file
f.close()