import unittest

from htmlnode import *
from textnode import *
from inline_markdown import *
from text_to_html import *

class TestSplitDelimiter(unittest.TestCase):
	def test_bold(self):
		node = TextNode("text1 **bold** text2", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(new_nodes, [TextNode("text1 ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text2", TextType.TEXT)])
	def test_italic(self):
		node = TextNode("text1 _italic_ text2", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
		self.assertEqual(new_nodes, [TextNode("text1 ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text2", TextType.TEXT)])			
	def test_code(self):
		node = TextNode("text1 `code` text2", TextType.TEXT)	
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(new_nodes, [TextNode("text1 ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" text2", TextType.TEXT)])		
	def test_nottextype(self):
		node = TextNode("**bold**", TextType.BOLD)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(new_nodes, [node])
	def test_nomatch(self):
		node = TextNode("text1 **bold text2", TextType.TEXT)
		with self.assertRaises(Exception) as cm:
			split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(str(cm.exception), "invalid syntax")
	def test_multi(self):
		node1 = TextNode("text1 **bold** text2", TextType.TEXT)
		node2 = TextNode("text3 **bold** text4", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
		self.assertEqual(new_nodes, 
			[
				TextNode("text1 ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text2", TextType.TEXT),
				TextNode("text3 ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text4", TextType.TEXT),
			]       
		)

class Test(unittest.TestCase):
	def test_split_images(self):
		node = TextNode("text ![alt1](https1) and ![alt2](https2)", TextType.TEXT)
		new_nodes = split_nodes_image([node])
		print(new_nodes)
		self.assertListEqual(
			[
				TextNode("text ", TextType.TEXT),
				TextNode("alt1", TextType.IMAGE, "https1"),
				TextNode(" and ", TextType.TEXT),
				TextNode("alt2", TextType.IMAGE, "https2"),
			],
				new_nodes,
			)
	def test_split_links(self):
		node = TextNode("text [anchor1](https1) and [anchor2](https2)", TextType.TEXT)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("text ", TextType.TEXT),
				TextNode("anchor1", TextType.LINK, "https1"),
				TextNode(" and ", TextType.TEXT),
				TextNode("anchor2", TextType.LINK, "https2"),
			],
				new_nodes,
                        )
	def test_split_imagesnotypes(self):
		node = TextNode("text", TextType.TEXT)
		new_nodes = split_nodes_image([node])
		self.assertListEqual([TextNode("text", TextType.TEXT)], new_nodes)
	def test_split_linkssnotypes(self):
		node = TextNode("text", TextType.TEXT)
		new_nodes = split_nodes_link([node])
		self.assertListEqual([TextNode("text", TextType.TEXT)], new_nodes)

class TestExtractImage(unittest.TestCase):
	def test_extract_markdown_image(self):
		matches = extract_markdown_images("text ![image](https)")
		self.assertListEqual([("image", "https")], matches)
	def test_extract_markdown_images(self):
		matches = extract_markdown_images("text ![image1](https1) and ![image2](https2)")
		self.assertListEqual([("image1", "https1"), ("image2", "https2")], matches) 
	def test_extract_markdown_link(self):
		matches = extract_markdown_links("text [link](https)")
		self.assertListEqual([("link", "https")], matches)
	def test_extract_markdown_links(self):
		matches = extract_markdown_links("text [link1](https1) and [link2](https2)")
		self.assertListEqual([("link1", "https1"), ("link2", "https2")], matches)
	def test_extract_markdown_imagesmix(self):
		matches = extract_markdown_images("text [link](https) and ![image](https)")
		self.assertListEqual([("image", "https")], matches)
	def test_extract_markdown_linksmix(self):
		matches = extract_markdown_links("text [link](https) and ![image](https)")
		self.assertListEqual([("link", "https")], matches)

class Test(unittest.TestCase):
	def test_text_to_textnodes(self):
		input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		output = [
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" and an ", TextType.TEXT),
				TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" and a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		self.assertEqual(text_to_textnodes(input), output)

class TestMarkdownToBlocks(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
# Heading

Paragraph

- ListItem1
- ListItem2
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"# Heading",
				"Paragraph",
				"- ListItem1\n- ListItem2",
			]
		)
			
	def test_markdown_to_blocks_excess(self):
		md = """
# Heading


Paragraph


- ListItem1
- ListItem2
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"# Heading",
				"Paragraph",
				"- ListItem1\n- ListItem2",
			]
		)

class TestBlockToBlockType(unittest.TestCase):
	def test_headings(self):
		block = "### heading text"
		function = block_to_block_type(block)
		self.assertEqual(function, BlockType.HEADING)

	def test_codes(self):
		block = "```\ncode```\n"
		function = block_to_block_type(block)
		self.assertEqual(function, BlockType.CODE)
	
	def test_quotes(self):
		block = ">quotetext\n> quotetext\n> quote text\n>quote text"
		function = block_to_block_type(block)
		self.assertEqual(function, BlockType.QUOTE)
	
	def test_unordered_list(self):
		block = "- text\n- "
		function = block_to_block_type(block)
		self.assertEqual(function, BlockType.UNORDERED_LIST)
	
	def test_ordered_list(self):
		block = "1. text\n2. "
		function = block_to_block_type(block)
		self.assertEqual(function, BlockType.ORDERED_LIST)

class TestMarkdownToHTMLNodes(unittest.TestCase):

	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

	"""
		
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
	"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)
	
class TestExtract_Title(unittest.TestCase):
	def test_extract_title_single_line(self):
		md = "# Title"
		title = extract_title(md)
		self.assertEqual(title, "Title")
	def test_extract_title_multi_line(self):
		md = """
# Title
"""
		title = extract_title(md)
		self.assertEqual(title, "Title")
	def test_extract_title_no_h1(self):
		md = "Title"
		with self.assertRaises(Exception) as cm: 
			title = extract_title(md)
		self.assertEqual(str(cm.exception), "No h1 header")

if __name__ == "__main__":
	unittest.main()