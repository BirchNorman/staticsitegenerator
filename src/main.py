from textnode import *
import os
import shutil
from copystatic import *
from gencontent import *

path_to_static = "./static"
path_to_public = "./public"
path_to_content = "./content"

def main():
	# TextNodeObject = TextNode("text", "link", "https://www.boot.dev")
	# print(TextNodeObject)
	if os.path.exists(path_to_public):
		shutil.rmtree(path_to_public)			

main()
copy_static(path_to_static, path_to_public)
generate_pages_recursive(path_to_content, "template.html", path_to_public)

# generate_page("content/index.md", "template.html", "public/index.html")
# generate_page("content/blog/glorfindel/index.md", "template.html", "public/index.html")
# generate_page("content/blog/tom/index.md", "template.html", "public/index.html")
# generate_page("content/blog/majesty/index.md", "template.html", "public/index.html")
# generate_page("content/contact/index.md", "template.html", "public/index.html")