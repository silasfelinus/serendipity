import sys
import cssutils

def extract_css_selectors(file_path):
    css_selectors = []
    
    with open(file_path, 'r') as css_file:
        content = css_file.read()

    sheet = cssutils.parseString(content)
    
    for rule in sheet:
        if isinstance(rule, cssutils.css.CSSStyleRule):
            for selector in rule.selectorList:
                css_selectors.append(selector.selectorText)

    return css_selectors

def main():
    css_file_path = sys.argv[1]
    css_selectors = extract_css_selectors(css_file_path)

    print("CSS selectors found:")
    for selector in css_selectors:
        print(selector)

if __name__ == "__main__":
    main()