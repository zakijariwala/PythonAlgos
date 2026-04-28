import os
import json
import re
import ast

def parse_python_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parsed = ast.parse(content)
    classes_data = []

    for node in ast.walk(parsed):
        if isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "complexity": None,
                "visualizable_points": [],
                "methods": []
            }
            
            if class_info["docstring"]:
                complexity_match = re.search(r'Time Complexity:\s*(O\(.*\))', class_info["docstring"])
                if complexity_match:
                    class_info["complexity"] = complexity_match.group(1)

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_source = ast.get_source_segment(content, item)
                    # Find visualizable points like: # [Visualizable Point: Name]
                    points = re.findall(r'#\s*\[Visualizable Point:\s*(.*?)\]', method_source)
                    if points:
                        class_info["visualizable_points"].extend(points)
                    class_info["methods"].append(item.name)
            
            classes_data.append(class_info)
            
    return classes_data

def main():
    repo_path = "python-algos"
    static_dir = "static"
    os.makedirs(static_dir, exist_ok=True)
    
    manifest = []
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                classes = parse_python_file(filepath)
                if classes:
                    manifest.append({
                        "file": file,
                        "path": filepath.replace(repo_path, '').lstrip('\\/'),
                        "classes": classes
                    })
                    
    output_path = os.path.join(static_dir, 'manifest.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest generated at {output_path}")

if __name__ == "__main__":
    main()
