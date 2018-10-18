import sys, subprocess, pprint
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
# from . import error, utility
from acmacs_base import json, files

# ----------------------------------------------------------------------

sVirusTypeConvert = {
    'A(H1N1)': 'h1seas',
    'A(H1N1)2009PDM': 'h1pdm',
    'A(H3N2)': 'h3',
    'BYAMAGATA': 'b-yam',
    'BVICTORIA': 'b-vic',
    }

sVirusTypeConvert_ssm_report = {
    'A(H1N1)': None,
    'A(H1N1)2009PDM': 'h1',
    'A(H3N2)': 'h3',
    'BYAMAGATA': 'by',
    'BVICTORIA': 'bv',
    }

sAssayConvert = {
    "HI": "hi",
    "FOCUS REDUCTION": "neut",
    "PLAQUE REDUCTION NEUTRALISATION": "neut",
    "MN": "neut",
    }

# ----------------------------------------------------------------------

def get_recent_merges(target_dir :Path, session=None, force=False, rename="ssm-report"):
    done_path = Path(target_dir, "getting-recent-merges-done")
    if not done_path.exists() or force:
        merge_data_path = Path(target_dir, "megres.json")
        try:
            merge_data = json.read_json(merge_data_path)
        except:
            merge_data = {}

        response = api(session=session).command(C="ad_whocc_recent_merges", log=False, labs=None, virus_types=None)
        if "data" not in response:
            module_logger.error("No \"data\" in response of ad_whocc_recent_merges api command:\n{}".format(pprint.pformat(response)))
            raise RuntimeError("Unexpected result of ad_whocc_recent_merges c2 api command")
        response = response['data']
        response.sort(key=lambda e: "{lab:4s} {virus_type:10s} {assay}".format(**e))
        module_logger.info('WHO CC recent merges\n{}'.format("\n".join("{lab:4s} {virus_type:14s} {assay:31s} {chart_id}".format(**e) for e in response)))

        formats = ["ace"] # "sdb.xz", "acd1.xz",

        for entry in response:
            if entry["lab"] != "CNIC" and not (entry["lab"] == "NIID" and entry["virus_type"] == "A(H3N2)" and entry["assay"] == "HI"):
                if rename == "ssm-report":
                    basename = "{lab}-{vt}-{assay}".format(lab=entry["lab"], vt=sVirusTypeConvert[entry["virus_type"]], assay=sAssayConvert[entry["assay"]]).lower()
                elif rename == "signature-pages":
                    basename = "{lab}-{vt}-{assay}".format(lab=entry["lab"], vt=sVirusTypeConvert_ssm_report[entry["virus_type"]], assay=sAssayConvert[entry["assay"]]).lower()
                else:
                    raise RuntimeError(f"Unrecognized rename arg: {rename!r}")
                targets = {f: target_dir.joinpath(basename + "." + f) for f in formats}
                if merge_data.get(basename) != entry["chart_id"] or not targets[formats[0]].exists():
                    merge_data[basename] = entry["chart_id"]
                    for fmt, filename in targets.items():
                        chart = api(session=session).command(C="chart_export", log=False, id=entry["chart_id"], format=fmt, part="chart")["chart"]
                        if isinstance(chart, dict) and "##bin" in chart:
                            import base64
                            chart = base64.b64decode(chart["##bin"].encode('ascii'))
                        # if fmt in ["sdb.xz", "ace"]:
                        #     json.write_json(path=filename, data=chart)
                        # else:
                        files.backup_file(filename)
                        with filename.open('wb') as f:
                            f.write(chart)
                        module_logger.info(str(filename.resolve()))
        json.write_json(path=merge_data_path, data=merge_data)
        done_path.touch()

# ----------------------------------------------------------------------

def make_h1pdm_overlay(recent_merges_dir, log_dir, force=False):
    target = recent_merges_dir.joinpath("all-h1pdm-hi.ace")
    if not target.exists() or force:
        module_logger.info('Making H1pdm overlay merge')
        charts = [recent_merges_dir.joinpath("cdc-h1pdm-hi.ace"), recent_merges_dir.joinpath("nimr-h1pdm-hi.ace"), recent_merges_dir.joinpath("niid-h1pdm-hi.ace"), recent_merges_dir.joinpath("melb-h1pdm-hi.ace")]
        # merge = recent_merges_dir.joinpath("all-h1pdm-hi.merge.acd2.xz")
        merge = recent_merges_dir.joinpath("all-h1pdm-hi.merge.ace")
        subprocess.check_call("c2 merge.py -r --overlay -o '{}' '{}' >'{}' 2>&1".format(merge, "' '".join(str(c) for c in charts), log_dir.joinpath("h1pdm-merge.log")), shell=True)
        module_logger.info('Relaxing H1pdm overlay merge')
        # subprocess.check_call("c2 relax-existing.py --disconnect-having-few-titers --disconnect-having-nan '{}' '{}' >'{}' 2>&1".format(merge, target, log_dir.joinpath("h1pdm-relax.log")), shell=True)
        subprocess.check_call("ad chart-relax-existing '{}' '{}' >'{}' 2>&1".format(merge, target, log_dir.joinpath("h1pdm-relax.log")), shell=True)
        # module_logger.info('Making ace for H1pdm overlay merge')
        # subprocess.check_call("c2 convert.py '{}' '{}' >'{}' 2>&1".format(target, recent_merges_dir.joinpath("all-h1pdm-hi.ace"), log_dir.joinpath("h1pdm-sdb.log")), shell=True)

