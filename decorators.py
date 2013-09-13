from functools import wraps

def ignore_msg_from_self(func):
    @wraps(func)
    def decorator(msg, args):
        if msg.getType() == "groupchat":
            if str(msg.getFrom()).split("/")[1] == 'PentaBot':
                return
        return func(msg, args)

    return decorator
