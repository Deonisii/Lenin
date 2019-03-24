# lenin.action module


def do_action(_: list) -> str:
    return "Sure...write some more code then I can do that!"


def ping_action(_: list) -> str:
    return 'PONG'


def hello_action(worlds: list) -> str:
    return 'Bot приветствует тебя!'


def eval_action(args: list) -> str:
    return eval(" ".join(args))


ALL = {
    'do': do_action,
    'ping': ping_action,
    'hello': hello_action,
    'eval': eval_action
}

for greeting in (
    'hi',
    'привет',
    'shalom',
    'salam',
    'hey',
    'good'
):
    ALL[greeting] = hello_action