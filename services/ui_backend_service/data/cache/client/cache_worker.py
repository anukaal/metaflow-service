import os
import json

import click

from .cache_action import import_action_class_spec


def execute_action(tempdir, action_spec, request_file):
    action_cls = import_action_class_spec(action_spec)
    with open(os.path.join(tempdir, request_file)) as f:
        request = json.load(f)

    execute(tempdir, action_cls, request)
    return True


def best_effort_read(key_paths):
    for key, path in key_paths:
        try:
            with open(path, 'rb') as f:
                yield key, f.read()
        except:
            pass


def execute(tempdir, action_cls, req):
    try:
        # prepare stream
        stream = None
        if req['stream_key']:
            stream = open(os.path.join(tempdir, req['stream_key']), 'a', buffering=1)

            def stream_output(obj):
                stream.write(json.dumps(obj) + '\n')
        else:
            stream_output = None

        # prepare keys
        keys = list(req['keys'])
        ex_keys = dict(best_effort_read(req['existing_keys'].items()))

        # execute action
        res = action_cls.execute(
            message=req['message'],
            keys=keys,
            existing_keys=ex_keys,
            stream_output=stream_output,
            invalidate_cache=req.get('invalidate_cache', False))

        # write outputs to keys
        for key, val in res.items():
            blob = val if isinstance(val, bytes) else val.encode('utf-8')
            with open(os.path.join(tempdir, req['keys'][key]), 'wb') as f:
                f.write(blob)
    finally:
        # make sure the stream is finalized so clients won't hang even if
        # the worker crashes
        if stream:
            stream.write('\n\n')
            stream.close()


@click.command()
@click.option("--request-file",
              default='request.json',
              help="Read request from this file.")
@click.argument('action_spec')
def cli(action_spec, request_file=None):
    """
    Execute an action specified by action_spec.
    """
    action_cls = import_action_class_spec(action_spec)
    with open(request_file) as f:
        req = json.load(f)

    execute("./", action_cls, req)


if __name__ == '__main__':
    cli(auto_envvar_prefix='MFCACHE_WORKER')
