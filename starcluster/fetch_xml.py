import os
import pickle
from datetime import datetime
from ConfigParser import ConfigParser
from IPython.parallel import Client

config = ConfigParser()
config.read('{0}/config.ini'.format(os.path.dirname(os.path.realpath(__file__))))

rc = Client(packer="pickle")
dview = rc[:]
print rc.ids


@dview.remote(block=True)
def makedir(directory):
    import os
    try:
        os.makedirs(directory)
    except:
        pass

@dview.remote(block=True)
def fetch(directory):
    import os
    for f in files:
        fname = f.split("/")[-1]
        os.chdir(directory)
        if not os.path.exists(fname):
            os.system("wget {0}".format(f))
            os.system("unzip {0}".format(fname))


fname = open("{0}/urls.pickle".format(config.get('directory', 'sqlalchemy')), "rb")
urls = pickle.load(fname)

for year in xrange(2005, 2014):
    print year, datetime.now()
    dview.scatter("files", urls[year])
    directory = "{0}/{1}".format(config.get('directory', 'local'), year)
    print "  *", directory
    makedir(directory)
    fetch(directory)
