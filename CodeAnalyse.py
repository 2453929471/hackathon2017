#coding:utf-8
import re

MODIFIERS=["public:","protected:","private:"]

class CodeAnalyse(object):
    def __init__(self, hfile_path, cpp_path):
        self.hfile_path = hfile_path
        self.cpp_path = cpp_path
        self.MAIN_CLASS_NAME = cpp_path[:cpp_path.rfind('.')]
        self.friends = []
        self.extends = []
        self.varables = {}
        self.funcs = {}
        self.vars_list = []  # 所有变量列表
        self.vars_list_without_ptr = []
        self.funcs_list = [] #所有函数列表
        self.relevant = {}  #所有成员变量与成员函数的相互关系

    def get_relevance_between_var_and_func(self):
        self.getvf()
        self.get_relativity()
        return self.relevant

    def getvf(self):
        '''
        分析头文件，确定所有的成员变量与成员函数
        '''
        hfile = open(self.hfile_path, 'r')
        lines = self.clean(hfile)
        i = self.extract_extends(lines)
        stack = 1
        while i < len(lines):
            # 等匹配到 } 函数体才正式结束
            line = lines[i]
            if stack > 0: 
                if line.find('public:') > -1:
                    stack, i = self.extract_modifier("public", lines, stack, i + 1)
                    continue
                if line.find("protected:") > -1:
                    stack, i = self.extract_modifier("protected", lines, stack, i + 1)
                    continue
                if line.find("private:") > -1:
                    stack, i = self.extract_modifier("private", lines, stack, i + 1)
                    continue
                else:
                    i += 1
            else:
                break
        for k, v in self.varables.items():
            s = 0
            for vv in v:
                vv = vv.replace('\t', ' ')
                var_name = vv.split()[-1].strip(';')
                self.vars_list.append(var_name)
                if var_name.find('*') != -1:
                    self.vars_list_without_ptr.append(var_name[var_name.rfind('*') + 1:])
                else:
                    self.vars_list_without_ptr.append(var_name)
                s += 1

        for k, v in self.funcs.items():
            s = 0
            for vv in v:
                s += 1
                slices = vv.replace('\t', ' ').split()
                if vv.find('~') != -1: continue
                for x in range(1, len(slices)):
                    idx = slices[x].find('(')
                    if idx == -1:
                        continue
                    elif idx == 0:
                        func_name = slices[x - 1]
                    else:
                        func_name = slices[x][:idx]
                    self.funcs_list.append(func_name)
                    break

    def extract_extends(self, lines):
        # print "调用extract_extends"
        i = 0
        class_start_line = 0
        while i < len(lines):
            line = lines[i]
            if line.find('class') > -1 and (
                    line.find(self.MAIN_CLASS_NAME + ':') > -1 or line[-len(self.MAIN_CLASS_NAME):] == self.MAIN_CLASS_NAME):
                while line.find('{') == -1:
                    if line.find('public') > -1:
                        parent = line[line.find('public') + 7:].strip(',')
                        self.extends.append(parent)
                    i = i + 1
                    line = lines[i]
                class_start_line = i
                break
            i += 1
        return class_start_line

    def extract_modifier(self, mod, lines, stack, i):
        if mod not in self.varables.keys():
            self.varables[mod] = []
        if mod not in self.funcs.keys():
            self.funcs[mod] = []
        while stack > 0 and (lines[i] not in MODIFIERS):
            line = lines[i]
            if line == '{':
                stack += 1
                i += 1
                continue
            if line in ['}', '};']:
                stack -= 1
                i += 1
                continue
            if line.find(';') > -1:
                # 确定变量
                if line.find('(') == -1:
                    self.varables[mod].append(line)
                    i += 1
                # 无实现 函数
                else:
                    self.funcs[mod].append(line)
                    i += 1
            else:
                tmp = ''
                while line.find(';') == -1:
                    tmp += line
                    if i + 1 < len(lines):
                        i = i + 1
                        line = lines[i]
                    else:
                        break
                tmp += line
                if tmp.find('{') == -1:
                    # 超长 无实现 函数
                    self.funcs[mod].append(tmp)
                    i += 1
                else:
                    # 超长 有实现 函数
                    stack += (tmp.count('{') - tmp.count('}'))
                    i += 1
                    while stack > 1 and i < len(lines):
                        line = lines[i]
                        tmp += line
                        stack += (line.count('{') - line.count('}'))
                        i += 1
                        self.funcs[mod].append(tmp)
        return stack, i

    def get_relativity(self):
        '''
        分析cpp文件，获得所有成员函数与成员变量的关系
        '''
        cppfile = open(self.cpp_path, 'r')
        cpplines = self.clean(cppfile)  # 以后补充：去除空白行，恶心格式
        for i in range(len(cpplines)):
            if (cpplines[i].find('(') != -1):
                Llist = re.split(r'[\s+:(]', cpplines[i])
                for Lstr in Llist:
                    if Lstr in self.funcs_list:
                        while cpplines[i].find(')') == -1:
                            i += 1
                        if cpplines[i].find('{') != -1 or (
                                i < len(cpplines) and cpplines[i + 1].find('{') != -1):  # 以后补充恶心情况
                            fun_var, i = self.analyse_func(i, Lstr, cpplines)
                            self.relevant[Lstr] = fun_var
                            break

    def analyse_func(self, index, fun, cpplines):
        '''
        分析一个函数体，记录所有与该函数相关的成员变量和成员函数
        :param index: fun在cpplines的位置
        :param fun: 正在分析的函数体名称
        :param cpplines: 预处理后的cpp数据
        :return: 与该函数相关的成员变量和成员函数list
        '''
        mystack = 1
        related = [] if fun not in self.relevant else self.relevant[fun]
        if cpplines[index].find('{') == -1: index += 1  # 此后的index指向有{那行
        # 防止其他类型通过->和.引用同名的成员,防止搜到“”内的字符串
        def check(Lstr, targetset, line):
            if Lstr in targetset:
                index = line.find(Lstr)
                if index > 0 and line[index - 1] == '.': return False
                if index > 1 and line[index - 1] == '>' and line[index - 2] == '-': return False
                if line[:line.find(Lstr)].count('"') % 2 == 1: return False  # 先不管有重复Lstr在一行，并且前面的被包，后面的没包的情况
                return True
            else:
                return False
        while mystack:
            index += 1
            line = cpplines[index]
            mystack += line.count('{')
            mystack -= line.count('}')
            Llist = re.split(r'[^\w]', line)#分割标识符，引起的bug由check弥补
            while '' in Llist: Llist.remove('')
            for Lstr in Llist:
                if check(Lstr, self.vars_list_without_ptr, line): related.append(Lstr)
                if check(Lstr, self.funcs_list, line):
                    #	if Lstr in od: Lstr = get_real_name(Lstr, line)#重载函数处理
                    related.append(Lstr)
        related = list(set(related))
        return related, index

    def clean(self, file):
        '''
        cpp与h文件的格式化预处理
        comment_flag:0 表示当前line可以考虑考虑
        comment_flag:1 如果当前line不以 */ 开头，直接跳过
        对友类的处理直接放入clean
        处理 a=1+/*RECT_SIZE*/ELLIPSE_SIZE这种情况直接不考虑
        '''
        lines = []
        comment_flag = 0
        for line in file:
            line = line.strip('\n').strip('\t').strip(' ')
            line = line[:(line.find('//') if line.find('//') > -1 else None)]
            if line.find('#') == 0:
                continue
            if line.strip('\n').strip() == '':
                continue
            if line.find('/*') > -1 and line.find('*/') > -1:
                line = line.replace(line[line.find('/*'):line.find('*/') + 2], '')
            if comment_flag == 1:
                if line.find('*/') > -1:
                    comment_flag = 0
                else:
                    continue
            else:
                if line.find('/*') == 0:
                    comment_flag = 1
                else:
                    if line.find('friend') > -1:
                        # print "找到friend类:",line
                        self.friends.append(line.strip(';').split()[-1])
                        continue
                    lines.append(line)
                    # print >> bbb,line
        return lines
