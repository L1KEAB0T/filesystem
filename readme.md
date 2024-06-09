# 简单文件系统 (Simple File System)

## 简介

这是一个使用 PyQt5 构建的简单文件系统 GUI 应用程序。它模拟了一个基本的文件系统，支持创建、删除、打开、关闭、写入、读取文件，创建和删除目录，以及保存和加载文件系统的状态。

## 功能

- **创建文件**: 在当前目录下创建一个新文件。
- **打开文件**: 打开一个文件以便读取或写入。
- **保存文件**: 将当前打开文件的内容写入到文件系统中。
- **关闭文件**: 关闭当前打开的文件。
- **删除文件**: 删除当前目录下的一个文件。
- **创建目录**: 在当前目录下创建一个新目录。
- **删除目录**: 删除当前目录下的一个目录（如果目录为空）。
- **更改目录**: 切换到指定目录。
- **返回上一级**: 切换到当前目录的上一级目录。
- **保存文件系统**: 将当前文件系统的状态保存到磁盘上。
- **加载文件系统**: 从磁盘上加载文件系统的状态。

## 依赖

- Python 3.x
- PyQt5
- pickle

## 安装与运行

1. 安装 Python 3.x，并确保 `pip` 已安装。
2. 安装 PyQt5:
    ```bash
    pip install PyQt5
    ```
3. 下载或克隆项目代码。

4. 运行程序:
    ```bash
    python filesystem.py
    ```

## 界面说明

### 文件系统界面

