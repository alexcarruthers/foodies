from functools import wraps

def disable_for_loaddata(signal_handler):
    '''
    Prevents fixtures from triggering post-save signals.

    http://stackoverflow.com/questions/3499791/how-do-i-prevent-fixtures-from-conflicting-with-django-post-save-signal-code
    '''
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            print "Skipping signal for %s %s" % (args, kwargs)
            return
        signal_handler(*args, **kwargs)

    return wrapper
