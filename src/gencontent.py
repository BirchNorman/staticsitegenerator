import os
from inline_markdown import *
from pathlib import Path

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path) as f:
		markdown = f.read()
	with open(template_path) as f:
		template = f.read()
	html_node = markdown_to_html_node(markdown)
	content = html_node.to_html()
	title = extract_title(markdown)
	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", content)
	dir_path = os.path.dirname(dest_path)
	os.makedirs(dir_path, exist_ok=True)
	with open(dest_path, "w") as f:
		f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	for content in os.listdir(dir_path_content):
		from_path = os.path.join(dir_path_content, content)
		if os.path.isfile(from_path):
			if not from_path.endswith(".md"):
				continue
			md_file_path = os.path.join(dest_dir_path, content)
			path_object = Path(md_file_path)
			to_path = str(Path(path_object).with_suffix(".html"))
			generate_page(from_path, template_path, to_path)
			# print("GEN", from_path, "->", to_path)
		elif os.path.isdir(from_path):
			to_path = os.path.join(dest_dir_path, content)
			os.makedirs(to_path, exist_ok=True)
			# print("DIR", from_path, "->", to_path)
			generate_pages_recursive(from_path, template_path, to_path)