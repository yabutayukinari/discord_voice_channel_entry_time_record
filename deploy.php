<?php

namespace Deployer;

require_once 'recipe/common.php';

// Project repository
set('repository', 'git@github.com:yabutayukinari/type77.git');

set('_xm3_pass', getenv('XM3_PASS'));

host(getenv('IP_ADDRESS'))
    ->port(getenv('PORT_NO'))
    ->user(getenv('USER_NAME'))
    ->identityFile('~/.ssh/id_rsa')
    ->addSshOption('StrictHostKeyChecking', 'no')
    ->stage('staging')
    ->set('deploy_path', '/var/bot/type77_test');

desc('service restart');
task('service:restart', function () {
    run('echo {{_xm3_pass}} | sudo -S  systemctl restart type77_test.service');
});

desc('create venv');
task('venv:create', function () {
    run('cd /var/bot/type77_test/current && python3 -m venv venv');
});

desc('pip install');
task('pip:install', function () {
    run('cd /var/bot/type77_test/current && . venv/bin/activate && pip install -U -r requirements.txt');
});

set('shared_dirs', []);
set('shared_files', ['src/config.py', 'mybot.sqlite3']);
set('writable_dirs', []);
set('writable_mode', 'chmod');
set('writable_chmod_mode', '0777');
set('writable_use_sudo', true);

desc('Deploy project');
task('deploy', [
    'deploy:info',
    'deploy:prepare',
    'deploy:lock',
    'deploy:release',
    'deploy:update_code',
    'deploy:shared',
    'deploy:writable',
    'deploy:symlink',
    'venv:create',
    'pip:install',
    'deploy:unlock',
    'service:restart',
    'cleanup',
]);

after('deploy', 'success');
after('deploy:failed', 'deploy:unlock');
