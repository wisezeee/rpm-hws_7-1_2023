env_consts = {
    'PG_HOST': '127.0.0.1',
    'PG_PORT': '5432',
    'PG_USER': 'app',
    'PG_PASSWORD': '123',
    'PG_DBNAME': 'test'
}


def setup_env():
    lines = [f'{const}={value}\n' for const, value in env_consts.items()]
    with open('.env', 'w') as env_file:
        env_file.writelines(lines)


if __name__ == '__main__':
    setup_env()
