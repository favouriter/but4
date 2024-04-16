import os
paths = os.listdir()
paths = [p for p in paths if os.path.isdir(p)]
root_path = os.getcwd()
for p in paths:
    os.chdir(f'{root_path}/{p}')
    if not os.path.exists(f'{root_path}/{p}/.git'):continue
    print(os.getcwd())
    try:
        os.system('git pull')
    except Exception as e:
        raise e
