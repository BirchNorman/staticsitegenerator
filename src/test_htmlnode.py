import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
	def test_props(self):
		node = HTMLNode("tag", "value", ["children"], {"key1": "val1", "key2": "val2"})
		self.assertEqual(node.props_to_html(), " key1=\"val1\" key2=\"val2\"")
	def test_noprops(self):
		node = HTMLNode("tag", "value", ["children"])
		self.assertEqual(node.props_to_html(), "")
	def test_emptyprops(self):
		node = HTMLNode("tag", "value", ["children"], {})
		self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
	def test_leaf_to_html_a(self):
		node = LeafNode("a", "Hello, world!", {"href": "https"})
		self.assertEqual(node.to_html(), "<a href=\"https\">Hello, world!</a>")
	def test_leaf_to_html_novalue(self):
		node = LeafNode("p", None)
		with self.assertRaises(ValueError) as cm:
			node.to_html()
		self.assertEqual(str(cm.exception), "no value")
	def test_leaf_to_html_notag(self):
		node = LeafNode(None, "Hello, world!")
		self.assertEqual(node.to_html(), "Hello, world!")

class TestLeafNode(unittest.TestCase):
	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
	def test_to_html_nested(self):
		child_node = LeafNode("flag", "value")
		parent_node = ParentNode("flag", [child_node])
		grandparent_node = ParentNode("flag", [parent_node])
	def test_to_html_multichild(self):
		child_node1 = LeafNode("flag", "value")
		child_node2 = LeafNode("flag", "value")
		parent_node = ParentNode("flag", [child_node1, child_node2])
	def tset_to_html_nochildren(self):
		parent_node = ParentNode("flag", None)
		with self.assertRaises(ValueError) as cm:
			parent_node.to_html()
		self.assertEqual(str(cm.exception), "no children")
	def test_to_html_notag(self):
		child_node = LeafNode("flag", "value")
		parent_node = ParentNode(None, [child_node])
		with self.assertRaises(ValueError) as cm:
			parent_node.to_html()
		self.assertEqual(str(cm.exception), "no tag")
	def test_to_html_nochildvalue(self):
		child_node = LeafNode("flag", None)
		parent_node = ParentNode("flag", [child_node])
		with self.assertRaises(ValueError) as cm:
			parent_node.to_html()
		self.assertEqual(str(cm.exception), "no value")

if __name__ == "__main__":
	unittest.main()
