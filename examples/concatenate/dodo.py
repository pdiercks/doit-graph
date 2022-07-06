def task_create():
    def write_file(string, targets):
        with open(targets[0], "w") as fh:
            fh.write(string)

    for letter in "ab":
        yield {"name": letter, "actions": [(write_file, (f"content {letter}\n",))], "targets": [f"file_{letter}.txt"]}


def task_concatenate():
    return {"actions": ["cat %(dependencies)s > %(targets)s"], "file_dep": ["file_a.txt", "file_b.txt"], "targets": ["concatenated.txt"]}


def task_dograph():
    return {"actions": ["doit graph"], "targets": ["tasks.dot"]}


def task_dot():
    return {"actions": ["dot -Tpng %(dependencies)s -o %(targets)s"], "file_dep": ["tasks.dot"], "targets": ["tasks.png"]}
