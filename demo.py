import os
for i in os.listdir():
    with open(i, "r") as file:
        things = file.read().replace("sys.exit(int(ConfigLanguareRunner.programEnv[9][1]))", "sys.exit(int(ConfigLanguareRunner.programEnv[9][1]))")
    with open(i, "w") as file:
        file.write(things)