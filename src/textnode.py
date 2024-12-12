from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text 
        self.text_type = text_type
        self.url = url

    def __eq__(self, node_two):
        if self.text == node_two.text and self.text_type == node_two.text_type and self.url == node_two.url:
            return True
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        text_node = LeafNode(None, text_node.text)
        return text_node
    elif text_node.text_type == TextType.BOLD:
        text_node = LeafNode("b", text_node.text)
        return text_node
    elif text_node.text_type == TextType.ITALIC:
        text_node = LeafNode("i", text_node.text)
        return text_node
    elif text_node.text_type == TextType.CODE:
        text_node = LeafNode("code", text_node.text)
        return text_node
    elif text_node.text_type == TextType.LINK:
        text_node = LeafNode("a", text_node.text)
        return text_node
    elif text_node.text_type == TextType.IMAGE:
        text_node = LeafNode("img", text_node.text)
        return text_node
    raise ValueError("Not a valid text node")
    

    
