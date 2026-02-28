from textnode import *

class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError()
	
	def props_to_html(self):
		s = ""
		if self.props != None and self.props != {}:
			for prop in self.props:
				s += f" {prop}=\"{self.props[prop]}\""
		return s
	
	def __repr__(self):
		return f"tag={self.tag}\nvalue={self.value}\nchildren={self.children}\nprops={self.props}"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value == None:
			raise ValueError("no value")
		elif self.tag == None:
			return self.value
		else:
			return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

	def __repr__(self):
		return f"tag={self.tag}\nvalue={self.value}\nprops={self.props}"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag == None:
			raise ValueError("no tag")
		if self.children == None:
			raise ValueError("no children")
		else:
			result = ""
			for node in self.children:
				result += node.to_html()
			return f"<{self.tag}>{result}</{self.tag}>"