#coding:utf-8
import quickfind
import csv

def save_csv(result):
    '''
    produce source-target file named ts.csv
    '''
    w1 = csv.writer(open("ts.csv", "w"))
    for k, v in result.items():
        if len(v) == 0:
            w1.writerow([k, k])
        else:
            for i in v:
                w1.writerow([k, i])

def classify(result, n):
    '''
    read the dictionary given
    create list reflecting the connection, set containing all functions
    data given, currently set empty
    '''
    Dic = result
    qf = quickfind.QuickFind(n)  # 11 is number of nodes in test case
    lista = []
    # get the key set of dictionary
    func_set = set(Dic.keys())

    num = 0;
    all_dic = {}
    func_dic = {}
    for key in func_set:
        func_dic[key] = num
        all_dic[key] = num
        num += 1

    for k, v in Dic.items():
        for n in v:
            if n not in all_dic:
                all_dic[n] = num
                num += 1
            # print all_dic[k] + all_dic[n]
            lista.append((all_dic[k], all_dic[n]))

    # union the nodes

    for k in lista:
        p = k[0]
        q = k[1]
        qf.union(p, q)
    # Below, test whether union
    # print "%d and %d is connected? %s" % (p,q,str(qf.connected(p,q)    ))

    # dictionary: root as key, list of functions as value
    rst_dic = {}
    # check the connectivity of function
    for k, v in func_dic.items():
        root = qf.id[v]
        # print root, rst_dic.has_key(root)

        if root not in rst_dic:
            rst_dic[root] = [k]
        else:
            rst_dic[root].append(k)

    # output_dic: dictionary in dictionary
    output_dic = {}
    index = 0
    for k, v in rst_dic.items():
        tmp_dic = {}
        for fc in v:
            tmp_dic[fc] = Dic[fc]
        output_dic[index] = tmp_dic
        index += 1
    return  output_dic

def output(output_dic, name, output_width = 100):
    '''
    use output_dic to generate output
    '''
    f = open(name, 'w')
    for k, v in output_dic.items():
        fc_list = []
        vr_list = []
        for j, k in v.items():
            fc_list.append(j)
            vr_list = vr_list + k
        tmp_list = list(set(vr_list))

        new_str = ''
        cur_len = 0
        for i in range(0, len(fc_list)):
            if (cur_len + len(fc_list[i]) + 2) <= output_width:
                new_str = new_str + str(fc_list[i]) + ', '
                cur_len += len(fc_list[i]) + 2
            else:
                cur_len = len(fc_list[i]) + 2
                new_str = new_str + '\n' + str(fc_list[i]) + ', '
        f.write(new_str)
        f.write('\n')
        for i in range(0, output_width):
            f.write('-')
        f.write('\n')

        new_vrstr = ''
        cur_len = 0
        for i in range(0, len(tmp_list)):
            if (cur_len + len(tmp_list[i]) + 2) <= output_width:
                new_vrstr = new_vrstr + str(tmp_list[i]) + ', '
                cur_len += len(tmp_list[i]) + 2
            else:
                cur_len = len(tmp_list[i]) + 2
                new_vrstr = new_vrstr + '\n' + str(tmp_list[i]) + ', '

        f.write(new_vrstr)
        f.write('\n')
        for i in range(0, output_width):
            f.write('=')
        f.write('\n')
    f.close()