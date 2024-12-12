from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        strings = node.text.split(delimiter)

        if len(strings) % 2 == 0:
            raise Exception("Incorrect markdown format: no closing delimeter")
        for i in range(len(strings)):
            if i % 2 == 0:
                split_nodes.append(TextNode(strings[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(strings[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            added_nodes = []
            parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)

            if parts[0] == "":
                added_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                remaining_text = parts[1]
            else:
                added_nodes.extend([TextNode(parts[0], TextType.TEXT), TextNode(image_alt, TextType.IMAGE, image_link)])
                remaining_text = parts[1]
            
            new_nodes.extend(added_nodes)

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for link in links:
            anchor = link[0]
            indv_link = link[1]
            added_nodes = []
            parts = remaining_text.split(f"[{anchor}]({indv_link})", 1)

            if parts[0] == "":
                added_nodes.append(TextNode(anchor, TextType.LINK, indv_link))
                remaining_text = parts[1]
            else:
                added_nodes.extend([TextNode(parts[0], TextType.TEXT), TextNode(anchor, TextType.LINK, indv_link)])
                remaining_text = parts[1]
            
            new_nodes.extend(added_nodes)

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        
        return new_nodes
    
def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    results = split_nodes_delimiter([node], "**", TextType.BOLD)
    results = split_nodes_delimiter(results,"*", TextType.ITALIC)
    results = split_nodes_delimiter(results, "`", TextType.CODE)
    results = split_nodes_image(results)
    return split_nodes_link(results)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"
        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_to_block_type(block)
        