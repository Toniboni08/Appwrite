from appwrite.client import Client
from appwrite.query import Query
from appwrite.services.databases import Databases

client = (Client()
              .set_project("67bccc79000a57dd1cff")
              .set_key("standard_ff7ea6d93718221f676d06876346da516ce120648edc18c1c5f0c0e9f1f48010a5b80d60e092745c6197d25ac483cc18b8a6f4e2ed9e0d82c51bd25e5057d8f7df26d65e223c35407a5e4afb5078db31b01dd12e2b239b37d7d0f7cdd56190609332b1adefa266a9fa3adc6f6f18762d82683da37e348dc81e68ce28d1eeaa32"))

databases = Databases(client)

print(databases.list_documents("67bdd976002814a9f0bf",
                    "67bddec4001367f18b1b",
                    [Query.equal("uuid", "d4bf2b5a30b94dd297ced52e4eecf245"), Query.equal("serverId", "01d13d06ffcc0d332234980f551b5b023bb8f8a1"), Query.limit(1)]
                )["documents"][0])