
import codecs
from json import dump
import json
import re
from sklearn.metrics import cohen_kappa_score
from optparse import OptionParser

def order_to_startposition(labels):
    return sorted(labels, key=lambda k: int(k['i_start']))

def calc_kappa(file1, file2, file3=None, save_wrong_sentences=False):
    with codecs.open(file1, "r", "utf-8", errors='ignore') as f_1:
        with codecs.open(file2, "r", "utf-8", errors='ignore') as f_2:

            if file3 != None:
                f_3 = codecs.open(file3, "r", "utf-8", errors='ignore')
                
            file1_content = json.load(f_1)
            file2_content = json.load(f_2)

            if file3 != None:
                file3_content = json.load(f_3)

            labels_1 = []
            labels_2 = []
            labels_3 = []
            merge_label = []
            orininal_label = []
            count = 0
            sentences_save = []
            
            for i in range(0, len(file1_content)):
                pos_file2 = [pos for pos in range(0, len(file2_content)) if file2_content[pos]['id'] == file1_content[i]['id']][0]
                sentence_file1 = file1_content[i]
                sentence_file2 = file2_content[pos_file2]
                
                if file3 != None:
                    pos_file3 = [pos for pos in range(0, len(file3_content)) if file3_content[pos]['id'] == file1_content[i]['id']][0]
                    sentence_file3 = file3_content[pos_file3]

                    labels_1 = ([l['type'] for l in order_to_startposition(sentence_file1['labels'])])
                    labels_2 = ([l['type'] for l in order_to_startposition(sentence_file2['labels'])])
                    labels_3 = ([l['type'] for l in order_to_startposition(sentence_file3['labels'])])
                    entrou = False

                    for x in range(0, len(labels_1)):
                        #validacao
                        if sentence_file1['id'] != sentence_file2['id'] or sentence_file1['id'] != sentence_file3['id']:
                            print('ids diferentes')
                            exit()

                        if labels_1[x] == labels_2[x] and labels_1[x] == labels_3[x]:                              
                            orininal_label.append(labels_1[x])
                            merge_label.append(labels_1[x])
                        # elif labels_2[x] == labels_3[x]:
                        #     orininal_label.append(labels_2[x])
                        #     merge_label.append(labels_2[x])
                        else:
                            entrou = True
                            count += 1 
                            orininal_label.append(labels_1[x])
                            merge_label.append('-1')

                    if entrou == True:
                        sentences_save.append(sentence_file2)
                else:
                    labels_1 = ([l['type'] for l in order_to_startposition(sentence_file1['labels'])])
                    labels_2 = ([l['type'] for l in order_to_startposition(sentence_file2['labels'])])
                    entrou = False

                    for x in range(0, len(labels_1)):
                        if labels_1[x] == labels_2[x]:                              
                            orininal_label.append(labels_1[x])
                            merge_label.append(labels_1[x])
                        else:
                            entrou = True
                            count += 1
                            # if labels_1[x] == '0' or labels_1[x] == '2':
                            #     count += 1
                            # print(labels_2[x])
                            orininal_label.append(labels_1[x])
                            merge_label.append(labels_2[x])
                    
                    if entrou == True:
                        sentences_save.append(sentence_file2)
                        print(sentence_file1['id'])

            if file3 == None:
                print(cohen_kappa_score(orininal_label, merge_label, [ '0','1','2','3','4']))
            else:
                print(cohen_kappa_score(orininal_label, merge_label, ['-1', '0','1','2','3','4']))
            
            print(count)

    if save_wrong_sentences == True:
        f = codecs.open('sentences_to_evaluate.json', 'w', 'utf-8')
        dump(sentences_save, f, indent=4, ensure_ascii=False)
        f.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-t', '--twitter', action='store_true', dest='is_twitter', default=False)
    parser.add_option('-n', '--new', action='store_true', dest='new_labeling', default=False)
    option, args = parser.parse_args()

    if option.new_labeling == True:
        if option.is_twitter == True:
            calc_kappa("concordance/webmedia/daniel_to_label_twitter_ajustado.json", "concordance/webmedia/adriana_to_label_twitter_ajustado.json", "concordance/webmedia/arthur_to_label_twitter_ajustado.json", False)
        else:
            calc_kappa("concordance/webmedia/daniel_to_label_buscape_ajustado.json", "concordance/webmedia/adriana_to_label_buscape_ajustado.json", "concordance/webmedia/arthur_to_label_buscape_ajustado.json", False)
    else:
        if option.is_twitter == True:
            calc_kappa("concordance/person1_twitter_merge.json", "concordance/person2_twitter_merge.json", "concordance/person3_twitter_merge.json", False)
        else:        
            calc_kappa("concordance/person1_buscape_merge.json", "concordance/person2_buscape_merge.json", "concordance/person3_buscape_merge.json", False)




