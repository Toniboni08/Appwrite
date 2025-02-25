import hashlib
import json
import uuid
from json import JSONDecodeError

import requests
from appwrite.client import Client
from appwrite.query import Query
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.services.users import Users


def throwError(context, errorType, message):
    context.error("Error %s occurred" % type)
    return context.res.json(
        {
            "success": False,
            "errorType": errorType,
            "message": message
        }
    )

def keyError(context, errorObject):
    return throwError(context, "KeyError", 'Field "%s" could not be found in the request' % errorObject.args[0])

def jsonError(context, errorObject):
    return throwError(context, "JsonDecodeError", errorObject.msg)

def main(context):
    client = (Client()
              .set_project("67bccc79000a57dd1cff")
              .set_key("standard_ff7ea6d93718221f676d06876346da516ce120648edc18c1c5f0c0e9f1f48010a5b80d60e092745c6197d25ac483cc18b8a6f4e2ed9e0d82c51bd25e5057d8f7df26d65e223c35407a5e4afb5078db31b01dd12e2b239b37d7d0f7cdd56190609332b1adefa266a9fa3adc6f6f18762d82683da37e348dc81e68ce28d1eeaa32"))

    databases = Databases(client)

    users = Users(client)

    if context.req.method == "GET":
        if context.req.path == "/get_challenge":
            try:
                request = context.req.body_json
                playerUUID = request["uuid"]

            except JSONDecodeError as error:
                return jsonError(context, error)
            except KeyError as error:
                return keyError(context, error)

            context.log(f"Creating a challenge server ID for {playerUUID}")

            serverId = hashlib.sha1(uuid.uuid4().bytes).hexdigest()

            databases.create_document("67bdd976002814a9f0bf",
                "67bddec4001367f18b1b",
                ID.unique(),
                {
                    "uuid": playerUUID,
                    "serverId": serverId
                }
            )


            return context.res.json(
                {
                    "serverId": serverId
                }
            )
        if context.req.path == "/authenticate":
            try:
                request = context.req.body_json
                playerUUID = request["uuid"]
                serverId = request["serverId"]

                try:
                    playerName = requests.get(f"https://api.minecraftservices.com/minecraft/profile/lookup/{playerUUID}").json()["id"]
                except KeyError:
                    return throwError(context, "UUIDNotFoundError", "the uuid %s could not be found in minecraft" % playerUUID)

                documents = databases.list_documents("67bdd976002814a9f0bf",
                    "67bddec4001367f18b1b",
                    [Query.equal("uuid", playerUUID), Query.equal("serverId", serverId), Query.limit(1)]
                )

                if documents["total"] == 0:
                    return throwError(context, "NoChallengeFound", f"The challenge with the serverId {serverId} and the uuid {playerUUID} could not be found!")

                databases.delete_document("67bdd976002814a9f0bf", "67bddec4001367f18b1b", documents["documents"][0]["id"])

                response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/hasJoined?username={playerName}&serverId={serverId}")
                if response.status_code == 200:
                    userQuery = users.list(Query.equal("name", playerUUID))

                    if userQuery["total"] == 0:
                        user = users.create(ID.unique(), name=playerUUID)
                    else:
                        user = userQuery["users"][0]


                    return context.res.json(
                        {
                            "success": True,
                            "token": users.create_token(user, 16),
                            "clientId": user["id"]
                        }
                    )

                context.log("Mojang reported with code %s" % response.status_code)

                return throwError(context, "NotAuthenticatedError", "The client did not authenticate with mojangs servers!")


            except JSONDecodeError as error:
                return jsonError(context, error)
            except KeyError as error:
                return keyError(context, error)

    return context.res.empty()