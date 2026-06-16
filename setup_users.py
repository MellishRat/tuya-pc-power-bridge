from werkzeug.security import generate_password_hash
import getpass
print("Password hash generator")
while True:
    username = input("Username, or blank to quit: ").strip()
    if not username:
        break
    password = getpass.getpass(f"Password for {username}: ")
    print(f"
{username}:
{generate_password_hash(password)}
")
