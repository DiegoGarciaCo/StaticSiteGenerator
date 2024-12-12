import unittest
from functions import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, block_to_block_type
from textnode import TextNode, TextType

class testFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_extract_markdown_images2(self):
        text = "this is "
        self.assertEqual(
            extract_markdown_images(text),
            []
        )

    def test_split_nodes_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("This is text with a ", TextType.TEXT, None), TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", TextType.TEXT, None), TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_split_nodes_images2(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and they're bangers.",TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with a ",
                TextType.TEXT, None),
                TextNode("rick roll", 
                TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
                TextNode(" and ", TextType.TEXT, None), 
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and they're bangers.", TextType.TEXT, None)
                
                ]
        )

    def test_split_nodes_images3(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", TextType.TEXT, None), TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_split_nodes_images4(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_split_node_images5(self):
        node = TextNode("only text no images", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("only text no images", TextType.TEXT)]
        )

    def test_split_nodes_links(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
                )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
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
        )

    def test_block_to_block_type(self):
        block = "# This is a heading"
        self.assertEqual(
            block_to_block_type(block),
            "heading"
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), "quote")
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")
    
if __name__ == "__main__":
    unittest.main()