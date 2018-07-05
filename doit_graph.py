import pygraphviz

from doit.cmd_base import DoitCmdBase
from doit.control import TaskControl


opt_subtasks = {
    'name': 'subtasks',
    'short': '',
    'long': 'show-subtasks',
    'type': bool,
    'default': False,
    'help': 'include subtasks in graph',
}


class GraphCmd(DoitCmdBase):
    doc_purpose = "create task's dependency-graph image"

    cmd_options = (opt_subtasks, )


    def node(self, task_name):
        """get graph node that should represent for task_name

        :param task_name:
        """
        if self.subtasks:
            return task_name
        task = self.tasks[task_name]
        return task.subtask_of or task_name


    def add_edge(self, src_name, sink_name, arrowhead):
        source = self.node(src_name)
        sink = self.node(sink_name)
        if source != sink and (source, sink) not in self._edges:
            self._edges.add((source, sink))
            self.graph.add_edge(source, sink, arrowhead=arrowhead)


    def _execute(self, subtasks):
        # init
        control = TaskControl(self.task_list)
        self.tasks = control.tasks
        self.subtasks = subtasks
        self._edges = set() # used to avoid adding same edge twice

        # create graph
        self.graph = pygraphviz.AGraph(strict=False, directed=True)
        self.graph.node_attr['color'] = 'lightblue2'
        self.graph.node_attr['style'] = 'filled'

        # populate graph
        for task in control.tasks.values():

            # add nodes
            node_attrs = {}
            if task.has_subtask:
                node_attrs['peripheries'] = '2'
            if (not task.subtask_of) or subtasks:
                self.graph.add_node(task.name, **node_attrs)

            # add edges
            for sink_name in task.setup_tasks:
                self.add_edge(task.name, sink_name, arrowhead='empty')
            for sink_name in task.task_dep:
                self.add_edge(task.name, sink_name, arrowhead='')

        self.graph.write('tasks.dot')

