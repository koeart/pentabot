from functools import wraps

def ignore_msg_from_self(func):
    @wraps(func)
    def decorator(self, msg, args):
        if msg.getType() == "groupchat":
            if unicode(msg.getFrom().__str__()).split("/")[1] == u'PentaBot':
                return
        return func(self, msg, args)

    return decorator
