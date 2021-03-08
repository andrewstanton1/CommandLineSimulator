from collections import defaultdict

class Directory:
    def __init__(self):
        self.root = 'user'
        self.children = defaultdict(dict)
        self.children['user'] = { 'name': 'user', 'parent': None, 'children': defaultdict(dict), 'files': [] }
        self.stack = [self.children]

    def make_dir(self, name):
        if name not in self.children[self.root]['children']:
            self.children[self.root]['children'][name] = { 'name': name, 'parent': self.root, 'children': defaultdict(dict), 'files': [] }
            return 'Succeded'
        return 'Failed'

    def touch_cmd(self, name):
        if name not in self.children[self.root]['files']:
            self.children[self.root]['files'].append(name)
            return "created"
        return "already exists"

    def change_dir_sub(self, name):
        if name in self.children[self.root]['children']:
            self.stack.append(self.children[self.root]['children'])
            self.children = self.children[self.root]['children']
            self.root = name
        return self.root

    def change_dir_parent(self):
        if self.children[self.root]['parent']:
            self.root = self.children[self.root]['parent']
            self.stack.pop()
            self.children = self.stack[-1]
        return self.root

    def list_dir(self, r):
        if not r:
            for item in self.children[self.root]['children']:
                print(item)
            for item in self.children[self.root]['files']:
                print(item)
        else:
            self.recursive(self.children, self.root)

    def recursive(self, children, root):
        if children[root]:
            for item in self.children[self.root]['files']:
                print(item)
            for item in children[root]['children']:
                print(item)
                if children[root]['children'][item]['children']:
                    self.recursive(children[root]['children'], item)
    
class CommandLine:
    def __init__(self):
        self.directory = Directory()

    def mkdir(self, name):
        result = self.directory.make_dir(name)
        print(f'{ result } to create directory { name }')

    def cd(self, name):
        if name == '..':
            result = self.directory.change_dir_parent()
        else:
            result = self.directory.change_dir_sub(name)
        
        print(f'Current directory is now { result }')

    def ls(self, r=None):
        self.directory.list_dir(r)

    def touch(self, name):
        result = self.directory.touch_cmd(name)
        print(f'File { name } { result }')

if __name__ == '__main__':
    cl = CommandLine()
    cl.mkdir('folder1')
    cl.mkdir('folder2')
    cl.ls()
    cl.cd('folder1')
    cl.ls()
    cl.mkdir('folderA')
    cl.ls()
    cl.cd('..')
    cl.ls('-r')
    cl.touch('andy.txt')
    cl.ls()