- **路径显示**: 显示当前目录路径。

    ![路径显示](https://github.com/L1KEAB0T/filesystem/blob/master/images/image-20240609112440188-171790348117410.png)

    ![image-20240609112440188](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609112440188-171790348117410.png)

- **控制台**: 显示文件系统操作的结果和信息。

    ![image-20240609112429459](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609112429459-17179034704319.png)

- **文件树视图**: 显示文件系统的目录结构。

    ![image-20240609112409218](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609112409218-17179034503057.png)

- **文件内容**: 显示和编辑当前打开文件的内容。

    ![image-20240609112510390](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609112510390-171790351147011.png)

- **操作按钮**:

## 操作说明

### 创建文件
1. 点击“创建文件”按钮。

2. 在弹出的对话框中输入文件名并点击“确定”。

3. 控制台显示创建结果。

   ![image-20240609111944943](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609111944943-17179031865051.png)

### 打开文件
1. 点击“打开文件”按钮。

2. 在弹出的对话框中输入文件名并点击“确定”。

3. 如果文件成功打开，其内容会显示在右侧的文本编辑框中。

   ![image-20240609112006017](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609112006017-17179032070462.png)

### 保存文件
1. 在文本编辑框中输入或修改文件内容。

2. 点击“保存文件”按钮。

3. 控制台显示保存结果。

   ![image-20240609112034046](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609112034046-17179032351383.png)

### 关闭文件
1. 点击“关闭文件”按钮。
2. 控制台显示关闭结果，并清空文本编辑框。

### 删除文件
1. 点击“删除文件”按钮。
2. 在弹出的对话框中输入文件名并点击“确定”。
3. 控制台显示删除结果。

### 创建目录
1. 点击“创建目录”按钮。

2. 在弹出的对话框中输入目录名并点击“确定”。

3. 控制台显示创建结果。

   ![image-20240609112110319](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609112110319-17179032714054.png)

### 删除目录
1. 点击“删除目录”按钮。
2. 在弹出的对话框中输入目录名并点击“确定”。
3. 控制台显示删除结果。

### 定位目录
1. 点击“更改目录”按钮。

2. 在弹出的对话框中输入目录名并点击“确定”（目录名称例如/1/1.1）。

3. 控制台显示更改结果，路径显示更新。

   ![image-20240609112129501](D:\大学学习\大二下\操作系统\filesystem\images\image-20240609112129501-17179032916175-17179032994906.png)

### 返回上一级
1. 点击“返回上一级”按钮。
2. 控制台显示更改结果，路径显示更新。

### 保存文件系统
1. 点击“保存文件系统”按钮。
2. 在弹出的文件对话框中选择保存路径并点击“保存”。
3. 控制台显示保存结果。

### 加载文件系统
1. 点击“加载文件系统”按钮。
2. 在弹出的文件对话框中选择文件并点击“打开”。
3. 控制台显示加载结果，文件树视图更新。

## 设计方案

### 1. 设计目标

设计一个简单的文件系统 GUI 应用，能够模拟文件系统的基本操作，包括文件和目录的创建、删除、打开、关闭、写入、读取，以及保存和加载文件系统状态。

### 2. 系统架构

系统架构分为文件系统逻辑层和用户界面层。

- **文件系统逻辑层**：负责文件系统的核心操作，包括文件和目录的管理、文件内容的读写、磁盘空间的分配和释放。
- **用户界面层**：提供图形用户界面，供用户执行文件系统操作并查看操作结果。

### 3. 模块设计

#### 3.1 文件系统逻辑层

- **FileSystem 类**
  - 属性：
    - `size`: 文件系统的总大小。
    - `disk`: 模拟磁盘存储，存储文件内容。
    - `bitmap`: 位图，记录磁盘块的使用情况。
    - `fat`: 文件分配表，记录文件的链表结构。
    - `root`: 根目录，存储文件和目录的树形结构。
    - `current_dir`: 当前目录。
    - `current_path`: 当前路径。
    - `open_files`: 打开文件的字典，记录已打开文件的地址。
  - 方法：
    - `format()`: 格式化文件系统。
    - `parse_path(path)`: 解析路径，返回目录和文件/目录名。
    - `create_file(filename)`: 创建文件。
    - `open_file(filename)`: 打开文件。
    - `close_file(filename)`: 关闭文件。
    - `write_file(filename, data)`: 向文件写入数据。
    - `read_file(filename)`: 读取文件内容。
    - `delete_file(filename)`: 删除文件。
    - `create_directory(dirname)`: 创建目录。
    - `delete_directory(dirname)`: 删除目录。
    - `change_directory(dirname)`: 切换目录。
    - `list_directory(directory, indent)`: 列出目录内容。
    - `save_to_disk(filename)`: 保存文件系统状态到磁盘。
    - `load_from_disk(filename)`: 从磁盘加载文件系统状态。

#### 3.2 用户界面层

- **FileSystemGUI 类**
  - 属性：
    - `fs`: 文件系统对象。
    - `current_open_file`: 当前打开文件的名称。
  - 方法：
    - `initUI()`: 初始化用户界面。
    - `update_tree_view()`: 更新文件树视图。
    - `build_tree(directory, parent)`: 构建文件树。
    - `create_file()`: 创建文件。
    - `open_file()`: 打开文件。
    - `save_file()`: 保存文件。
    - `close_file()`: 关闭文件。
    - `delete_file()`: 删除文件。
    - `create_directory()`: 创建目录。
    - `delete_directory()`: 删除目录。
    - `change_directory()`: 更改目录。
    - `go_back()`: 返回上一级目录。
    - `save_file_system()`: 保存文件系统。
    - `load_file_system()`: 加载文件系统。
    - `closeEvent(event)`: 处理窗口关闭事件，自动保存文件系统。

### 4. 详细设计

#### 4.1 文件系统逻辑层

- **文件创建**
  - 检查路径是否有效。
  - 检查文件是否已存在。
  - 分配一个空闲块，更新位图和文件分配表。
  - 在目录树中添加文件节点。

- **文件打开**
  - 检查路径是否有效。
  - 检查文件是否存在。
  - 将文件加入打开文件列表。

- **文件写入**
  - 检查文件是否已打开。
  - 根据文件分配表写入数据，分配新的块（如有需要）。

- **文件读取**
  - 检查文件是否已打开。
  - 根据文件分配表读取数据。

- **文件删除**
  - 检查路径是否有效。
  - 检查文件是否存在。
  - 更新位图和文件分配表，释放块。
  - 从目录树中删除文件节点。

- **目录创建**
  - 检查路径是否有效。
  - 检查目录是否已存在。
  - 在目录树中添加目录节点。

- **目录删除**
  - 检查路径是否有效。
  - 检查目录是否存在。
  - 检查目录是否为空。
  - 从目录树中删除目录节点。

#### 4.2 用户界面层

- **初始化用户界面**
  - 设置窗口标题和大小。
  - 创建和布局控件（按钮、文本框、树视图、文本编辑框）。
  - 连接按钮事件和相应的方法。

- **文件操作**
  - 调用文件系统逻辑层的方法执行文件操作。
  - 更新控制台显示操作结果。
  - 更新文件树视图。

- **目录操作**
  - 调用文件系统逻辑层的方法执行目录操作。
  - 更新控制台显示操作结果。
  - 更新文件树视图。

- **文件系统状态保存和加载**
  - 调用文件系统逻辑层的方法执行状态保存和加载。
  - 更新控制台显示操作结果。
  - 更新文件树视图。

### 5. 总结

该设计方案涵盖了文件系统的基本功能和用户界面的设计。文件系统逻辑层负责核心的文件和目录管理，用户界面层通过图形界面与用户交互，实现文件系统操作的可视化。两者通过明确的接口进行交互，保证了代码的模块化和可维护性。

## 注意事项

- 程序在关闭时会自动询问是否保存文件系统的状态。
- 文件系统的最大大小为 100 个块，可以根据需要调整。
- 文件系统保存在 `.pkl` 文件中。

## 联系方式

如果有任何问题或建议，请联系 [2251324@tongji.edu.cn]。