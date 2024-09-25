import shutil
from os import walk
import csv

main_dir = '../../Study/Data/'

src_dir = main_dir + 'final/'
dest_dir = main_dir + 'organised/'


f = []
for (dirpath, dirnames, filenames) in walk(src_dir):
    f.extend(filenames)
    break

dataset = {}
with open(main_dir + 'anonymized_file_base.csv', mode='r') as file_base:
    reader = csv.reader(file_base)
    dataset = {rows[0]: [rows[1], rows[2], rows[3], rows[4]] for rows in reader}

dataset.pop('fileID')

for data in dataset:
    fields = dataset.get(data)
    id = fields[0]
    type = '_pd' if fields[1] == 'caso' else '_healthy'
    on_off = '_' + fields[2] if fields[2] != 'NA' else ''
    hand = '_r' if fields[3] == 'd' else '_l'
    final_dest_dir = dest_dir

    if dest_dir == main_dir + 'organised/':
        if fields[1] == 'caso':
            final_dest_dir += 'pd/' + fields[2] + '/'
        else:
            final_dest_dir += 'healthy/'

    shutil.copyfile(src_dir + data + '.csv', final_dest_dir + id + type + on_off + hand + '.csv')


