# -*- coding: utf-8 -*-
# lenin.action module


def do_action(_: list) -> str:
    return "Sure...write some more code then I can do that!"


def ping_action(_: list) -> str:
    return 'PONG'


def hello_action(_: list) -> str:
    return 'Bot приветствует тебя!'


def eval_action(args: list) -> str:
    return eval(" ".join(args))

def self_upgrade(_: list) -> str:
    return 'start upgrade-bot task'


ALL = {
    'do': do_action,
    'ping': ping_action,
    'hello': hello_action,
    'eval': eval_action,
    'обновись': self_upgrade
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