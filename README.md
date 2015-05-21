#Yaml AST beautifier

The script `astdumper.py` contained in this repository pretty prints the AST trees used by [Quantified Code](https://www.quantifiedcode.com/).
They are representing the AST as a YAML documents.
But unfortunately the map elements within this YAML are unsorted which makes it hard to read the syntax trees.

## How to use

First install the following requirements:
  * Python 3
  * pyyaml (`pip install pyyaml`)

Run the script `astdumper.py`. It accepts the input on stdin. Alternatively you might specify a file name as first parameter.

## Integration with VIM

If you use VIM as your text editor, you can use the piping functionality using the following key sequence:

```
:%!astdumper.py
```

(assuming that astdumper.py is in your PATH environment variable)

## Usage with xsel

In order to pretty print an AST which is saved in the clipboard buffer, you might use the following bash command:

```
xsel -b | astdumper.py
```
