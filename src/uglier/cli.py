import sys
import logging

from uglier.colored_logger import ColoredFormatter
from uglier.patcher import Patcher

from argparse import ArgumentParser


def parse_known_intermixed_args(self, args=None, namespace=None):
    # self - argparse parser
    # simplified from http://bugs.python.org/file30204/test_intermixed.py
    parsefn = super(SubParser, self).parse_known_args  # avoid recursion

    positionals = self._get_positional_actions()
    for action in positionals:
        # deactivate positionals
        action.save_nargs = action.nargs
        action.nargs = 0

    namespace, remaining_args = parsefn(args, namespace)
    for action in positionals:
        # remove the empty positional values from namespace
        if hasattr(namespace, action.dest):
            delattr(namespace, action.dest)
    for action in positionals:
        action.nargs = action.save_nargs
    # parse positionals
    namespace, extras = parsefn(remaining_args, namespace)
    return namespace, extras


class SubParser(ArgumentParser):
    parse_known_args = parse_known_intermixed_args


def parse_arguments(args):
    parser = ArgumentParser(
        description="Make your python code a (working) repulsive mess!"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose logging"
    )
    parser.add_argument(
        "-y", "--yolo", action="store_true", help="overwrite the original file(s)"
    )
    parser.add_argument("sources", nargs="+", help="files to uglify")

    (opts, _) = parser.parse_known_intermixed_args(args)
    return opts


def uglier(args):
    logger = logging.getLogger("uglier")
    logger.setLevel(logging.WARNING)
    sh = logging.StreamHandler()
    sh.setFormatter(ColoredFormatter())
    logger.addHandler(sh)

    opts = parse_arguments(args)
    if opts.verbose:
        logger.setLevel(logging.DEBUG)

    patcher = Patcher(opts)
    patcher.patch_paths(opts.sources)


def run():
    uglier(sys.argv[1:])


if __name__ == "__main__":
    run()
