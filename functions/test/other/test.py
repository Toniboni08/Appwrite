from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.id import ID

client = (Client()
              .set_project("67bccc79000a57dd1cff")
              .set_key("standard_ff7ea6d93718221f676d06876346da516ce120648edc18c1c5f0c0e9f1f48010a5b80d60e092745c6197d25ac483cc18b8a6f4e2ed9e0d82c51bd25e5057d8f7df26d65e223c35407a5e4afb5078db31b01dd12e2b239b37d7d0f7cdd56190609332b1adefa266a9fa3adc6f6f18762d82683da37e348dc81e68ce28d1eeaa32"))

users = Users(client)

print(users.list())