import random
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def gen_vcode(length=4):
    return ''.join(random.choices('0123456789', k=length))


def is_valid(email) -> bool:
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def gen_vcode_msg(vcode, to_addr, from_addr='moss_se2023@163.com'):
    """
        vcode: 发送的验证码
        from_addr: 发送方邮箱
        to_addr: 接收方邮箱
        return: 返回含有发送验证码的MIMEText对象
    """
    text = f'您好，欢迎使用MOSS团队开发的ShieAsk平台。\n您的验证码是: {vcode}, 有效期为20分钟。'
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = _format_addr('ShieAsk平台<%s>' % from_addr)
    msg['To'] = _format_addr('用户<%s>' % to_addr)
    msg['Subject'] = Header('ShieAsk平台验证码', 'utf-8').encode()
    return msg


def send_vcode(to_addr, smtp_server='smtp.163.com', from_addr='moss_se2023@163.com', password='WEYVECFDPURIPBPJ'):
    """
        smtp_server: 当前使用的smtp服务器
        from_addr: 发送方邮箱
        password: 发送方邮箱密码（smtp授权码）
        to_addr: 接收方邮箱
    """
    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    vcode = gen_vcode()
    msg = gen_vcode_msg(vcode, to_addr)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    return vcode

# if __name__ == "__main__":
#     to = '20373228@buaa.edu.cn'
#     code = send_vcode(to)
#     print('发送的验证码：', code)
#     # 利用code进行相关操作
