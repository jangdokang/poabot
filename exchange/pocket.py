from pocketbase import PocketBase
import jwt
from utility import log_message, log_error_message
import time
import traceback

pb = PocketBase('http://127.0.0.1:8090')

def auth():
  try:
    pb.admins.auth_with_password("poa@admin.com", "poabot!@#$")
  except Exception:
    raise Exception("DB auth error")

def reauth():
  try:
    token = pb.auth_store.base_token
    decoded_token = jwt.decode(token,  options={"verify_signature": False})
    expire_time = decoded_token["exp"]
    current_time = int(time.time())
    if current_time > expire_time:
      auth()
  except:
    raise Exception("DB reauth error")

def create(collection, data):
  try:
    reauth()
    log_message(pb.auth_store.base_token)
    pb.collection(collection).create(data)
  except :
    raise Exception("DB create error")


def delete(collection, id):
  try:
    reauth()
    pb.collection(collection).delete(id)
  except:
    raise Exception("DB delete error")
    

def get_full_list(collection, batch_size = 200,query_params=None):
  try:
    reauth()
    return pb.collection(collection).get_full_list(batch=batch_size, query_params=query_params)
  except:
    raise Exception("DB get_full_list error")

try:
  auth()
except:
  log_error_message(traceback.format_exc(), "DB auth error")
