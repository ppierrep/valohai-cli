from typing import Callable, Dict, Iterable, Optional, Tuple

import click

from valohai_cli.help_texts import EXECUTION_COUNTER_HELP


def _default_name_formatter(option: Dict[str, str]) -> str:
    return option['name']


def prompt_from_list(
    options: Iterable[dict],
    prompt: str,
    nonlist_validator: Optional[Callable] = None,
    name_formatter: Callable = _default_name_formatter
) -> dict:
    for i, option in enumerate(options, 1):
        click.echo('{number} {name} {description}'.format(
            number=click.style('[%3d]' % i, fg='cyan'),
            name=name_formatter(option),
            description=(
                click.style('(%s)' % option['description'], dim=True)
                if option.get('description')
                else ''
            ),
        ))
    while True:
        answer = click.prompt(prompt)
        if answer.isdigit() and (1 <= int(answer) <= len(options)):
            return options[int(answer) - 1]
        if nonlist_validator:
            retval = nonlist_validator(answer)
            if retval:
                return retval
        for option in options:
            if answer == option['name']:
                return option
        click.secho('Sorry, try again.')
        continue


class HelpfulArgument(click.Argument):
    def __init__(self, param_decls: Tuple[str], **kwargs) -> None:
        self.help = kwargs.pop('help', None)
        super(HelpfulArgument, self).__init__(param_decls, **kwargs)

    def get_help_record(self, ctx):
        if self.help:
            return (self.name, self.help)


def counter_argument(fn: Callable) -> Callable:
    # Extra gymnastics needed because `click.arguments` mutates the kwargs here
    return click.argument('counter', help=EXECUTION_COUNTER_HELP, cls=HelpfulArgument)(fn)
