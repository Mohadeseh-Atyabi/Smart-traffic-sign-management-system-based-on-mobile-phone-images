import json
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import csv
import numpy as np
from collections import defaultdict
from xml.etree.ElementTree import Element, SubElement, ElementTree


def coco_to_csv(filename):
    # COCO2017/annotations/instances_val2017.json
    s = json.load(open(filename, 'r'))
    out_file = filename[:-5] + '.csv'
    out = open(out_file, 'w')
    # out.write('id,x1,y1,x2,y2,label/n')

    all_ids = []
    for im in s['images']:
        all_ids.append(im['id'])
    all_fn = []
    for im in s['images']:
        all_fn.append(im['file_name'])
    all_d = []
    for im in s['images']:
        all_d.append((im['height'], im['width']))

    classes = []
    for cl in s['categories']:
        classes.append(cl['name'])

    all_ids_ann = []
    for ann in s['annotations']:
        image_id = ann['image_id']
        all_ids_ann.append(image_id)
        x1 = ann['bbox'][0]
        x2 = ann['bbox'][2] - x1
        y1 = ann['bbox'][1]
        y2 = ann['bbox'][3] - y1
        label = ann['category_id']
        out.write(
            '{},{},{},{},{},{},{},{}/n'.format(classes[label], x1, y1, x2, y2, all_fn[image_id], all_d[image_id][1],
                                               all_d[image_id][0]))


def yolo_to_csv(yolo_dir, destination_dir):
    os.chdir(yolo_dir)
    myFiles = glob.glob('*.txt')
    classes = []
    with open(yolo_dir + '/classes.names', 'rt') as f:
        for l in f.readlines():
            classes.append(l[:-1])

    width = 1024
    height = 1024
    image_id = 0
    final_df = []
    for item in myFiles:

        image_id += 1
        with open(item, 'rt') as fd:
            for line in fd.readlines():
                row = []
                bbox_temp = []
                splited = line.split()
                print(splited)
                try:
                    row.append(classes[int(splited[0])])

                    # print(row)
                    row.append(splited[1])
                    row.append(splited[2])
                    row.append(splited[3])
                    row.append(splited[4])
                    row.append(item[:-4] + ".png")
                    row.append(width)
                    row.append(height)
                    final_df.append(row)

                except:
                    pass
    df = pd.DataFrame(final_df)
    df.to_csv(destination_dir + "/saved.csv", index=False)


def xml_to_csv(path, destination_dir):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        print(xml_file)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            bbx = member.find('bndbox')
            xmin = int(bbx.find('xmin').text)
            ymin = int(bbx.find('ymin').text)
            xmax = int(bbx.find('xmax').text)-xmin
            ymax = int(bbx.find('ymax').text)-ymin
            label = member.find('name').text
            value = (
                     label,
                     xmin,
                     ymin,
                     xmax,
                     ymax,
                     root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text)
                     )
            xml_list.append(value)

    xml_df = pd.DataFrame(xml_list )
    xml_df.to_csv(destination_dir + '/saved.csv', index=None, header=False)


def csv_to_coco(file_dir, destination_dir):
    path = file_dir
    save_json_path = destination_dir + '/traincoco.json'
    clmns = ['class', 'xmin', 'ymin', 'xmax', 'ymax', 'filename', 'width', 'height']
    data = pd.read_csv(path, names=clmns, header=None)
    images = []
    categories = []
    annotations = []
    data['fileid'] = data['filename'].astype('category').cat.codes
    data['categoryid'] = pd.Categorical(data['class'], ordered=True).codes
    data['categoryid'] = data['categoryid'] + 1
    data['annid'] = data.index

    def image(row):
        image = {}
        image["height"] = row.height
        image["width"] = row.width
        image["id"] = row.fileid
        image["file_name"] = row.filename
        return image

    def category(row):
        category = {}
        category["supercategory"] = 'None'
        category["id"] = row.categoryid - 1

        category["name"] = row[1]
        return category

    def annotation(row):
        annotation = {}
        area = (row.xmax) * (row.ymax)
        annotation["segmentation"] = []
        annotation["iscrowd"] = 0
        annotation["area"] = area
        annotation["image_id"] = row.fileid
        annotation["bbox"] = [row.xmin, row.ymin, row.xmax + row.xmin, row.ymax + row.ymin]
        annotation["category_id"] = row.categoryid - 1
        annotation["id"] = row.annid
        return annotation

    for row in data.itertuples():
        annotations.append(annotation(row))
    imagedf = data.drop_duplicates(subset=['fileid']).sort_values(by='fileid')
    for row in imagedf.itertuples():
        images.append(image(row))
    catdf = data.drop_duplicates(subset=['categoryid']).sort_values(by='categoryid')
    for row in catdf.itertuples():
        categories.append(category(row))

    data_coco = {}
    data_coco["images"] = images
    data_coco["categories"] = categories
    data_coco["annotations"] = annotations
    json.dump(data_coco, open(save_json_path, "w"), indent=4)