# ----------------------------------------------------------------------

sAPI = None

def api(session=None):
    global sAPI
    if sAPI is None:
        user = "whocc-viewer"
        if session is None:
            from getpass import getpass
            password = getpass(prompt="Password for {!r} on amcacs-web: ".format(user))
        else:
            password = None
        sAPI = API(session=session, user=user, password=password)
    return sAPI

# ----------------------------------------------------------------------

class API:

    def __init__(self, session=None, user="whocc-viewer", password=None, url_prefix='https://acmacs-web.antigenic-cartography.org/'):
        """If host is None, execute command in this acmacs instance directly."""
        self.url_prefix = url_prefix
        self.session = session
        if not session and user:
            self._login(user, password)

    def _execute(self, command, print_response=False, log_error=True, raise_error=False):
        if self.url_prefix:
            if self.session:
                command.setdefault('S', self.session)
            response = self._execute_http(command)
        else:
            raise NotImplementedError()
            # ip_address = '127.0.0.1'
            # command.setdefault('I', ip_address)
            # command.setdefault('F', 'python')
            # if self.session:
            #     from ..mongodb_collections import mongodb_collections
            #     command.setdefault('S', mongodb_collections.sessions.find(session_id=self.session, ip_address=ip_address))
            # from .command import execute
            # response = execute(command)
            # if isinstance(response.output, str):
            #     response.output = json.loads(response.output)
        #module_logger.info(repr(response.output))
        if isinstance(response, dict) and response.get('E'):
            if log_error:
                module_logger.error(response['E'])
                for err in response['E']:
                    if err.get('traceback'):
                        module_logger.error(err['traceback'])
            if raise_error:
                raise CommandError(response['E'])
        elif print_response:
            if isinstance(response, dict) and response.get('help'):
                module_logger.info(response['help'])
            else:
                module_logger.info('{} {!r}'.format(type(response), response))
        return response

    def _execute_http(self, command):
        command['F'] = 'json'
        module_logger.debug('_execute_http %r', command)
        response = self._urlopen(url='{}/api'.format(self.url_prefix), data=json.dumps(command).encode('utf-8'))
        return json.loads(response)

    def _login(self, user, password):
        import random
        response = self._execute(command=dict(F='python', C='login_nonce', user=user), print_response=False)
        if response.get('E'):
            raise LoginFailed(response['E'])
        # module_logger.debug('login_nonce user:{} nonce:{}'.format(user, response))
        digest = self._hash_password(user=user, password=password)
        cnonce = '{:X}'.format(random.randrange(0xFFFFFFFF))
        password = self._hash_nonce_digest(nonce=response['nonce'], cnonce=cnonce, digest=digest)
        response = self._execute(command=dict(F='python', C='login', user=user, cnonce=cnonce, password=password, application=sys.argv[0]), print_response=False)
        module_logger.debug('response {}'.format(response))
        if response.get('E'):
            raise LoginFailed(response['E'])
        self.session = response['S']
        module_logger.info('--session={}'.format(self.session))

    def command(self, C, print_response=False, log_error=True, raise_error=False, **args):
        cmd = dict(C=C, log_error=log_error, **self._fix_args(args))
        # try:
        #     getattr(self, '_fix_command_' + C)(cmd)
        # except AttributeError:
        #     pass
        return self._execute(cmd, print_response=print_response, log_error=log_error, raise_error=raise_error)

    def download(self, id):
        return self._urlopen(url='{}/api/?cache=1&session={}&id={}'.format(self.url_prefix, self.session, id))

    def _urlopen(self, url, data=None):
        import ssl, urllib.request
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return urllib.request.urlopen(url=url, data=data, context=context).read()

    def _hash_password(self, user, password):
        import hashlib
        m = hashlib.md5()
        m.update(';'.join((user, 'acmacs-web', password)).encode('utf-8'))
        return m.hexdigest()

    def _hash_nonce_digest(self, nonce, cnonce, digest):
        import hashlib
        m = hashlib.md5()
        m.update(';'.join((nonce, cnonce, digest)).encode('utf-8'))
        return m.hexdigest()

    def __getattr__(self, name):
        if name[0] != '_':
            return lambda **a: self.command(name, **a)
        else:
            raise AttributeError(name)

    # def _fix_command_chart_new(self, cmd):
    #     if isinstance(cmd['chart'], str) and os.path.isfile(cmd['chart']): # read data from filename and encode it to make json serializable
    #         cmd['chart'] = json.BinaryData(open(cmd['chart'], 'rb').read())

    def _fix_args(self, args):
        for to_int in ('skip', 'max_results', 'size'):
            if args.get(to_int) is not None:
                args[to_int] = int(args[to_int])
        return args

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
