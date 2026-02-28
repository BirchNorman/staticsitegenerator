from textnode import *
import os
import shutil
from copystatic import *
from gencontent import *
import sys

path_to_static = "./static"
path_to_docs = "./docs"
path_to_content = "./content"

def main():
	# TextNodeObject = TextNode("text", "link", "https://www.boot.dev")
	# print(TextNodeObject)
	if os.path.exists(path_to_docs):
		shutil.rmtree(path_to_docs)			

main()
copy_static(path_to_static, path_to_docs)

basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]

generate_pages_recursive(path_to_content, "template.html", path_to_docs, basepath)
