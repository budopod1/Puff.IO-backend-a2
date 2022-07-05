import traceback


def exec_admin(command, state):
    admin_globals = {
        "state": state,
        "users": state.users,
        "servers": state.servers
    }
    if state.servers and state.users:
        admin_globals = {
            "first_server": state.servers[0],
            "entities": state.servers[0].entities,
            "first_player": state.servers[0].entities[0]
        }
    try:
        exec(command, admin_globals)
    except Exception:
        print("Error in repl code:")
        print(traceback.format_exc())


def console(state):
    print("Admin Console")
    print("Type 'help' for help")
    repl_mode = False
    while True:
        if repl_mode:
            print("(repl mode)", end="")
        command = input(" >>> ")
        
        if repl_mode:
            if command == "/exit":
                repl_mode = False
                continue
            exec_admin(command, state)
            continue
        
        if command == "help":
            print("""
Admin Console Help

Start a Python instruction with a '/' to run it globals:
* state
* users
* servers
* first_server
* entities
* first_player
(Some may not be present if they do not exist)

repl - Start a Python repl (once in it, type '/exit' to exit)
            """)
        elif command == "repl":
            print("Type '/exit' to exit Python repl")
            repl_mode = True
        elif command.startswith("/"):
            exec_admin(command[1:], state)
        else:
            print("Invalid command")
        