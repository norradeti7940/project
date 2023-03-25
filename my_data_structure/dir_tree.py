from os import scandir, sep
from os.path import normpath, isdir, splitext
class DirTree:

    class Node:
        def __init__(self, name) -> None:
            self.name = name
            self.child : list[DirTree.Node] = []
            self.parent : DirTree.Node | None = None
            self.value = 0
            self.total = 0

        def __str__(self) -> str:
            return f'({self.name}, value {self.value}, total {self.total}, child {[c.name for c in self.child] if self.child else None})'

    def __init__ (self, dir : str, extension_filter : list[str] | None = None):
        if not isdir(dir):
            raise NotADirectoryError(f'the specified path ({dir}) is not a directory')
        self.extension_filter = extension_filter
        normalize_path_list = normpath(dir).split(sep)
        self.root = actual = self.Node(normalize_path_list[0])
        for f in normalize_path_list[1:]:
            temp = self.Node(f)
            temp.parent = actual
            actual.child.append(temp)
            actual = temp
        self.__search(dir, actual)
        self.relative = actual

    def __search(self, dir: str, node: Node):
        for f in scandir(dir):
            if isdir(f):
                temp = self.Node(f.name)
                temp.parent = node
                node.child.append(temp)
                self.__search(f.path, temp)
            if not self.extension_filter:
                node.value += 1
                node.total += 1
            else:
                extension = splitext(f.name)[1]
                if extension in self.extension_filter:
                    node.value += 1
                    node.total += 1
        actual = node
        while actual.parent:
            actual.parent.total += node.value
            actual = actual.parent

    def print(self, extended : bool = False) -> str:
        if extended:
            self.__print(self.root, 0)
        else:
            self.__print(self.relative, 0)

    def __print(self, node : Node, identation : int):
        tab='\t'
        print(f'{tab*identation}{node.name}: {node.value} {node.total}')
        if node.child:
            for n in node.child:
                self.__print(n,identation+1)

    def remove_empty_nodes(self, extended : bool = True):
        if extended:
            self.__remove_empty_nodes(self.root)
        else:
            self.__remove_empty_nodes(self.relative)

    def __remove_empty_nodes(self, node : Node):
        if node.child:
            for n in node.child.copy():
                if n.total == 0:
                    node.child.remove(n)
                    del n
                else:
                    self.__remove_empty_nodes(n)
    
    def __add__(self, val):
        print(val)
        return self

    def __iadd__(self, val):
        print('a')
        return self

    def __copy__(self):
        new = DirTree()
if __name__ == '__main__':
    a = DirTree(r'C:\Users\mysmu\OneDrive\Immagini\soos\zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz smista', ['.webp', '.png', '.jpg', '.jpeg', '.gif'])
    #a.print()
    a.remove_empty_nodes()
    a.print(True)