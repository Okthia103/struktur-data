import pandas as pd
from collections import deque
import time

class TreeNode:
    def __init__(self, value):  # Fix typo: change _init_ to __init__
        self.value = value
        self.children = []

def display_laptop_info(file_path):
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
        return None
    except UnicodeDecodeError:
        print(f"Tidak dapat membaca file '{file_path}' dengan encoding yang benar.")
        return None
    
    print("Nama-nama kolom yang tersedia:")
    print(df.columns.tolist())
    
    laptop_name = input("Masukkan nama laptop yang ingin dicari: ")
    
    laptop_info = df[df[['laptop_ID', 'Product', 'TypeName', 'Company']].isin([laptop_name]).any(axis=1)]  # Ganti 'Product' dengan 'TypeName' jika perlu
    
    if laptop_info.empty:
        print(f"Laptop dengan nama '{laptop_name}' tidak ditemukan.")
    else:
        print("Informasi laptop:")
        print(laptop_info)
    
    return df

def bfs_tree(root, target=None):
    if not root:
        return {
            "bfs": [],
            "operations": 0,
            "max_depth": 0,
            "execution_time": 0,
            "found": False
        }
    
    visited = set()
    queue = deque([(root, 0)])  # Store (node, depth)
    bfs = []
    operations = 0
    found = False
    max_depth = 0

    start_time = time.time()
    
    while queue:
        node, depth = queue.popleft()
        operations += 1
        if node not in visited:
            visited.add(node)
            bfs.append(node.value)
            if node.value == target:
                found = True
                break
            max_depth = max(max_depth, depth)
            queue.extend((child, depth + 1) for child in node.children if child not in visited)

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "bfs": bfs,
        "operations": operations,
        "max_depth": max_depth,
        "execution_time": execution_time,
        "found": found
    }

def main():
    file_path = "C:\\Users\\HP VICTUS\\OneDrive\\ドキュメント\\bismillah\\laptops.csv"
    df = display_laptop_info(file_path)
    
    if df is not None:
        root = TreeNode("root")  # Root node to hold all laptops
        laptop_nodes = {}

        for _, row in df.iterrows():
            laptop_id = str(row['laptop_ID'])  # Ensure IDs are strings
            screen_resolution = row['ScreenResolution']
            
            if laptop_id not in laptop_nodes:
                laptop_nodes[laptop_id] = TreeNode(laptop_id)
            
            if screen_resolution not in laptop_nodes:
                laptop_nodes[screen_resolution] = TreeNode(screen_resolution)
                root.children.append(laptop_nodes[screen_resolution])
            
            laptop_nodes[screen_resolution].children.append(laptop_nodes[laptop_id])

        search_again = input("Do you want to perform a BFS search? (y/n): ")
        if search_again.lower() == 'y':
            target_value = input("Enter the target laptop ID: ")
            result = bfs_tree(root, target_value)
            print("BFS:", result["bfs"])
            print("Number of Operations:", result["operations"])
            print("Max Depth of Search:", result["max_depth"])
            print("Execution Time (seconds):", result["execution_time"])
            print("Found Target Node:", result["found"])

if __name__ == "__main__":  # Fix typo: change _name_ to __name__
    main()
