import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode
from functions import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", "italic", "google.com")
        node2 = TextNode("This is a text node", "italic", "google.com")

    def test_url_none(self):
        node = TextNode("This is a test node", "bold", None)
        self.assertNoLogs(node)


    def test_not_eq(self):
        node = TextNode("This is a text node","text")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node(self):
        text_node = TextNode("this is some text", TextType.BOLD)
        node = text_node_to_html_node(text_node)
        node2 = LeafNode("b", text_node.text)
        self.assertEqual(node, node2)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter2(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter3(self):
        node = TextNode("This is text with a *Italic phrase* in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("Italic phrase", TextType.ITALIC),
                TextNode(" in the middle", TextType.TEXT),
            ]
        )

if __name__ == "__main__":
    unittest.main()