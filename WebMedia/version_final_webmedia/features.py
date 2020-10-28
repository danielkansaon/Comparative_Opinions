import json


with open('twitter_dataset.json', 'r') as file1:
    content = json.load(file1)
    dict_features = {}

    for sentence in content:
        labels = sentence['labels']

        for label in labels:
            if label['type'] == '1':
                if 'feature' in label:
                    dict_features[label['feature']] = 0

print(dict_features)

