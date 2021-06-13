<?php

namespace Deployer;

require_once 'recipe/common.php';

// Project repository
set('repository', 'git@github.com:yabutayukinari/type77.git');

host(getenv('IP_ADDRESS'))
    ->port(getenv('PORT_NO'))
    ->user(getenv('USER_NAME'))
    ->identityFile('~/.ssh/id_rsa')
    ->addSshOption('StrictHostKeyChecking', 'no')
    ->stage('staging')
    ->set('deploy_path', '/var/bot/type77_test');

set('shared_dirs', []);
set('shared_files', ['.env', 'src/services.php', 'mybot.sqlite3']);
set('writable_dirs', []);
set('writable_mode', 'chmod');
set('writable_chmod_mode', '0777');
set('writable_use_sudo', false);

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
    'deploy:unlock',
    'cleanup',
]);

after('deploy', 'success');
after('deploy:failed', 'deploy:unlock');
