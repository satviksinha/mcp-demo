from fastmcp import FastMCP
from todo_db import TodoDB
from typing import Annotated,NamedTuple

mcp = FastMCP('TODO_MCP')

todo_db = TodoDB('/Users/sinhasatvik/Desktop/mcp-demo/todo_tasks.json')
# todo_db.sample_data()

class Todo(NamedTuple):
    file_name:Annotated[str,'source file name containing the #TODO']
    line_number:Annotated[int,'line number of the #TODO comment from the source file']
    todo_text:Annotated[str,'the #TODO text to add']

@mcp.tool(
        name='mcp_add_todo',
        description='Add a single #TODO text from the source file',
)
def add_todo(file_name:Annotated[str,'source file name containing the #TODO'],
             line_number:Annotated[int,'line number of the #TODO comment from the source file'],
             todo_text:Annotated[str,'the #TODO text to add']):
    return todo_db.add(file_name,todo_text,line_number)

@mcp.tool(
        name='mcp_add_todos',
        description='Add multiple #TODO texts from source files in a single call. Returns the number of #TODO texts added',
)
def add_todos(
        todos: list[Todo]
):
    for todo in todos:
        todo_db.add(todo.file_name,todo.line_number,todo.todo_text)
    return len(todos)

@mcp.resource(
        name='mcp_get_todos_for_file',
        description='Get all #TODO texts for a given source file. Returns an empty array if source file doesnt exist or there are no #TODO texts in the file',
        uri="todo://{file_name}/todos",
)
def get_todos_for_file(file_name:Annotated[str,'source file name containing the #TODO']) -> list[str]:
    todos = todo_db.get(file_name)
    return [text for text in todos.values()]

def run():
    mcp.run()

if __name__ == '__main__':
    run()