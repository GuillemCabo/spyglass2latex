#!/usr/bin/python
import sys
import re
#Arguments:
    # arg0 -> .self
    # arg1 -> Path to Spyglass Port report to process
    # arg2 -> Path of the ouput file    
#Number of valid arguments
x = 3
#Position of output file in args
ain = 1
#Position of output file in args
aout = 2
#Number of columns to parse
ncol = 6
#Enable debug mode
debug = False
#debug = True

# Auxiliar functions
def ParseReportInfo( s ):
    ######Example input
    ######     Report Created by: drac
    ######     Report Created on: Mon Sep 21 09:49:43 2020
    ######     Working Directory: /tmp/RDC
    ######     Report Location  : ./RDC/RDC/lint/lint_rtl/spyglass_reports/morelint/ReportPortInfo
    ######     SpyGlass Version : SpyGlass_vO-2018.09-SP1-1
    ######     Policy Name      : morelint(SpyGlass_vO-2018.09-SP1-01)
    ######     Comment          : Report Top Level Module Port Info
    #TODO
    return

def ParseModuleInfo( s ):
    ######Example input
    #####   Module: RDC
    #####   ---------------
    #####   Module Type: Top_Level
    #TODO
    moduleinfo = ["",""]
    if "Module:" in s:
        # remove all spaces
        s=re.sub(' +', '',s)
        # remove tabs
        s=re.sub('\t', '',s)
        # remove line jumps
        s=re.sub('\n', '',s)
        # backslack all the underscores to avoid latex problems
        s=re.sub('_', '\_',s)
        # Remove name
        s=re.sub('Module:','',s)
        moduleinfo[0]=s
    if "Module Type" in s:
        # remove all spaces
        s=re.sub(' +', '',s)
        # remove tabs
        s=re.sub('\t', '',s)
        # remove line jumps
        s=re.sub('\n', '',s)
        # backslack all the underscores to avoid latex problems
        s=re.sub('_', '\_',s)
        # Remove name
        s=re.sub('ModuleType:','',s)
        moduleinfo[1]=s
    return moduleinfo

def ParseMatrixInfo( s ):
    ######Example input
    #####    Port Name            Direction       Width      Index                Comment                             Comment Source
    #####    -------------------------------------------------------------------------------------------------------------
    #####    clk_i                INPUT           1          -                    Width of data registers             module port
    #####    rstn_i               INPUT           1          -                    Active low asyncronous reset. It... module port
    #####    enable_i             INPUT           1          -                    can be generated                    module port
    #####    events_i             INPUT           8          [0:3][1:0]           Monitored events that can genera... module port
    #####    events_weights_i     INPUT           64         [0:3][0:1][7:0]      internally registered, set by so... module port
    #####    interruption_rdc_o   OUTPUT          1          -                    Event longer than specified weig... module port
    #####    interruption_vector_rdc_o OUTPUT          8          [0:3][1:0]           Interruption vector to indicate ... module port
    #####    watermark_o          OUTPUT          64         [0:3][0:1][7:0]      High watermark for each event of... module port
    #####    ===========================================================================================================
    
    debug = False
    #debug = True
    
    matrix_row = [""]
    # remove tabs
    s=re.sub(' +\t', '',s)
    # remove line jumps
    s=re.sub(' +\n', '',s)
    # remove two or more spaces
    s=re.sub('  +', ';',s)
    # Signal new element after automatic elipsis
    s=re.sub('\.\.\. ', '...;',s)
    # backslack all the underscores to avoid latex problems
    s=re.sub('_', '\_',s)
    if (debug):
        print s
    return s 
    
#check if there are enough arguments
if (len(sys.argv) < x):
    print 'not enough arguments' 
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    sys.exit()

if(len(sys.argv) > x):
    print 'Too much arguments' 
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    sys.exit()

# Store all the fields of the original file as lists. The first item of the 

# Info fields of the report
created_by = ["Report Created by: "] 
created_on = ["Report Created on: "]
work_dir = ["Working Directory: "]
report_loc = ["Report Location  : "]
spy_ver = ["SpyGlass Version : "]
policy = ["Policy Name      : "]
comment = [" Comment          : "]

