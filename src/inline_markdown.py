import re
from htmlnode import *
from textnode import *
from text_to_html import *
from copystatic import *
from itertools import zip_longest

def extract_markdown_images(text):
	tuples = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return tuples

def extract_markdown_links(text):
	tuples = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return tuples

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		elif node.text.count(delimiter) % 2 != 0:
			raise Exception("invalid syntax")
		else:
			split_nodes = []
			plain = []
			bold = []
			for part in node.text.split(delimiter)[::2]:
				plain.append(TextNode(part, TextType.TEXT))
			for part in node.text.split(delimiter)[1::2]:
				bold.append(TextNode(part, text_type))
			split_nodes = [x for xs in zip_longest(plain, bold) for x in xs]
			split_nodes_filtered = [node for node in split_nodes if node is not None]
			new_nodes.extend(split_nodes_filtered)
	return new_nodes
			
def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		split_nodes = []
		images = extract_markdown_images(node.text)
		if images == []:
			split_nodes.append(node)		
		else:
			plain_text = node.text
			for image in images:
				alt = image[0]
				lnk = image[1]
				txt = plain_text.split(f"![{alt}]({lnk})", 1)
				split_nodes.append(TextNode(txt[0], TextType.TEXT))
				plain_text = txt[1]
				split_nodes.append(TextNode(alt, TextType.IMAGE, lnk))
			if plain_text != "":
				split_nodes.append(TextNode(plain_text, TextType.TEXT))
		new_nodes.extend(split_nodes)
	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		split_nodes = []
		links = extract_markdown_links(node.text)
		if links == []:
			split_nodes.append(node)
		else:
			plain_text = node.text
			for link in links:
				anchr = link[0]
				lnk = link[1]
				txt = plain_text.split(f"[{anchr}]({lnk})", 1)
				split_nodes.append(TextNode(txt[0], TextType.TEXT))
				plain_text = txt[1]
				split_nodes.append(TextNode(anchr, TextType.LINK, lnk))
			if plain_text != "":
				split_nodes.append(TextNode(plain_text, TextType.TEXT))
		new_nodes.extend(split_nodes)
	return new_nodes

def text_to_textnodes(text):	
	nodes1 = [TextNode(text, TextType.TEXT)]
	nodes2 = split_nodes_delimiter(nodes1, "**", TextType.BOLD)
	nodes3 = split_nodes_delimiter(nodes2, "_", TextType.ITALIC)
	nodes4 = split_nodes_delimiter(nodes3, "`", TextType.CODE)
	nodes5 = split_nodes_image(nodes4)
	nodes6 = split_nodes_link(nodes5)
	return nodes6

def markdown_to_blocks(markdown):
	blocks = markdown.split("\n\n")
	cleaned_blocks = [block.strip() for block in blocks]
	filtered_blocks = list(filter(None, cleaned_blocks))
	return filtered_blocks

def block_to_block_type(block):
	if block[0] == "#" and " " in block and len(block.split(" ")) > 1 and len(block.split(" ", 1)) <= 6:
		return BlockType.HEADING
	elif block.strip().startswith("```") and block.strip().endswith("```"):
		return BlockType.CODE
	elif block[0] == ">" and len(block.split(">")) > 1 and len(block.split("> ")) > 1:
		quote = True
		for line in block:
			if block[0] != ">" or len(block.split(">")) <= 1 or len(block.split("> ")) <= 1:
				quote == False
		if quote == True:
			return BlockType.QUOTE
	elif block[:2] == "- ":
		unordered_list = True
		for line in block:
			if line[:2] != "- ":
				unordered_list == False
		if unordered_list == True:
			return BlockType.UNORDERED_LIST
	elif block[:3] == "1. ":
		ordered_list = True
		num = 1
		lines = block.split("\n")
		for line in lines:
			if line.split(". ", 1)[0] != num:
				ordered_list == False
			num += 1
		if ordered_list == True:
			return BlockType.ORDERED_LIST
	else:
		return BlockType.PARAGRAPH

def text_to_children(text):
	text_nodes = text_to_textnodes(text)
	children = []
	for text_node in text_nodes:
		child = text_node_to_html_node(text_node)
		children.append(child)
	return children

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	block_nodes = []
	for block in blocks:
		if block_to_block_type(block) == BlockType.HEADING:
			num = block.split(" ")[0].count("#")
			handled_block = block[num+1:]
			parent_node = ParentNode(f"h{num}", text_to_children(handled_block))
			block_nodes.append(parent_node)
		elif block_to_block_type(block) == BlockType.CODE:
			child_node = LeafNode("code", block[4:-3])
			parent_node = ParentNode("pre", [child_node])
			block_nodes.append(parent_node)	
			# print(f"block: {repr(block)}")
			# print(f"sliced: {repr(block[4:-3])}")
		elif block_to_block_type(block) == BlockType.QUOTE:
			lines = block.split("\n")
			stripped_lines = [line[2:] for line in lines]		
			handled_block = " ".join(stripped_lines)
			parent_node = ParentNode("blockquote", text_to_children(handled_block))
			block_nodes.append(parent_node)	
		elif block_to_block_type(block) == BlockType.UNORDERED_LIST:
			children = []
			for line in block.split("\n"):
				handled_line = line[2:]
				child_node = ParentNode("li", text_to_children(handled_line))
				children.append(child_node)
			parent_node = ParentNode("ul", children)
			block_nodes.append(parent_node)	
		elif block_to_block_type(block) == BlockType.ORDERED_LIST:
			children = []
			for line in block.split("\n"):
				handled_line = line.split(". ", 1)[1]
				child_node = ParentNode("li", text_to_children(handled_line))
				children.append(child_node)
			parent_node = ParentNode("ol", children)
			block_nodes.append(parent_node)	
		elif block_to_block_type(block) == BlockType.PARAGRAPH:
			handled_block = block.replace("\n", " ")
			parent_node = ParentNode("p", text_to_children(handled_block))
			block_nodes.append(parent_node)
	return ParentNode("div", block_nodes)

def extract_title(markdown):
	header = None
	for line in markdown.split("\n"):
		if line[:2] == "# ":
			header = line[2:].strip()
	if header == None:
		raise Exception("No h1 header")
	else:
		return header
	