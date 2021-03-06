from fabfile.config import *
from fabfile.utils.fabos import detect_ostype

@task
@EXECUTE_TASK
@roles('all')
def cleanup_repo():
    '''Removes all existing repos in all the nodes specified in testbed'''
    execute('cleanup_repo_node', env.host_string)

@task
def cleanup_repo_node(*args):
    '''Remove existing repos in given node'''
    for host_string in args:
        with settings(host_string=host_string):
            os_type = detect_ostype().lower()
            with hide('everything'):
                ts = run("date '+%s'")
            if os_type == 'ubuntu':
                org_repo_file = '/etc/apt/sources.list'
                bck_repo_file = '/etc/apt/sources_%s.list' % ts
                print 'Backup Original sources.list (%s) as (%s)' % (
                    org_repo_file, bck_repo_file)
                run('mv %s %s' % (org_repo_file, bck_repo_file))
                print 'Create an empty sources.list'
                run('touch /etc/apt/sources.list')
                run('chmod 644 /etc/apt/sources.list')
                run('apt-get update')
            elif os_type in ['centos', 'redhat']:
                with cd('/etc/yum.repos.d/'):
                    with hide('everything'):
                        repo_files = run('ls -1 *.repo').split('\r\n')
                    print 'Backup Original repo files with timestamp'
                    for repo_file in repo_files:
                        run('mv %s %s.%s' % (repo_file, repo_file, ts))
                run('yum clean all')
