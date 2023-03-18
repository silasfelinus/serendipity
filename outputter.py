import os

root_dir = os.getcwd() # get the current working directory
app_dir = os.path.join(root_dir, "app")

all_code = ""

# loop over all files in the app directory
for root, dirs, files in os.walk(app_dir):
    for file_name in files:
        file_path = os.path.join(root, file_name)

        # open the file, read its contents and add it to the string
        with open(file_path, "r") as f:
            code = f.read()
            all_code += file_path+'\n'+code+'\n-\n'

# open a text file and write the contents of all_code to it
with open("all_code.txt", "w") as f:
    f.write(all_code)