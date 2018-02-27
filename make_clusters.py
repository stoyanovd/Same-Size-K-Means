import json
import sys

from clustering.equal_groups import EqualGroupsKMeans
import numpy as np
import matplotlib.pyplot as plt

lon = 'lon'
lat = 'lat'
label = 'label'


def get_ans(n_clusters, array_id_lon_lat):
    X = np.array(list([p['lon'], p['lat']] for p in array_id_lon_lat))

    clf = EqualGroupsKMeans(n_clusters=n_clusters)
    clf.fit(X)

    # print(clf.labels_)

    # caution, it's inplace
    for i in range(len(array_id_lon_lat)):
        array_id_lon_lat[i]['label'] = int(clf.labels_[i])

    return array_id_lon_lat


def draw_plot(n_clusters, array_id_lon_lat):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    for i in range(n_clusters):
        a = []
        for j in range(len(array_id_lon_lat)):
            if array_id_lon_lat[j]['label'] == i:
                a += [[array_id_lon_lat[j]['lon'], array_id_lon_lat[j]['lat']]]
        plt.plot(*zip(*a), marker='o', color=colors[i], ms=4.5, linestyle='None')

    plt.figure(num=1, figsize=(20, 10))
    plt.savefig('ans.png')


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('--n_clusters', type=int,
                                help='number of clusters', required=True)
    required_named.add_argument('--draw_plot', type=int,
                                help='draw plot or not draw (into file "ans.png"). Put 1 or 0.',
                                required=True)
    required_named.add_argument('--input_json_file',
                                help='file with json with geo points. Format:' +
                                     "[{'id':1, 'lon':2.2, 'lat':3.3}, ... ]",
                                required=True)

    required_named.add_argument('--output_json_file',
                                help='file with json with geo points. Format:' +
                                     "[{'id':1, 'label': 5, 'lon':2.2, 'lat':3.3}, ... ]",
                                required=True)

    args = parser.parse_args()

    # [{'id':1, 'lon':2.2, 'lat':3.3}, ... ]
    array_id_lon_lat = json.load(open(args.input_json_file, encoding='utf-8'))  # , parse_float=True, parse_int=True)

    array_id_label_lon_lat = get_ans(args.n_clusters, array_id_lon_lat)

    if args.draw_plot == 1:
        draw_plot(args.n_clusters, array_id_label_lon_lat)

    json.dump(array_id_label_lon_lat, open(args.output_json_file, 'w', encoding='utf-8'))


if __name__ == '__main__':
    # print(sys.argv) # here are all arguments
    main()
