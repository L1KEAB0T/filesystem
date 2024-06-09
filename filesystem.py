import sys
import pickle
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QInputDialog, QTreeView, QSplitter, QLabel, QLineEdit, QFileDialog
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

class FileSystem:
    def __init__(self, size):
        self.size = size
        self.disk = [None] * size
        self.bitmap = [0] * size
        self.fat = [-1] * size
        self.root = {'type': 'dir', 'content': {}}
        self.current_dir = self.root
        self.current_path = ['/']
        self.open_files = {}

    def format(self):
        self.disk = [None] * self.size
        self.bitmap = [0] * self.size
        self.fat = [-1] * self.size
        self.root = {'type': 'dir', 'content': {}}
        self.current_dir = self.root
        self.current_path = ['/']
        self.open_files = {}

    def parse_path(self, path):
        parts = path.strip('/').split('/')
        dir = self.root
        for part in parts[:-1]:
            if part in dir['content'] and dir['content'][part]['type'] == 'dir':
                dir = dir['content'][part]
            else:
                return None, None
        return dir, parts[-1]

    def create_file(self, filename):
        dir, filename = self.parse_path(filename)
        if not dir:
            return "路径无效."
        if filename in dir['content']:
            return "文件已存在."
        for i in range(self.size):
            if self.bitmap[i] == 0:
                self.bitmap[i] = 1
                dir['content'][filename] = {'address': i, 'length': 0, 'type': 'file'}
                self.fat[i] = -1
                return "文件创建成功."
        return "磁盘空间不足."

    def open_file(self, filename):
        dir, filename = self.parse_path(filename)
        if not dir or filename not in dir['content']:
            return "文件不存在."
        if filename in self.open_files:
            return "文件已打开."
        self.open_files[filename] = dir['content'][filename]['address']
        return "文件打开成功."

    def close_file(self, filename):
        if filename not in self.open_files:
            return "文件未打开."
        del self.open_files[filename]
        return "文件关闭成功."

    def write_file(self, filename, data):
        if filename not in self.open_files:
            return "文件未打开."
        index = self.open_files[filename]
        for char in data:
            if index == -1:
                for i in range(self.size):
                    if self.bitmap[i] == 0:
                        self.bitmap[i] = 1
                        self.fat[index] = i
                        index = i
                        break
                else:
                    return "磁盘空间不足."
            self.disk[index] = char
            index = self.fat[index]
        self.current_dir['content'][filename]['length'] += len(data)
        return "数据写入成功."

    def read_file(self, filename):
        if filename not in self.open_files:
            return "文件未打开."
        index = self.open_files[filename]
        data = ''
        while index != -1:
            if self.disk[index] is not None:
                data += self.disk[index]
            index = self.fat[index]
        return data

    def delete_file(self, filename):
        dir, filename = self.parse_path(filename)
        if not dir or filename not in dir['content']:
            return "文件不存在."
        index = dir['content'][filename]['address']
        while index != -1:
            next_index = self.fat[index]
            self.bitmap[index] = 0
            self.disk[index] = None
            self.fat[index] = -1
            index = next_index
        del dir['content'][filename]
        if filename in self.open_files:
            del self.open_files[filename]
        return "文件删除成功."

    def create_directory(self, dirname):
        dir, dirname = self.parse_path(dirname)
        if not dir:
            return "路径无效."
        if dirname in dir['content']:
            return "目录已存在."
        dir['content'][dirname] = {'type': 'dir', 'content': {}}
        return "目录创建成功."

    def delete_directory(self, dirname):
        dir, dirname = self.parse_path(dirname)
        if not dir or dirname not in dir['content']:
            return "目录不存在."
        if dir['content'][dirname]['content']:
            return "目录不为空."
        del dir['content'][dirname]
        return "目录删除成功."

    def change_directory(self, dirname):
        parts = dirname.strip('/').split('/')
        dir = self.root

        # Handle absolute paths
        if dirname.startswith('/'):
            self.current_path = ['/']
            self.current_dir = self.root

        for part in parts:
            if part == '..':
                if len(self.current_path) > 1:
                    self.current_path.pop()
                    self.current_dir = self.root
                    for directory in self.current_path[1:]:
                        self.current_dir = self.current_dir['content'][directory]
            elif part == '' or part == '.':
                continue
            else:
                if part in self.current_dir['content'] and self.current_dir['content'][part]['type'] == 'dir':
                    self.current_dir = self.current_dir['content'][part]
                    self.current_path.append(part)
                else:
                    return "目录不存在."

        return "目录切换到 " + "/".join(self.current_path)

    def list_directory(self, directory=None, indent=0):
        if directory is None:
            directory = self.current_dir
        files = []
        for name, info in directory['content'].items():
            if info['type'] == 'dir':
                files.append('  ' * indent + f"{name}/")
                files.extend(self.list_directory(info, indent + 1))
            else:
                files.append('  ' * indent + f"{name} (地址: {info['address']}, 长度: {info['length']})")
        return files

    def save_to_disk(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.disk, self.bitmap, self.fat, self.root, self.current_path), f)

    def load_from_disk(self, filename):
        with open(filename, 'rb') as f:
            self.disk, self.bitmap, self.fat, self.root, self.current_path = pickle.load(f)
        self.current_dir = self.root
        for directory in self.current_path[1:]:
            self.current_dir = self.current_dir['content'][directory]

class FileSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fs = FileSystem(100)
        self.current_open_file = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('简单文件系统')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        self.path_display = QLineEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setText("/")

        button_layout = QHBoxLayout()

        self.create_file_btn = QPushButton('创建文件')
        self.create_file_btn.clicked.connect(self.create_file)
        button_layout.addWidget(self.create_file_btn)

        self.open_file_btn = QPushButton('打开文件')
        self.open_file_btn.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_file_btn)

        self.save_file_btn = QPushButton('保存文件')
        self.save_file_btn.clicked.connect(self.save_file)
        button_layout.addWidget(self.save_file_btn)

        self.close_file_btn = QPushButton('关闭文件')
        self.close_file_btn.clicked.connect(self.close_file)
        button_layout.addWidget(self.close_file_btn)

        self.delete_file_btn = QPushButton('删除文件')
        self.delete_file_btn.clicked.connect(self.delete_file)
        button_layout.addWidget(self.delete_file_btn)

        self.create_dir_btn = QPushButton('创建目录')
        self.create_dir_btn.clicked.connect(self.create_directory)
        button_layout.addWidget(self.create_dir_btn)

        self.delete_dir_btn = QPushButton('删除目录')
        self.delete_dir_btn.clicked.connect(self.delete_directory)
        button_layout.addWidget(self.delete_dir_btn)

        self.change_dir_btn = QPushButton('定位目录')
        self.change_dir_btn.clicked.connect(self.change_directory)
        button_layout.addWidget(self.change_dir_btn)

        self.go_back_btn = QPushButton('返回上一级')
        self.go_back_btn.clicked.connect(self.go_back)
        button_layout.addWidget(self.go_back_btn)

        self.save_fs_btn = QPushButton('保存文件系统')
        self.save_fs_btn.clicked.connect(self.save_file_system)
        button_layout.addWidget(self.save_fs_btn)

        self.load_fs_btn = QPushButton('加载文件系统')
        self.load_fs_btn.clicked.connect(self.load_file_system)
        button_layout.addWidget(self.load_fs_btn)

        splitter = QSplitter(Qt.Horizontal)
        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['名称', '地址', '长度'])
        self.tree_view.setModel(self.model)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)

        self.file_content = QTextEdit()

        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.file_content)
        splitter.addWidget(self.console)
        splitter.setSizes([200, 300, 300])

        main_layout.addWidget(self.path_display)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.update_tree_view()

    def update_tree_view(self):
        self.model.removeRows(0, self.model.rowCount())
        root_item = self.model.invisibleRootItem()
        self.build_tree(self.fs.root, root_item)
        self.path_display.setText("/".join(self.fs.current_path))

    def build_tree(self, directory, parent):
        for name, info in directory['content'].items():
            if info['type'] == 'dir':
                dir_item = QStandardItem(name + '/')
                parent.appendRow(dir_item)
                self.build_tree(info, dir_item)
            else:
                file_item = QStandardItem(name)
                address_item = QStandardItem(str(info['address']))
                length_item = QStandardItem(str(info['length']))
                parent.appendRow([file_item, address_item, length_item])

    def create_file(self):
        filename, ok = QInputDialog.getText(self, '创建文件', '输入文件名:')
        if ok:
            current_path = "/".join(self.fs.current_path) + '/' + filename
            result = self.fs.create_file(current_path)
            self.console.append(result)
            self.update_tree_view()

    def open_file(self):
        filename, ok = QInputDialog.getText(self, '打开文件', '输入文件名:')
        if ok:
            current_path = "/".join(self.fs.current_path) + '/' + filename
            result = self.fs.open_file(current_path)
            if "成功" in result:
                self.current_open_file = filename
                file_content = self.fs.read_file(filename)
                self.file_content.setText(file_content)
            self.console.append(result)

    def save_file(self):
        if self.current_open_file:
            content = self.file_content.toPlainText()
            result = self.fs.write_file(self.current_open_file, content)
            self.console.append(result)
            self.update_tree_view()
        else:
            self.console.append("没有打开的文件可以保存.")

    def close_file(self):
        if self.current_open_file:
            result = self.fs.close_file(self.current_open_file)
            self.console.append(result)
            self.file_content.clear()
            self.current_open_file = None
        else:
            self.console.append("没有打开的文件可以关闭.")

    def delete_file(self):
        filename, ok = QInputDialog.getText(self, '删除文件', '输入文件名:')
        if ok:
            current_path = "/".join(self.fs.current_path) + '/' + filename
            result = self.fs.delete_file(current_path)
            self.console.append(result)
            self.update_tree_view()

    def create_directory(self):
        dirname, ok = QInputDialog.getText(self, '创建目录', '输入目录名:')
        if ok:
            current_path = "/".join(self.fs.current_path) + '/' + dirname
            result = self.fs.create_directory(current_path)
            self.console.append(result)
            self.update_tree_view()

    def delete_directory(self):
        dirname, ok = QInputDialog.getText(self, '删除目录', '输入目录名:')
        if ok:
            current_path = "/".join(self.fs.current_path) + '/' + dirname
            result = self.fs.delete_directory(current_path)
            self.console.append(result)
            self.update_tree_view()

    def change_directory(self):
        dirname, ok = QInputDialog.getText(self, '更改目录', '输入目录名:')
        if ok:
            result = self.fs.change_directory(dirname)
            self.console.append(result)
            self.update_tree_view()

    def go_back(self):
        result = self.fs.change_directory('..')
        self.console.append(result)
        self.update_tree_view()

    def save_file_system(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "保存文件系统", "", "Pickle Files (*.pkl)")
        if save_path:
            self.fs.save_to_disk(save_path)
            self.console.append(f"文件系统保存到 {save_path}")

    def load_file_system(self):
        load_path, _ = QFileDialog.getOpenFileName(self, "加载文件系统", "", "Pickle Files (*.pkl)")
        if load_path:
            self.fs.load_from_disk(load_path)
            self.console.append(f"文件系统从 {load_path} 加载")
            self.update_tree_view()

    def closeEvent(self, event):
        self.save_file_system()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileSystemGUI()
    ex.show()
    sys.exit(app.exec_())
