import argparse
import os
import re
import sys

import frontmatter
import jupytext
from slugify import slugify


parser = argparse.ArgumentParser(description="CLI tool for converting .ipynb file to markdown")
parser.add_argument("--filename",
                    help="Name of your ipynb file to convert")

if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])
    filename = args.filename

    notebook = jupytext.read(filename)
    nb_str = jupytext.writes(notebook, fmt='md')
    metadata, content = frontmatter.parse(nb_str)

    if metadata['jupyter']:
        content = re.sub("(<!--.*?-->)", "", content, flags=re.DOTALL)
        blog_meta, _ = frontmatter.parse(content)
        print(blog_meta)
        print(content)
        print([f for f in os.listdir('.')])
        with open(f'{slugify(blog_meta["title"])}.md', 'w') as fw:
            fw.write(content)