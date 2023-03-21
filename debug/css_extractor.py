import re
import sys

def extract_css_selectors(file_path):
    with open(file_path, 'r') as css_file:
        content = css_file.read()
        
    # Remove comments
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    
    # Extract selectors
    selectors = re.findall(r'([^{]+){', content)
    
    # Clean up and split compound selectors
    cleaned_selectors = []
    for selector in selectors:
        cleaned_selector = selector.strip()
        if ',' in cleaned_selector:
            cleaned_selectors.extend(cleaned_selector.split(','))
        else:
            cleaned_selectors.append(cleaned_selector)
    
    return cleaned_selectors

def main():
    css_file_path = sys.argv[1]
    css_selectors = extract_css_selectors(css_file_path)
    
    print("CSS selectors found:")
    for selector in css_selectors:
        print(selector)

if __name__ == "__main__":
    main()