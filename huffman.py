from Node import Node


def filter_uppercase_and_spaces(input_string: str) -> str:
    """
    Filters the input string to retain only uppercase letters and spaces.
    """
    return "".join(
        char for char in input_string.upper() if char.isalpha() or char == " "
    )


def count_frequencies(input_string: str) -> list[int]:
    """
    Counts the frequency of each uppercase letter in the input string.
    Returns a list of 26 integers, where index 0-25 correspond to 'A'-'Z'.
    Spaces are ignored here because we assume space is the most frequent
    and will always be in the tree.
    """
    frequencies: list[int] = [0] * 26
    for ch in input_string:
        if ch != " ":
            index = ord(ch) - ord("A")
            frequencies[index] = frequencies[index] + 1
    return frequencies


def initialize_forest(frequencies: list[int]) -> list[Node]:
    """
    Initializes a forest (list) of Node objects for each character with a non-zero frequency.
    Adds one Node for space (index 26) with a very large frequency to ensure
    it is placed optimally as the root branch.
    """
    forest: list[Node] = []

    # letters A–Z
    for i in range(26):
        if frequencies[i] > 0:
            symbol = chr(i + ord("A"))
            forest.append(Node(frequencies[i], symbol))

    # add space (index 26)
    space_freq = max(sum(frequencies), 1) 
    forest.append(Node(space_freq, " "))

    return forest


def get_smallest(forest: list[Node]) -> Node:
    """
    Remove and return the Node with the smallest frequency.
    """
    smallest_index: int = 0
    for i in range(1, len(forest)):
        if forest[i].get_frequency() < forest[smallest_index].get_frequency():
            smallest_index = i
    node: Node = forest[smallest_index]
    forest[:] = forest[:smallest_index] + forest[smallest_index + 1 :]
    return node


def build_huffman_tree(frequencies: list[int]) -> Node:
    """
    Builds the Huffman tree from the list of frequencies and returns the root Node.
    """
    forest: list[Node] = initialize_forest(frequencies)
    while len(forest) > 1:
        left: Node = get_smallest(forest)
        right: Node = get_smallest(forest)
        parent: Node = Node(left.get_frequency() + right.get_frequency())
        parent.set_left(left)
        parent.set_right(right)
        forest.append(parent)
    return forest[0]


def build_encoding_table(huffman_tree_root: Node) -> list[str]:
    """
    Builds the encoding table from the Huffman tree.
    Returns a list of 27 strings, where index 0-25 correspond to 'A'-'Z'
    and index 26 corresponds to space.
    """
    table: list[str] = [""] * 27

    def traverse(node: Node, prefix: str) -> None:
        if node.get_symbol() is not None:
            if node.get_symbol() == " ":
                table[26] = prefix
            else:
                index = ord(node.get_symbol()) - ord("A")
                table[index] = prefix
        else:
            traverse(node.get_left(), prefix + "0")
            traverse(node.get_right(), prefix + "1")

    traverse(huffman_tree_root, "")
    return table


def encode(input_string: str, encoding_table: list[str]) -> str:
    """
    Encodes the input string using the provided encoding table.
    """
    encoded: str = ""
    for ch in input_string:
        if ch == " ":
            encoded = encoded + encoding_table[26]
        else:
            index = ord(ch) - ord("A")
            encoded = encoded + encoding_table[index]
    return encoded


def decode(encoded_string: str, huffman_root: Node) -> str:
    """
    Decodes the encoded string using the Huffman tree as a key.
    """
    result: str = ""
    node: Node = huffman_root
    for bit in encoded_string:
        if bit == "0":
            node = node.get_left()
        else:
            node = node.get_right()
        if node.get_symbol() is not None:
            result = result + node.get_symbol()
            node = huffman_root
    return result


# ---------------------------
# Test Block
# ---------------------------
if __name__ == "__main__":
    text = "HELLO WORLD"
    filtered = filter_uppercase_and_spaces(text)
    print("Filtered:", filtered)

    freqs = count_frequencies(filtered)
    print("Frequencies:", freqs)

    tree = build_huffman_tree(freqs)
    table = build_encoding_table(tree)
    print("Encoding Table:", table)

    encoded = encode(filtered, table)
    print("Encoded:", encoded)

    decoded = decode(encoded, tree)
    print("Decoded:", decoded)
