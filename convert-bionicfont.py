from bs4 import BeautifulSoup,NavigableString
import re 

# # Example HTML
# html = "<html><body><div><p>Hello world</p><p>Test</p></div><span>Leaf text</span></body></html>"

input_file = f"Middlemarch.xhtml"  # Replace with your HTML file
output_file = f"Middlemarch-bionic.xhtml"
with open(input_file, "r", encoding="utf-8") as f:
    html = f.read()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Function to identify leaf tags containing only navigable strings
def find_leaf_tags_with_string(tag):
    if isinstance(tag, str):  # If it's a string, it's a leaf
        return True
    # If it's a tag and has no child tags, it's a leaf with only string content
    return not tag.find_all(True)


# Traverse the tree and modify leaf tags with navigable strings
for tag in soup.body.find_all(True):  # Loop through all tags
    if find_leaf_tags_with_string(tag):
        # Modify the tag as needed (e.g., replace with a new <em> tag)
        if tag.string:
            modified_tag = soup.new_tag(tag.name)  # Create a new tag with same name
            modified_tag.attrs = tag.attrs # inherit all attributes
            s=tag.string.split()
            for long_word in s: # long_word is word with punctuation
                for word in re.findall( r'\w+|[^\s\w]+', long_word):
                    if len(word)>1:
                        halflen=len(word)//2
                        boldtag = soup.new_tag("b")
                        boldtag.string = word[:halflen]
                        modified_tag.append(boldtag)
                        modified_tag.append(NavigableString(f"{word[halflen:]}"))
                    elif len(word)==1:
                        modified_tag.append(NavigableString(word))
                modified_tag.append(NavigableString(" "))
            # modified_tag.string = tag.string  # Set the string of the original tag as the content
            tag.replace_with(modified_tag)  # Replace the original tag with the modified tag

# # Output the modified HTML
# print(soup.prettify())


with open(output_file, "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"Processed HTML saved to {output_file}")


