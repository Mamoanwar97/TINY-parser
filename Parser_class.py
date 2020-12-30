from in_out import *
import pygraphviz as pgv


class Parser():
    def __init__(self, text):
        self.tokens = text
        self.token = self.tokens[0]
        self.index = 1
        self.count = 0
        self.Graph = pgv.AGraph()

    def get_token(self):
        if (self.index < len(self.tokens)):
            temp = self.index
            self.index = self.index + 1
            return self.tokens[temp]

    def ConnectHorizontal(self, firstNode, secondNode):
        self.Graph.subgraph(nbunch=[firstNode, secondNode], rank='same')
        self.Graph.add_edge(firstNode, secondNode)

    def match(self, expected_token):
        self.token = self.get_token()

    def factor(self):
        if (self.token == '('):
            self.match('(')
            ret = self.exp()
            self.match(')')
        else:
            temp = self.token
            self.match(self.token)
            self.Graph.add_node(self.count, label=temp)
            ret = self.Graph.get_node(self.count)
            self.count += 1
        return ret

    def term(self):
        temp = self.factor()
        while (self.token == '*' or self.token == '/'):
            # name = name + '1'
            self.Graph.add_node(self.count, label=self.token)
            parentnode = self.Graph.get_node(self.count)
            self.count += 1
            self.match(self.token)
            leftchild = temp
            rightchild = self.factor()
            self.Graph.add_edge(parentnode, leftchild)
            self.Graph.add_edge(parentnode, rightchild)  # rightchild
            temp = parentnode
        return temp

    def exp(self):
        temp = self.term()
        while (self.token == '+' or self.token == '-'):
            self.Graph.add_node(self.count, label=self.token)
            parentnode = self.Graph.get_node(self.count)
            self.count += 1
            self.match(self.token)
            leftchild = temp
            rightchild = self.term()
            self.Graph.add_edge(parentnode, leftchild)
            self.Graph.add_edge(parentnode, rightchild)  # rightchild
            temp = parentnode
        if (self.token == '<' or self.token == '>' or self.token == '='):
            self.Graph.add_node(self.count, label=self.token)
            parentnode = self.Graph.get_node(self.count)
            self.count += 1
            self.match(self.token)
            leftchild = temp
            rightchild = self.exp()
            self.Graph.add_edge(parentnode, leftchild)
            self.Graph.add_edge(parentnode, rightchild)
            return parentnode
        else:
            return temp

    def Read(self):
        self.match('read')
        if (isIdentfier(self.token)):
            self.Graph.add_node(self.count, label='read \n' + self.token, shape='rectangle')
            temp = self.Graph.get_node(self.count)
            self.count += 1
            self.match(self.token)
        return temp

    def Write(self):
        self.match('write')
        temp1 = self.exp()
        self.Graph.add_node(self.count, label='write', shape='rectangle')
        self.Graph.add_edge(self.count, temp1)
        temp = self.Graph.get_node(self.count)
        self.count += 1
        self.match(self.token)
        return temp

    def ifStatement(self):
        self.match('if')
        self.Graph.add_node(self.count, label='if', shape='rectangle')
        parentnode = self.Graph.get_node(self.count)
        self.count += 1
        leftchild = self.exp()
        self.Graph.subgraph(nbunch=[leftchild], rank='same')
        self.match('then')
        rightchild = self.stmtSeq()
        self.Graph.subgraph(nbunch=[leftchild, rightchild], rank='same')
        self.Graph.add_edge(leftchild, rightchild, color='white')
        self.Graph.add_edge(parentnode, leftchild)
        self.Graph.add_edge(parentnode, rightchild)
        if (self.token == 'else'):
            self.match('else')
            elsechild = self.stmtSeq()
            self.Graph.add_edge(parentnode, elsechild)
        self.match('end')
        return parentnode

    def repeat(self):
        self.match('repeat')
        self.Graph.add_node(self.count, label='repeat', shape='rectangle')
        parentnode = self.Graph.get_node(self.count)
        self.count += 1
        leftchild = self.stmtSeq()
        self.match('until')
        rightchild = self.exp()
        self.Graph.subgraph(nbunch=[rightchild], rank='same')
        self.Graph.add_edge(parentnode, leftchild)
        self.Graph.add_edge(parentnode, rightchild)
        return parentnode

    def assign(self):
        temp = self.exp()
        while (self.token == ':='):
            self.Graph.add_node(self.count, label=self.token)
            parentnode = self.Graph.get_node(self.count)
            self.count += 1
            self.match(self.token)
            leftchild = temp
            rightchild = self.exp()
            self.Graph.subgraph(nbunch=[leftchild, rightchild], rank='same')
            self.Graph.add_edge(leftchild, rightchild, color='white')
            self.Graph.add_edge(parentnode, leftchild)
            self.Graph.add_edge(parentnode, rightchild)  # rightchild
            temp = parentnode
        return temp

    def stmt(self):
        if self.token == 'read':
            temp = self.Read()
        elif self.token == 'write':
            temp = self.Write()
        elif self.token == 'if':
            temp = self.ifStatement()
        elif self.token == 'repeat':
            temp = self.repeat()
        else:
            temp = self.assign()
        return temp

    def stmtSeq(self):
        temp = self.stmt()
        temp1 = temp
        while (self.token == ';'):
            self.match(self.token)
            temp2 = self.stmt()
            self.ConnectHorizontal(temp1, temp2)
            temp1 = temp2
        return temp

    def run(self):
        self.stmtSeq()
        self.Graph.draw('SyntaxTree.png', prog='dot')