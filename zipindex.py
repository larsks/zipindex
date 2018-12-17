import click
import datetime
import logging
import os
import zipfile

from model import db_session, bind, select, Directory, Archive, File

LOG = logging.getLogger('zipindex')


class App():
    loglevel = None
    zipindex = None


@click.group()
@click.option('-i', '--index', envvar='ZIPINDEX')
@click.option('-v', '--verbose', 'loglevel', is_flag=True,
              flag_value='INFO')
@click.option('-q', '--quiet', 'loglevel', is_flag=True,
              flag_value='WARNING', default=True)
@click.option('-d', '--debug', 'loglevel', is_flag=True,
              flag_value='DEBUG')
@click.pass_context
def zipindex(ctx, index, loglevel):
    if index is None:
        raise click.exceptions.ClickException('you must specify an index')

    ctx.obj = App()
    ctx.obj.zipindex = index
    ctx.obj.loglevel = loglevel

    logging.basicConfig(level=loglevel)

    bind(path=ctx.obj.zipindex, debug=True if loglevel == 'DEBUG' else False)


def scantree(path):
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


@zipindex.command()
@click.argument('sources', nargs=-1)
@click.pass_obj
def create(ctx, sources):
    LOG.info('creating %s', ctx.zipindex)

    with db_session:
        for dir_path in sources:
            LOG.info('processing directory %s', dir_path)
            dir = Directory.get(path=dir_path) or Directory(path=dir_path)
            dir.last_update = datetime.datetime.now()

            for entry in scantree(dir_path):
                if not entry.is_file():
                    continue
                if not entry.path.endswith('.zip'):
                    continue

                zip = zipfile.ZipFile(entry.path)
                LOG.info('processing archive %s', entry.path)
                archive = (Archive.get(path=entry.path) or
                           Archive(directory=dir, path=entry.path))

                for name in zip.namelist():
                    (File.get(archive=archive, path=name) or
                     File(archive=archive, path=name))


@zipindex.command()
@click.argument('patterns', nargs=-1)
@click.pass_obj
def search(ctx, patterns):
    with db_session:
        for pattern in patterns:
            query = select(f for f in File if pattern in f.path)
            for res in query:
                print(res.archive.path, res.path)


if __name__ == '__main__':
    import sys
    zipindex(sys.argv[1:])
