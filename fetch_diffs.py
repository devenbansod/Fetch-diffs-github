import urllib2
import sys
import argparse

# initial config - default values if arguments not specified
inp_file = "diffs_list.txt"
user_org = "phpmyadmin"
respository = "phpmyadmin"
directory = ""

parser = argparse.ArgumentParser()

parser.add_argument('-i', required=True, action='store', dest='input_file',
                    help='Specify the input file with list of PR numbers AND/OR commit ids')

parser.add_argument('-d', required=True, action='store', dest='directory',
                    help='Specify output directory to store the diff/patch files')

parser.add_argument('-r', action='store', dest='respository',
                    help='Specify the respository')

parser.add_argument('-u', action='store', dest='user_org',
                    help='Specify the username')

parser.add_argument('--patch', action='store_true', dest='patch',
                    help='Store patches instead of diffs')

parser.add_argument('--both', action='store_true', dest='both',
                    help='Store both diffs and patches')

parser.add_argument('--separate', action='store_true', dest='separate',
                    help='Store diffs and patches in separate folders (only used with --both option)')


results = parser.parse_args()
if results.input_file:
	inp_file = results.input_file
if results.directory:
	directory = results.directory
if results.respository:
	respository = results.respository
if results.user_org:
	user_org = results.user_org


fr = open(inp_file, "r")
line_no = 0

all_lines = fr.read().splitlines()

print "Found " + str(len(all_lines)) + " PRs/commits in the file : " + inp_file + "\n"

print "Saving all files in directory : " + directory + "\n"

errors = 0

for pr_no in all_lines:
	print "Fetching PR no : " + pr_no
	line_no += 1

	url = "https://patch-diff.githubusercontent.com/raw/" \
		+ user_org + "/" + respository + "/pull/" + pr_no

	if results.patch:
		url = url + ".patch"
	else :
		url = url + ".diff"

	response = urllib2.urlopen(url)
	if not response :
		print "Error : Line number '" + line_no + "' gave an error"
		error += 1
		continue

	fh = open(directory + pr_no + ".diff", "w")
	fh.write(response.read())
	fh.close()

	print "Fetced PR number : " + pr_no
	if results.patch:
		print "Stored at " + directory + pr_no + ".patch" + "\n"
	else:
		print "Stored at " + directory + pr_no + ".diff" + "\n"

fr.close()

if errors > 0:
	print "Process completed with " + errors + "errors\n"
else :
	print "Process completed sucessfully\n"
