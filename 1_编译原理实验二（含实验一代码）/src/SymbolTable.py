# 一个自定义的符号表
class SymbolTable:
    def __init__(self, namespace="root"):
        self.namespace = namespace  # 定义一个名字，方便后面debug

        self.children = []  # 每一个子作用域的符号表
        self.symbols = []  # 构建一个id_name和type的list
        self.parent = None  # 符号表的父节点

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def add_symbol(self, symbol):
        look_result = self.lookup(symbol)
        if look_result == "NOT FOUND":
            self.symbols.append(symbol)
            return
        elif look_result == "FOUND":
            print("错误：\tID \"" + symbol + "\" 在当前作用域多次定义！")
            exit(-1)
        elif look_result == "FOUND IN PARENT":
            print("警告：\tID \"" + symbol + "\" 在上级作用域已经被定义！")

    def lookup(self, symbol):
        """
        检查命名冲突，只会往上一级作用域查找！
        """
        if symbol in self.symbols:
            return "FOUND"  # 表示在当前作用域
        elif self.parent is not None:
            if self.parent.lookup(symbol) == "FOUND":  # 表示在上一级作用域
                return "FOUND IN PARENT"
        return "NOT FOUND"  # 表示找不到

    def check_namespace(self, type_list: list, type_name: str):
        if not self.lookup_namespace(type_list):
            print(type_name + " 未定义即使用！")
            exit(-1)

    def lookup_namespace(self, type_name: list):
        """
        检查未定义即使用，以及引用是否正确。自顶向下查找，只能由root节点进行！
        """
        if len(type_name) == 0:
            return True

        if self.namespace.endswith("root"):
            for child in self.children:
                if child.lookup_namespace(type_name):
                    return True
            return False

        else:
            if self.namespace.endswith(type_name[0]):
                type_name.pop(0)
                for child in self.children:
                    if child.lookup_namespace(type_name):
                        return True
                return False

    def display(self):
        print(self.namespace, end="\n\t")
        for symbol in self.symbols:
            print(symbol, end=" ")
        print()
        for child in self.children:
            child.display()
