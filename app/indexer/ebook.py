from indexer import Indexer
from pathlib import Path
from ebooklib import epub
from datetime import datetime
from elasticsearch.helpers import bulk


class EpubIndexer(Indexer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.path = kwargs.get('path')
        self.path_prefix = kwargs.get('path_prefix', '')

    def _ebook_data_generator(self):
        for filepath in Path(self.path).glob('**/*.epub'):
            book = epub.read_epub(filepath)

            title = book.get_metadata('DC', 'title')
            identifier = book.get_metadata('DC', 'identifier')
            language = book.get_metadata('DC', 'language')
            creator = book.get_metadata('DC', 'creator')
            publisher = book.get_metadata('DC', 'publisher')
            date = book.get_metadata('DC', 'date')
            contributor = book.get_metadata('DC', 'contributor')
            description = book.get_metadata('DC', 'description')

            if not title:
                continue

            if not identifier:
                continue

            try:
                document = {
                    '_op_type': 'index',
                    '_index': self.es_index,
                    '_type': 'ebook',
                    '_id': identifier[0][0],
                    'meta': {
                        'added_at': datetime.utcnow(),
                        'base_path': filepath.absolute().as_posix().replace('\\', '/').replace(self.path_prefix, ''),
                    },
                    'title': title[0][0] if title else '',
                    'identifier': identifier[0][0] if identifier else '',
                    'language': language[0][0] if language else '',
                    'creator': creator[0][0] if creator else '',
                    'publisher': publisher[0][0] if publisher else '',
                    'date': date[0][0] if date else '',
                    'contributor': contributor[0][0] if contributor else '',
                    'description': description[0][0] if description else '',
                }

                yield document
            except IndexError:
                continue

    def run(self):
        bulk(self.es, self._ebook_data_generator())
