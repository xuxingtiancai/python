#coding=gbk

#假设需要编译执行的文件是Main.py

#外部执行：
os.system('python Exe.py Main.py args[]')

#内部执行：
if __name__ == '__main__':
    if sys.argv[0].endswith('.py'):
        os.system('python [py2exe]/Exe.py Main.py %s' % ' '.join(sys.argv[1:]))
    else:
        main()

