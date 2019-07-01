"""Command line interface for the G2P toolkit."""

import click

import g2p
from g2p.scrape import run as scrape_run


@click.group(help=g2p.__doc__)
@click.version_option(version=g2p.__version__)
def cli():
    pass


@cli.command(help=g2p.scrape.__doc__)
# TODO: communicate `language` has to be like "English" but not "eng"
#   anyway to make `language` more user-friendly?
#   click.argument doesn't allow a "help" kwarg, unfortunately
@click.argument("language", type=str)
@click.option(
    "--phonetic",
    is_flag=True,
    help=(
        "Retrieve the [phonetic] transcriptions "
        "rather than the /phonemic/ ones."
    ),
)
@click.option(
    "--no-stress", is_flag=True, help="Remove stress marks in pronunciations."
)
@click.option(
    "--no-syllable-boundaries",
    is_flag=True,
    help="Remove syllable boundary marks in pronunciations.",
)
@click.option(
    "--dialect",
    type=str,
    multiple=True,
    help=(
        "Retrieve entries that have this dialect specification. "
        "If not given, then all dialects are included in the output. "
        "The dialect name is the one in the underlying HTML code, inside "
        '<span><class="ib-content qualifier-content" title="[dialect-name]">, '
        "not the one seen in the rendered web page on the surface."
    ),
    # TODO: The UX isn't great.
    #   Anyway to improve dialect specification?
    #   e.g., not need to peek the underlying HTML?
    # TODO: Allow multiple dialects being specified
)
@click.option(
    "--require-dialect-label",
    is_flag=True,
    help="Include only entries that have a dialect specification.",
)
@click.option(
    "--casefold", is_flag=True, help="Apply case-folding to the orthography."
)
@click.option(
    "--cut-off-date",
    type=str,
    help=(
        "Retrieve only entries that were added to Wiktionary "
        "on or before this date (in ISO format, e.g., 2018-10-23). "
        "If not given, today's date is used."
    ),
)
@click.option(
    "--output",
    type=str,
    help="Output filename. If not given, results appear in stdout.",
)
def scrape(
    language,
    phonetic,
    no_stress,
    no_syllable_boundaries,
    dialect,
    require_dialect_label,
    casefold,
    cut_off_date,
    output,
):
    scrape_run(
        language,
        phonetic,
        no_stress,
        no_syllable_boundaries,
        dialect,
        require_dialect_label,
        casefold,
        cut_off_date,
        output,
    )


@cli.command(help="Evaluate G2P results.")
@click.argument("foo")
@click.option("--bar", default=1, help="number of bars")
def evaluate(foo, bar):
    # TODO
    print(f"running the 'evaluate' command]\nfoo = {foo}\nbar = {bar}")


if __name__ == "__main__":
    cli()
