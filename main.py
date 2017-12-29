#coding:utf-8
import sys
import CodeAnalyse as ca
import classify

###############################################################################

__author__ = 'Luo Yaoxiang <luoyaox@qq.com>' \
             'Shi Junjie <jushi@microstrategy.com>' \
             'Gao Mengru <mgao@microstrategy.com>'

__date__, __version__ = '12/26/2017', '0.01'  # Creation
__date__, __version__ = '12/28/2017', '1.00'  # First release

__description__ = 'Final goal of this tool is to do code refactoring automatically. ' \
                  'Now we have finished the part of separate a big class into several small classes.'

__note__ = '12/26/2017   Gao       - H file parsing & Visualizing with Pygame and Plotly' \
           '12/26/2017   Luo       - CPP file parsing & Extracing relations between vars and funcs' \
           '12/26/2017   Shi       - Clustering classes using relations & Visualizing with MSTR Workstaiton'

################################################################################    

def read_argv():
	from optparse import OptionParser
	this_version = 'v%s (c) %s %s' % (__version__, __date__.split('/')[2], __author__)
	this_description = __description__
	this_usage = '''%prog'''
	parser = OptionParser(version=this_version, description=this_description, usage=this_usage)
	parser.add_option('-v', '--visualize',
                  action='store', dest='visualize', default=None,
                  help='visualize the relations. --plotly: Visualize with plotly, need to install required libs \n' \
                  		'--csv: Import csv file to visualize with MSTR workstation \n' \
                  		'--pygame: Visualize with pygame, need to install required libs. ' \
                  		'We suggest using plotly to load large scale of data rather than pygame.'
                  		)
	(options, args) = parser.parse_args()
	return options, args

if __name__ == '__main__':
	options, args = read_argv()
	#main()
	__VISUSALIZE__=options.visualize
	if len(args)!=2 or (args[0][-2:]!='.h' and args[-4:]!='.cpp') or (args[0][:-2]!=args[1][:-4]):
		print("This program takes two args: .h file and .cpp file with the same name")
		exit(0)
	h_path = args[0]
	cpp_path = args[1]
	analyzer = ca.CodeAnalyse(h_path,cpp_path)
	# get relevance between vars and funcs
	relevance = analyzer.get_relevance_between_var_and_func()
	# get funcs list and vars list
	funcs_list = analyzer.funcs_list
	vars_list = analyzer.vars_list
	# classify
	n = len(set(vars_list)) + len(set(funcs_list))
	output_dic = classify.classify(relevance, n)
	# output result as txt
	classify.output(output_dic, 'output_file.txt')
	print("Success classify!")
	#draw_fig(output_dic)
	# save relevance for visualize
	if __VISUSALIZE__=='csv':
		classify.save_csv(relevance)
	# visualize
	if __VISUSALIZE__=='plotly':
		import draw
		print('Waiting for visualizing with plotly...')
		draw.visualize(relevance)
	if __VISUSALIZE__=='pygame':
		import draw_pygame
		print('Waiting for visualizing with pygame...')
		draw_pygame.visualize(output_dic)	
	#else:
	#	print("Warning: -v takes only csv, plotly and pygame")	
