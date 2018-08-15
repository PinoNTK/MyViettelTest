import random
import uuid

def address():
    return '{0:010d}'.format(random.randint(100,10000))
def birthday():
    return '{0}/{1}/{2}'.format(random.randint(1,29),random.randint(1,13),random.randint(1800,2002))
def mail():
    return '{0}@{1}'.format(random.choice(['haah','asdas','asdasdadas']),random.choice(['gmail.com','outlook.com','viettel.com.vn']))
def name_rand():
    ho=['Phạm','Nguyễn']
    ten_dem = ['Văn','Thị','Ngọc']
    ten=['Linh','Kiên','Sơn','Nhi','Hoa','Duyên']
    return '{0} {1} {2}'.format(random.choice(ho),random.choice(ten_dem),random.choice(ten))
def username(name):
    return '{0}{1}'.format(name.lower().replace(' ',''),random.randint(1,9999))
def gen_account(n):
    accounts = []
    for i in range(n):
        name = name_rand()
        accounts.append({
            'accountBalance':random.randint(50000,1e9),
            'accountNumber':'{0:011d}'.format(random.randint(1900000000,19900000000)),
            'address':address(),
            'birthday':birthday(),
            'cardNumber':'{0:09d}'.format(random.randint(10000000,999000000)),
            'idNumber':'{0:09d}'.format(random.randint(17400000,179999999)),
            'mail':mail(),
            'name':name,
            'password':uuid.uuid4(),
            'phoneNumber':'{0:011d}'.format(random.randint(1660000000,1689999999)),
            'role':random.choice(['normal','admin']),
            'username':username(name),
            'gender':random.choice(['male','female']),
            'memberSince':'{0:02d}/{1:04d}'.format(random.randint(1,13),random.randint(2000,2019))
        })
    return accounts
if __name__ == '__main__':
    print(gen_account(5))
    # print(audio.shape)