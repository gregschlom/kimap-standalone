#!/usr/bin/env python
import optparse
import os, sys, stat

def which(program):
    '''
    Returns the path to a given executable, or None if not found
    '''
    import os
    if os.name == "nt":
	    program += ".exe"

    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def dictToString(dict):
    '''
    Joins the keys and values of a dictionary, using = as a separator
    '''
    ret = ''
    for key, value in dict.iteritems():
        ret += key + '=' + value + ' '
    return ret
  
def escape(s):
    '''
    Replaces \ with \\ and " with \"
    '''
    return s.replace('\\', '\\\\').replace('"', '\\"')
    
def generateCmakeCommand(project, additionalOptions = {}):
    '''
    Generates the run-cmake command for a given project
    '''

    baseOptions = {
        '-DQT_QMAKE_EXECUTABLE:FILEPATH': options.qmake,
        '-DCMAKE_INSTALL_PREFIX': '"' + rootPath + '"',
        '-DCMAKE_PREFIX_PATH': '"' + rootPath + '"',
        '-DCMAKE_BUILD_TYPE': 'Debug' if options.debug else 'Release',
        '-DSTATIC_LIBRARY': 'ON' if options.static else 'OFF',
        '-DKDE4_BUILD_TESTS': 'ON' if options.tests else 'OFF',
        '-DKIMAP_STANDALONE': 'ON',
        '-DNO_DBUS': 'ON',
        '-DCMAKE_CXX_FLAGS': '"-DKIMAP_STANDALONE -DNO_DBUS' + (' -DKDEWIN_STATIC_LIBS' if options.static else '') + '"'
    }

    buildFolder = rootPath + '/build/' + project
    buildFolders.append(buildFolder)

    try:
        os.makedirs(buildFolder)
    except:
        pass    # makdeirs raise an exception if the folder already exist, ignore it.
       
    command = 'cmake ' \
                + ('-G "NMake Makefiles" ' if os.name == 'nt' else '') \
                + dictToString(baseOptions) \
                + dictToString(additionalOptions) \
                + '"' + rootPath + '\\src\\' + project + '"'
    
    fullScript = '#!/usr/bin/env python\n' \
               + 'import os\n' \
               + 'os.system("' + escape(command) + '")\n'
               
    filename = buildFolder + '/run-cmake.py'
    print ' -- generating ' + filename
    file = open(filename, 'w')
    file.write(fullScript)
    file.close()
    os.chmod(filename, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
    
###################################################################

parser = optparse.OptionParser()

parser.add_option("--qmake", dest="qmake", help="full path to qmake executable", metavar="QMAKE")
parser.add_option("--debug",   action="store_true",  dest="debug",  help="build in debug mode (default)", default=True)
parser.add_option("--release", action="store_false", dest="debug",  help="build in release mode")
parser.add_option("--static",  action="store_true",  dest="static", help="build as static libraries (default)", default=True)
parser.add_option("--shared",  action="store_false", dest="static", help="build as a shared libraries")
parser.add_option("--tests",   action="store_true",  dest="tests",  help="build tests", default=False)

(options, args) = parser.parse_args()

buildFolders = []

# If --qmake wasn't specified, try to autodetect it in path
if options.qmake == None:
    options.qmake = which("qmake")

# If we couldn't autodetect, fail
if options.qmake == None:
    print "Could not find qmake executable in path, please specify it with the --qmake command line argument";
    sys.exit(1)
 
# If the --qmake option is invalid, fail
if not (os.path.exists(options.qmake) and os.access(options.qmake, os.X_OK)):
    print 'Could not open qmake executable "' + options.qmake + '"'
    sys.exit(1)

# Initialize paths with forward slashes on all platforms
rootPath = os.getcwd()

if os.name == 'nt':
    options.qmake = options.qmake.replace('\\', '/')
    rootPath = rootPath.replace('\\', '/')

print 'Using qmake executable at "' + options.qmake + '"\n'

## Boost
generateCmakeCommand("3rdparty/boost");

## Cyrus-sasl
generateCmakeCommand("3rdparty/cyrus-sasl", {'-DSTATIC_PLUGIN=': 'ON' if options.static else 'OFF'})

## ZLib
generateCmakeCommand("3rdparty/zlib");

## Automoc
generateCmakeCommand("automoc");

## kdewin on windows
if os.name == "nt":
	generateCmakeCommand("kdewin");

## kdelibs
generateCmakeCommand("kdelibs");

## kdepimlibs
generateCmakeCommand("kdepimlibs", {'-DKDEPIM_NO_KRESOURCES': 'ON', 
                                    '-DKDEPIM_NO_KCAL': 'ON', 
                                    '-DCMAKE_CXX_FLAGS': '"-DKDELIBS_STATIC_LIBS"' if options.static else '""'})

## ksmtp
generateCmakeCommand("ksmtp", {'-DCMAKE_CXX_FLAGS': '"-DKDELIBS_STATIC_LIBS -DKDEPIM_STATIC_LIBS"' if options.static else '""'})
                                    
## Generate the build-all script

buildAll = '#!/usr/bin/env python\nimport os, sys\n'
for folder in buildFolders:
    command = ""
    if os.name == 'nt':
        command = 'cd "' + folder + '" && python run-cmake.py && jom && jom install'
    else:
        command = 'cd "' + folder + '" && ./run-cmake.py && make && make install'
    buildAll += 'if os.system("' + escape(command) + '") != 0:\n    sys.exit(1)\n'

filename = rootPath + '/build-all.py'
file = open(filename, 'w')
file.write(buildAll)
file.close()
os.chmod(filename, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)

print "\nConfiguration successful. Now you can launch build-all.py\n";