#Section Separator
ssep1= "################################################################################"

# Info fields of the module
##Section Separator
ssep2= "Port Name            Direction       Width      Index                Comment                             Comment Source"
##Module type name
module = ""
##Module type
mtype = ""
##Skip this line
port_name = [""]
direction = [""]
width = [""]
index = [""]
#Module Comment
mcomment = [""]
#Module Comment Source
mscomment = [""]
# Report Matrix Separate fileld name from values
fn_sep="-------------------------------------------------------------------------------------------------------------"
# Report Matrix end separator
ssep3= "==========================================================================================================="

#Read content from file, save parsed lines
parsed = ""
reader = open(sys.argv[ain])
try:
    print 'Parsing file: ',str(sys.argv[ain]) 
    print 'Output file: ',str(sys.argv[aout]) 
    # Get rid of first line
    line = reader.readline()
    # Get lines until module info (Report info)
    # The string where the section ends shall be:
    line = reader.readline()
    cnt = 2
    #while (line ):
    while ((ssep1 in line) is False) :
        if(debug):
            print("Info_rep {}: {}".format(cnt, line.strip()))
        line = reader.readline()
        ParseReportInfo(line);
        cnt += 1
    # Get lines until module matrix (Module info)
    while ((ssep2 in line) is False) :
        tmp_minfo = []
        if(debug):
            print("Info_mod {}: {}".format(cnt, line.strip()))
        line = reader.readline()
        tmp_minfo = ParseModuleInfo(line)
        # This can be done better
        if (tmp_minfo[0] and not module):
            module = tmp_minfo[0] 
        if (tmp_minfo[1] and not mtype):
            mtype = tmp_minfo[1] 
        cnt += 1
    # Get lines until the end (Module Port matrix)
    while ((ssep3 in line) is False) :
        parsed = ParseMatrixInfo(line)
        tmp_list = parsed.split(";")
        #ignore incomplete lines 
        if (len(tmp_list) == ncol):
            #TODO rewrite and avoid hardcoded ncol
            port_name.append(tmp_list[0]) 
            direction.append(tmp_list[1])
            width.append(tmp_list[2])
            index.append(tmp_list[3])
            mcomment.append(tmp_list[4])
            mscomment.append(tmp_list[5])
        else:
            print "#######################################"
            print "This line has {} arguments instead of {}".format(len(tmp_list),ncol)
            print "excluded:"+parsed
            print tmp_list

        if(debug):
            print("Mod_mat {}: {}".format(cnt, line.strip()))
        line = reader.readline()
        cnt += 1
finally:
    reader.close()

#Gather result matrix
matrix=[port_name,direction,width,index,mcomment,mscomment]
if(debug):
    print "*********************\n"
    print('\n'.join(' '.join(map(str,sl)) for sl in matrix))
    print "*********************\n"
# Display output file. Number of items is hardcoded
# rewrite to use ncol instead
tex_out=[]
tex_out.append("\\begin{table}[]")
tex_out.append("\\begin{tabular}{llllll}")
tex_out.append("\\hline")
#parsed matrix
tex_out.append(port_name[1]+" & "+ direction[1] +" & "+ width[1] +" & "+ index[1] +" & "+ mcomment[1] +" & "+ mscomment[1]+"\\\\")
tex_out.append("\\hline")
for n in range (2,len(port_name)):
    tex_out.append(port_name[n]+" & "+ direction[n] +" & "+ width[n] +" & "+ index[n] +" & "+ mcomment[n] +" & "+ mscomment[n]+"\\\\")
tex_out.append("\\hline")
tex_out.append("\\end{tabular}")
tex_out.append("\\caption{Ports of module "+ module +"}")
tex_out.append("\\label{port:"+module+"}")
tex_out.append("\\end{table}")
if(debug):
    print "*********************\n"
    print tex_out
    print "*********************\n"
# Write output file
f = open(sys.argv[aout], 'w')
try:
    for item in tex_out:
            f.write("%s\n" % item)
finally:
    f.close
