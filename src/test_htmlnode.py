import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_node(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node2.props,
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph of text.</p>"
            )
        self.assertEqual(
            node2.to_html(), 
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_parent_to_html(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        leaf3 = LeafNode("i", "italic text")
        leaf4 = LeafNode(None, "Normal text")
        node = ParentNode(
            "p",
            [
                leaf1,
                leaf2,
                leaf3,
                leaf4,
            ],
        )
        self.assertEqual(
           node.to_html(), 
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_mutiple_node_test(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        leaf3 = LeafNode("i", "italic text")
        leaf4 = LeafNode(None, "Normal text")
        node = ParentNode(
            "div",
            [
                leaf1,
                leaf2,
                leaf3,
                leaf4,
            ],
        )
        node2 = ParentNode(
            "div",
            [
                leaf1,
                leaf2,
                node,
                leaf3,
                leaf4  
            ]
        )
        self.assertEqual(
            node2.to_html(),
            "<div><b>Bold text</b>Normal text<div><b>Bold text</b>Normal text<i>italic text</i>Normal text</div><i>italic text</i>Normal text</div>"            
                         )
        
    def test_mutiple_node_test_props(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        leaf3 = LeafNode("i", "italic text")
        leaf4 = LeafNode(None, "Normal text")
        node = ParentNode(
            "div",
            [
                leaf1,
                leaf2,
                leaf3,
                leaf4,
            ],
        )
        node2 = ParentNode(
            "div",
            [
                leaf1,
                leaf2,
                node,
                leaf3,
                leaf4  
            ],
            {"class": "flex justify-center items-center"}
        )
        self.assertEqual(
            node2.to_html(),
            '<div class="flex justify-center items-center"><b>Bold text</b>Normal text<div><b>Bold text</b>Normal text<i>italic text</i>Normal text</div><i>italic text</i>Normal text</div>'            
                         )
    
    def test_mutiple_node_test_prop(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        leaf3 = LeafNode("i", "italic text")
        leaf4 = LeafNode(None, "Normal text")
        node = ParentNode(
            "div",
            [
                leaf1,
                leaf2,
                leaf3,
                leaf4,
            ],
            {"class": "flex justify-center items-center"}
        )
        node2 = ParentNode(
            "div",
            [
                leaf1,
                leaf2,
                node,
                leaf3,
                leaf4  
            ],
            {"class": "flex justify-center items-center"}
        )
        self.assertEqual(
            node2.to_html(),
            '<div class="flex justify-center items-center"><b>Bold text</b>Normal text<div class="flex justify-center items-center"><b>Bold text</b>Normal text<i>italic text</i>Normal text</div><i>italic text</i>Normal text</div>'            
                         )
    


if __name__ == "__main__":
    unittest.main()