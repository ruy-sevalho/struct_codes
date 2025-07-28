user_profile = {"username": "john_doe", "status": "active", "last_login": "2025-07-22"}

name = "username"

match user_profile:
    case {key: username, "status": "active"} if key == name and "last_login" in user_profile:
        print(f"Active user {username} logged in recently.")
    case _:
        print("User profile not recognized.")