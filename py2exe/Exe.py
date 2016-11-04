
def pyinstaller(files, **kwargs):
    mainfile = files[0]
    paras = kwargs.get('paras', [])
    key = os.path.basename(mainfile)[:-3]
    sys_dir = os.getcwd()
    exe_dir = '[pyinstaller]/{0}'.format(key)
    if not os.path.exists(exe_dir):
        os.makedirs(exe_dir)

    files_str = ' '.join(os.path.join(sys_dir, f) for f in files)
    exe('cd {0} && pyinstaller -F {1}'.format(exe_dir, files_str))
    paras_str = ' '.join(paras)
    exe('{0}/dist/{1}.exe {2}'.format(exe_dir, key, paras_str))

def py2exe(files, **kwargs):
    mainfile = files[0]
    paras = kwargs.get('paras', [])
    key = os.path.basename(mainfile)[:-3]
    sys_dir = os.getcwd()
    exe_dir = '[py2exe]/{0}'.format(key)
    if not os.path.exists(exe_dir):
        os.makedirs(exe_dir)
    c_SetupPy = 'setup.py'

    with open(os.path.join(exe_dir, c_SetupPy), 'w') as fout:
        print >>fout, 'from distutils.core import setup'
        print >>fout, 'import py2exe'
        files_str = ','.join('"%s"' % os.path.join(sys_dir, f) for f in files)
        print >>fout, 'setup(console=[%s])' % files_str

    exe('cd {0} && python {1} py2exe'.format(exe_dir, c_SetupPy))
    paras_str = ' '.join(paras)
    exe('{0}/dist/{1}.exe {2}'.format(exe_dir, key, paras_str))
    
    
if __name__ == '__main__':
    if sys.argv[0].endswith('.py'):
        util.pyinstaller([os.path.relpath(__file__), 'util.py'])
    else:
        main()
