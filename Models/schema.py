def get_users(User):
   return{
      "id":str(User["_id"]),
      "username":User["username"],
      "email":User["email"],
      "password":User["password"]

   }

def all_users(todos):
   return [get_users(todo) for todo in todos]