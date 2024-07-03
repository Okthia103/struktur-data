import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QFileDialog, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
)
from collections import deque
import time

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

class LaptopSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('laptops.csv', encoding='latin-1')  # Preload the CSV file
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Laptop Search App')
        
        # Layouts
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        delete_layout = QHBoxLayout()
        bfs_layout = QHBoxLayout()
        results_layout = QVBoxLayout()
        
        # Laptop search
        self.search_input = QLineEdit()
        self.search_btn = QPushButton('Search Laptop')
        self.search_btn.clicked.connect(self.search_laptop)
        search_layout.addWidget(QLabel('Laptop Name:'))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        
        # Laptop delete
        self.delete_btn = QPushButton('Delete Laptop')
        self.delete_btn.clicked.connect(self.delete_laptop)
        delete_layout.addWidget(self.delete_btn)
        
        # BFS button
        self.bfs_btn = QPushButton('Perform BFS')
        self.bfs_btn.clicked.connect(self.perform_bfs)
        bfs_layout.addWidget(self.bfs_btn)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        # Adding layouts to main layout
        main_layout.addLayout(search_layout)
        main_layout.addLayout(delete_layout)
        main_layout.addLayout(bfs_layout)
        main_layout.addLayout(results_layout)
        
        # Setting the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    def search_laptop(self):
        self.results_text.clear()  # Clear previous results
        laptop_name = self.search_input.text()
        laptop_info = self.df[self.df[['Product', 'TypeName', 'Company']].isin([laptop_name]).any(axis=1)]
        
        if laptop_info.empty:
            self.results_text.append(f"Laptop with name '{laptop_name}' not found.")
        else:
            self.results_text.append(f"Laptop Information:\n{laptop_info.to_string(index=False)}")
        
        # Auto-populate the delete_input field with the searched laptop name
        self.search_input.setText(laptop_name)
    
    def delete_laptop(self):
        self.results_text.clear()  # Clear previous results
        laptop_name = self.search_input.text()
        
        mask = self.df[['Product', 'TypeName', 'Company']].apply(lambda x: x.str.contains(laptop_name, case=False, na=False))
        before_deletion = self.df.shape[0]
        self.df = self.df[~mask.any(axis=1)]
        after_deletion = self.df.shape[0]
        
        
        # Clear the search_input field after deletion
        self.search_input.clear()
    
    def perform_bfs(self):
        self.results_text.clear()  # Clear previous results
        root = TreeNode("root")
        laptop_nodes = {}
        
        for _, row in self.df.iterrows():
            laptop_id = str(row['Product'])
            screen_resolution = row['ScreenResolution']
            
            if laptop_id not in laptop_nodes:
                laptop_nodes[laptop_id] = TreeNode(laptop_id)
            
            if screen_resolution not in laptop_nodes:
                laptop_nodes[screen_resolution] = TreeNode(screen_resolution)
                root.children.append(laptop_nodes[screen_resolution])
            
            laptop_nodes[screen_resolution].children.append(laptop_nodes[laptop_id])
        
        result = self.bfs_tree(root)
        
        self.results_text.append(f"BFS: {', '.join(result['bfs'])}")
        self.results_text.append(f"Number of Operations: {result['operations']}")
        self.results_text.append(f"Max Depth of Search: {result['max_depth']}")
        self.results_text.append(f"Execution Time (seconds): {result['execution_time']:.6f}")
        self.results_text.append(f"Found Target Node: {result['found']}")
    
    def bfs_tree(self, root, target=None):
        if not root:
            return {
                "bfs": [],
                "operations": 0,
                "max_depth": 0,
                "execution_time": 0,
                "found": False
            }
        
        visited = set()
        queue = deque([(root, 0)])
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
    app = QApplication(sys.argv)
    ex = LaptopSearchApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
