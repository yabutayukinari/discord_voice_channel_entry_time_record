<?php

namespace Deployer;

require_once 'recipe/common.php';

// Project repository
set('repository', 'git@github.com:yabutayukinari/type77.git');

// staging
host('staging')
    ->hostname(getenv('IP_ADDRESS'))
    ->port(getenv('PORT_NO'))
    ->user(getenv('USER_NAME'))
    ->identityFile('~/.ssh/id_rsa')
    ->addSshOption('StrictHostKeyChecking', 'no')
    ->stage('staging')
    ->set('branch', 'develop')
    ->set('deploy_path', '/var/bot/type77_test');


// release
host('release')
    ->hostname(getenv('IP_ADDRESS'))
    ->port(getenv('PORT_NO'))
    ->user(getenv('USER_NAME'))
    ->identityFile('~/.ssh/id_rsa')
    ->addSshOption('StrictHostKeyChecking', 'no')
    ->stage('release')
    ->set('branch', 'main')
    ->set('deploy_path', '/var/bot/type77');

desc('file chmod staging');
task('file:chmod_staging', function () {
    run('chmod 775 /var/bot/type77_test/current/src/launcher.py');
});

desc('service restart staging');
task('service:restart_staging', function () {
    run('sudo systemctl restart type77_test.service');
});

desc('create venv staging');
task('venv:create_staging', function () {
    run('cd /var/bot/type77_test/current && python3 -m venv venv');
});

desc('pip install staging');
task('pip:install_staging', function () {
    run('cd /var/bot/type77_test/current && . venv/bin/activate && pip install -U -r requirements.txt');
});

set('shared_dirs', []);
set('shared_files', ['src/config.py', 'mybot.sqlite3']);
set('writable_dirs', []);
set('writable_mode', 'chmod');
set('writable_chmod_mode', '0777');
set('writable_use_sudo', true);
set('cleanup_use_sudo', true);

desc('Deploy staging project');
task('deploy_staging', [
    'deploy:info',
    'deploy:prepare',
    'deploy:lock',
    'deploy:release',
    'deploy:update_code',
    'deploy:shared',
    'deploy:writable',
    'deploy:symlink',
    'venv:create_staging',
    'pip:install_staging',
    'file:chmod_staging',
    'deploy:unlock',
    'service:restart_staging',
    'cleanup',
]);

//
desc('file chmod release');
task('file:chmod_release', function () {
    run('chmod 775 /var/bot/type77/current/src/launcher.py');
});

desc('service restart release');
task('service:restart_release', function () {
    run('sudo systemctl restart type77.service');
});

desc('create venv release');
task('venv:create_release', function () {
    run('cd /var/bot/type77/current && python3 -m venv venv');
});

desc('pip install release');
task('pip:install_release', function () {
    run('cd /var/bot/type77/current && . venv/bin/activate && pip install -U -r requirements.txt');
});

desc('Deploy release project');
task('deploy_release', [
    'deploy:info',
    'deploy:prepare',
    'deploy:lock',
    'deploy:release',
    'deploy:update_code',
    'deploy:shared',
    'deploy:writable',
    'deploy:symlink',
    'venv:create_release',
    'pip:install_release',
    'file:chmod_release',
    'deploy:unlock',
    'service:restart_release',
    'cleanup',
]);

after('deploy_staging', 'success');
after('deploy_release', 'success');
after('deploy:failed', 'deploy:unlock');


