import os

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("{} has been created".format(dir_name))
    else:
        print("{} already exists".format(dir_name))

if __name__=="__main__":
    create_directory("data source")
    create_directory("data staging")
    create_directory("data destination")