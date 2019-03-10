from urllib import request
import argparse
import logging
import json
import os


def get_response(url, logger):
    """
    Requisita um GET e retorna a resposta obtida em caso de sucesso.

    Feito o request, sua resposta é validada e retornada.
    Em caso de erro no request ou na validação, retorna None.
    Todas as mensagens são tratadas pelo logger.
    """
    try:
        logger.info('GET Request: {}'.format(url))
        response = request.urlopen(url)
    except Exception as error:
        logger.error(error)
        response = None
    else:
        code = response.getcode()
        if code != 200:
            logger.error('Resposta inválida do servidor. Código: ' + str(code))
            headers = ['\t{}: {}'.format(*h) for h in response.getheaders()]
            map(logger.info, headers)
            response = None
    finally:
        return response


def get_filename(post, filter_type, resolution):
    """
    Valida um post e retorna o nome do arquivo ou uma string vazia.

    Recebe um dicionário referente a um post, verifica se há uma imagem,
    a filtra e, se válida, retorna o nome do arquivo.
    """
    post_res = [post.get('w'), post.get('h')]
    post_ext = post.get('ext')
    filename = '{}{}'.format(post.get('tim'), post_ext)

    if (None in post_res) or (post_ext not in ['.jpg', '.jpeg', '.png']) or (
        filter_type == 'EQUAL' and post_res != resolution) or (
            filter_type == 'MAX' and post_res > resolution) or (
            filter_type == 'MIN'and post_res < resolution):
        filename = ''

    return filename


# Configuração dos argumentos da linha de comando
parser = argparse.ArgumentParser(
    description='Busca e baixa wallpapers de uma board do 4chan.')
parser.add_argument(
    '-r',
    '--resolution',
    type=int,
    nargs=2,
    metavar=('WIDTH', 'HEIGHT'),
    required=True,
    help='Resolução desejada dos wallpapers')
parser.add_argument(
    '-b', '--board', default='wg', help='Id da board sem as barras')
parser.add_argument(
    '-f',
    '--filter',
    choices=['MIN', 'MAX', 'EQUAL'],
    default='EQUAL',
    help='Filtro aplicado às imagens encontradas na board')
parser.add_argument(
    '-d',
    '--destination',
    default=os.path.join(os.getcwd(), 'Wallpapers'),
    help='Onde serão salvos os wallpapers')
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Imprime informações e erros na tela')
args = parser.parse_args()

# Configurar exibição de mensagens na tela
logging.basicConfig(
    level=logging.NOTSET,
    format='%(message)s',
    handlers=[logging.NullHandler()])
logger = logging.getLogger()
if args.verbose:
    logger.addHandler(logging.StreamHandler())

if not os.path.exists(args.destination):
    os.makedirs(args.destination)

api_url = 'https://{}.4cdn.org/{}/{}'

res = get_response(api_url.format('a', args.board, 'threads.json'), logger)
pages = [] if res is None else json.load(res)
threads = [thrd['no'] for thrds in pages for thrd in thrds['threads']]
downloads = 0

for thread_id in threads:
    res = get_response(
        api_url.format('a', args.board, 'thread/{}.json'.format(thread_id)),
        logger)

    if res is None:
        continue

    posts = json.load(res)
    filenames = map(lambda p: get_filename(p, args.filter, args.resolution),
                    posts['posts'])

    for filename in filter(bool, filenames):
        res = get_response(api_url.format('i', args.board, filename), logger)

        if res is None:
            continue

        image = open(os.path.join(args.destination, filename), 'wb')
        image.write(res.read())
        image.close()

        logger.info('Arquivo {!r} baixado'.format(filename))
        downloads += 1

logger.info('Arquivos baixados: {}'.format(downloads))