def csv_to_yolo(csv_file,destination_folder):
    classes_names = []
    if not os.path.exists(destination_folder+'/data'):
        os.makedirs(destination_folder+'/data')
    file_names = []
    data = csv.reader(open(csv_file))
    for l in data:
        file_names.append(l[5])
        classes_names.append(l[0])
    classes_names = np.unique(classes_names)
    classes = {k: v for v, k in enumerate(classes_names)}
    f=open(destination_folder+"/data/"+ 'classes.names','a')
    for i in classes_names:
        f.write(str(i))
        f.write('/n')
    f.close()
    for name in np.unique(file_names):
        file = open(destination_folder+'/data/'+str(name[:-4])+".txt",'a')
        for l in csv.reader(open(csv_file)):
            if(l[5]==name):
                file.write(str(classes[l[0]]))
                file.write(' ')
                file.write(l[1])
                file.write(' ')
                file.write(l[2])
                file.write(' ')
                file.write(l[3])
                file.write(' ')
                file.write(l[4])
                file.write(' ')
                file.write('/n')
    file.close()


def csv_to_voc_pascal(file_dir, save_root2):
    file_dir = 'here1.csv'
    save_root2 = save_root2 + "/result_xmls"
    if not os.path.exists(save_root2):
        os.mkdir(save_root2)

    def write_xml(folder, filename, bbox_list):
        root = Element('annotation')
        SubElement(root, 'folder').text = folder
        SubElement(root, 'filename').text = filename
        SubElement(root, 'path').text = './images' + filename
        source = SubElement(root, 'source')
        SubElement(source, 'database').text = 'Unknown'

        # Details from first entry
        e_class_name, e_xmin, e_ymin, e_xmax, e_ymax, e_filename, e_width, e_height = bbox_list[0]
        size = SubElement(root, 'size')
        SubElement(size, 'width').text = e_width
        SubElement(size, 'height').text = e_height
        SubElement(size, 'depth').text = '3'
        SubElement(root, 'segmented').text = '0'

        for entry in bbox_list:
            e_class_name, e_xmin, e_ymin, e_xmax, e_ymax, e_filename, e_width, e_height = entry
            obj = SubElement(root, 'object')
            SubElement(obj, 'name').text = e_class_name
            SubElement(obj, 'pose').text = 'Unspecified'
            SubElement(obj, 'truncated').text = '0'
            SubElement(obj, 'difficult').text = '0'

            bbox = SubElement(obj, 'bndbox')
            SubElement(bbox, 'xmin').text = e_xmin
            SubElement(bbox, 'ymin').text = e_ymin
            SubElement(bbox, 'xmax').text = e_xmax
            SubElement(bbox, 'ymax').text = e_ymax

        # indent(root)
        tree = ElementTree(root)
        xml_filename = os.path.join('.', folder, os.path.splitext(filename)[0] + '.xml')
        tree.write(xml_filename)

    entries_by_filename = defaultdict(list)

    with open(file_dir, 'r', encoding='utf-8') as f_input_csv:
        csv_input = csv.reader(f_input_csv)
        header = next(csv_input)
        class_name, xmin, ymin, xmax, ymax, filename, width, height = header
        header[3] = str(int(header[1]) + int(header[3]))
        header[4] = str(int(header[2]) + int(header[4]))
        entries_by_filename[filename].append(header)
        for row in csv_input:
            class_name, xmin, ymin, xmax, ymax, filename, width, height = row
            row[3] = str(int(row[1]) + int(row[3]))
            row[4] = str(int(row[2]) + int(row[4]))
            # print(row)
            entries_by_filename[filename].append(row)
    for filename, entries in entries_by_filename.items():
        # print(filename, len(entries))
        write_xml(save_root2, filename, entries)


xml_to_csv("C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/Dataset/train",
           "C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/Dataset")