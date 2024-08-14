import argparse
import os.path

parser = argparse.ArgumentParser(description="创建自签名SSL证书")

parser.add_argument('domain', type=str, help='域名')
parser.add_argument('--days', type=int, default=36500, help='证书有效期天数')
parser.add_argument('--root', type=str, default='RootCA', help='根证书名称')
parser.add_argument('--C', type=str, default='CN', help='国家名称')
parser.add_argument('--ST', type=str, default='ShangHai', help='省份名称')
parser.add_argument('--L', type=str, default='ShangHai', help='城市名称')
parser.add_argument('--O', type=str, default='Shanghai XXXX Co., Ltd', help='组织名称')
parser.add_argument('--OU', type=str, default='Shanghai XXXX', help='组织单位名称')
parser.add_argument('--CN', type=str, default='Shanghai XXXXX', help='公司名称')

sys_args = parser.parse_args()

subj = f'/C={sys_args.C}/ST={sys_args.ST}/L={sys_args.L}/O={sys_args.O}/OU={sys_args.OU}/CN={sys_args.CN}'

def os_system(command):
    print('\n\n',command, '\n')
    os.system(command)

# 检查并创建根证书
def create_root():
    if not os.path.exists(f'{sys_args.root}.key'):
        os_system(f'openssl genrsa -des3 -out {sys_args.root}.key 2048')
        os_system(f'openssl req -x509 -new -nodes -key {sys_args.root}.key -sha256 -days {sys_args.days} -out {sys_args.root}.pem -subj "{subj}"')
        os_system(f'openssl x509 -outform der -in {sys_args.root}.pem -out {sys_args.root}.crt')

def create_domain():
    if os.path.exists(f'{sys_args.domain}.key'): return
    os_system(f'openssl genrsa -out {sys_args.domain}.key 2048')
    os_system(f'openssl req -new -key {sys_args.domain}.key -out {sys_args.domain}.csr -subj "{subj}"')
    tmp = f'''authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = *.{sys_args.domain}'''
    with open(f'{sys_args.domain}.ext', 'w') as f:
        f.write(tmp)
    os_system(f'openssl x509 -req -in {sys_args.domain}.csr -CA {sys_args.root}.pem -CAkey {sys_args.root}.key -CAcreateserial -out {sys_args.domain}.crt -days {sys_args.days} -sha256 -extfile {sys_args.domain}.ext')
    os_system(f'openssl x509 -outform PEM -in {sys_args.domain}.crt -out {sys_args.domain}.pem')

if __name__ == '__main__':
    create_root()
    create_domain()
    