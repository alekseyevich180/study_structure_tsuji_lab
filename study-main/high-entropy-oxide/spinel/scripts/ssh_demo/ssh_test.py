import paramiko

with paramiko.SSHClient() as client:
    HOSTNAME = "genkai.hpc.kyushu-u.ac.jp"
    USERNAME = "ku40000345"
    KEY_FILENAME = "/home/az/code/study/high-entropy-oxide/spinel/scripts/ssh_demo/busseiken_private"
    # PASSWORD = 'password'
    # SSH接続
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 1. パスワード認証認証方式
    # client.connect(hostname=HOSTNAME, port=22, username=USERNAME, password=PASSWORD)

    # 2. 公開鍵認証方式
    client.connect(
        hostname=HOSTNAME, port=22, username=USERNAME, key_filename=KEY_FILENAME
    )

    # コマンド実行
    # 作業ディレクトリに移動する
    base_dir = "iwai/Cr2O3/test/jikken3"

    # ディレクトリのリスト
    directory_list = [1, 2, 3, 4]

    for i in directory_list:
        # コマンドをまとめて実行
        command = f"""
        cd {base_dir} &&
        mkdir {i} &&
        cp OUTCARS/OUTCAR_{i} {i}/OUTCAR &&
        cp test_vef.sh {i}/ &&
        cd {i} &&
        qsub test_vef.sh
        """

        stdin, stdout, stderr = client.exec_command(command)
        stdin.close()
