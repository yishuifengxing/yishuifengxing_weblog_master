from data.connect import session
from data.user_module import User

def add_user():
    person = User(username='yishuifengxing',password='20160828307@86')
    session.add(person)
    session.commit()

if __name__ == '__main__':
    add_user()