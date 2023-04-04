import configparser
import json
import os,sys
from pathlib import Path


class mysetting:
    def __init__(self):
        parser = configparser.ConfigParser()
        current_folder = Path(__file__).absolute().parent
        os.chdir(str(current_folder))
        config_path = os.path.dirname(__file__) + '/dbpasswd.ini'
        # config_path = os.path.expanduser('dbpasswd.ini')
        parser.read(config_path, encoding='utf-8')
        if not os.path.exists(config_path):
            raise SystemError('config_path:{} not exists'.format(config_path))

        locs = [w[4:] for w in filter(lambda x: x.startswith("loc:"), parser.sections())]

        cfg = {}
        for loc in locs:
            x = parser["loc:%s" % loc]
            tmp = {}
            for k, v in x.items():
                k, v = k.strip(), v.strip()
                try:
                    tmp[k] = json.loads(v)
                except:
                    tmp[k] = v
            cfg[loc] = tmp

        self.cfg = cfg

    def __getitem__(self, loc):
        return self.cfg[loc]


db_settings = mysetting()

if __name__ == '__main__':
    db_settings = mysetting()
    print(db_settings['test_postgresql']['host'])
