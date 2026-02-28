import unittest

def test_text(self):
	node = TextNode("text", TextType.TEXT)
	html_node = text_node_to_html_node(node)
	self.assertEqual(html_node.tag, None)
	self.assertEqual(html_node.value, "Text")

def test_bold(self):
	node = TextNode("text", TextType.BOLD)
	html_node = text_node_to_html_node(node)
	self.assertEqual(html_node.tag, "b")
	self.assertEqual(html_node.value, "text")

def test_itallic(self):
	node = TextNode("text", TextType.ITALIC)
	html_node = text_node_to_html_node(node)
	self.assertEqual(html_node.tag, "i") 
	self.assertEqual(html_node.value, "text")

def test_code(self):
	node = TextNode("text", TextType.CODE)
	html_node = text_node_to_html_node(node)
	self.assertEqual(html_node.tag, "code")
	self.assertEqual(html_node.value, "text")

def test_link(self):
	node = TextNode("anchor", TextType.LINK, "url")
	html_node = text_node_to_html_node(node)
	self.assertEqual(html_node.tag, "a")
	self.assertEqual(html_node.value, "anchor")
	self.assertEqual(html_node.props, {"href": "url"})

def test_image(self):
	node = TextNode("image", TextType.LINK, "url")
	html_node = text_node_to_html_node(node)
	self.assertEqual(html_node.tag, "img")
	self.assertEqual(html_node.value, "")
	self.assertEqual(html_node.props, {"src": "url", "alt": "text"})

if __name__ == "__main__":
	unittest.main()
