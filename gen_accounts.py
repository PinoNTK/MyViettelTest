import random
import string
from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.BankAccount

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹỷ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYyy'

def remove_accents(input_str):
    s = ''
    # print(list(u''+input_str))
    for c in list(input_str):
        if c in s1:
            s += s0[s1.index(c)]
        elif c in string.printable:
            s += c
    return s

def address():
    list_addr = ['Hai Bà Trưng','Bạch Mai','Đại Cồ Việt','Lê Thanh Nghị','Bách Khoa',
                 'Tạ Quang Bửu','Phạm Hùng','Cầu Giấy','Nam Từ Liêm','Tây Sơn',
                 'Chùa Bộc','Nguyễn Trãi','Thanh Xuân','Ngã Tư Sở','Hà Đông']
    addr = 'Số {0} Ngách {1} Ngõ {2} {3}'.format(random.randint(1,100),random.randint(1,50),random.randint(1,50),random.choice(list_addr))
    return addr
day_in_month = {
        1:31,
        2:29,
        3:31,
        4:30,
        5:31,
        6:30,
        7:31,
        8:31,
        9:30,
        10:31,
        11:30,
        12:31
    }
def birthday():
    year = random.randint(1980,2002)

    month = random.randint(1,12)
    if month==2 and (year%4==0 and year%100!=0):
        day = 28
    else:
        day = day_in_month[month]
    day = random.randint(1,day+1)
    return '{0}/{1}/{2}'.format(day,month,year)
def mail(name):
    user = '{0}{1}'.format(name.lower().replace(' ', ''), random.randint(1, 9999999))
    return '{0}@{1}'.format(remove_accents(user),random.choice(['gmail.com','outlook.com','viettel.com.vn','yahoo.vn']))


ho = [u'Phạm', u'Nguyễn', u'Trần', u'Hoàng', u'Lê']
ten_dem = {'male':['Văn','Đình'],
           'female':[ 'Thị', 'Ngọc']}

ten = {'male':['Linh', 'Kiên', 'Sơn','Hưng','Hùng','Tuấn','Tú','Đông','Bộ','Đức','Thái','Việt','Hoàng','Tiến','Tùng' ],
        'female':['Nhi', 'Hoa', 'Duyên','Anh','Linh','Ánh','Hương','Hiền','Hòa','Thu','Trang','Phương','Nhung','Nga']}
def name_rand(gender):

    return '{0} {1} {2}'.format(random.choice(ho),random.choice(ten_dem[gender]),random.choice(ten[gender]))
def username(name):
    user = '{0}{1}'.format(remove_accents(name).lower().replace(' ',''),random.randint(1,9999999))
    return user
def gen_account(n):
    accounts = []
    for i in range(n):
        gender = random.choice(['male','female'])
        name = name_rand(gender)
        accounts.append({
            'accountBalance':random.randint(50000,1e9),
            'accountNumber':'{0:011d}'.format(random.randint(1900000000,19900000000)),
            'address':address(),
            'birthday':birthday(),
            'cardNumber':'{0:09d}'.format(random.randint(10000000,999000000)),
            'idNumber':'{0:09d}'.format(random.randint(17400000,179999999)),
            'mail':mail(name),
            'name':name,
            'password':''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits) for _ in range(12)),
            'phoneNumber':'{0:011d}'.format(random.randint(1660000000,1689999999)),
            'role':random.choice(['normal','admin']),
            'username':username(name),
            'gender':gender,
            'memberSince':'{0:02d}/{1:04d}'.format(random.randint(1,13),random.randint(2000,2019))
        })
    return accounts
if __name__ == '__main__':
    myAccounts = gen_account(40)
    for account in myAccounts:
        db.Accounts.insert(account)
