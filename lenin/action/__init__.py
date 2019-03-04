# lenin.action module

def do_action(_: list) -> str:
    return "Sure...write some more code then I can do that!"

def ping_action(_: list) -> str:
    return 'PONG'

def eval_action(args: list) -> str:
    return eval(" ".join(args))

ALL = {
    'do' : do_action,
    'ping': ping_action,
    'eval': eval_action
}
