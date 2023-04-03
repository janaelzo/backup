import subprocess
################################
#DO NOT TOUCH
################################


#path to script
# ./bin/run_device.expect

path_to_expect = "bin/run_device.expect"


def call_script(router,user,pswd):
    selected = router_selector(router)
    #subprocess.call(path_to_expect,shell=True)
    f = open("stdout.txt", "w")
    try:
        subprocess.check_call("expect run_device.expect -h %s -t 7750 -u %s -p %s -c cmd.txt " %(router,user,pswd), stdout=f,shell=True)
        #subprocess.check_call("expect run_device.expect -h %s -t 7750 -u %s -p %s -c cmd.txt " % (router,user,pswd), stdout=f)

    except:
        print("FAILED CONNECTION")
# make lowercase for dns 
def router_selector(router):
    lower = router.lower()

    return lower

def search_txt(type):
    lines = []
    info = []
    if type == 'port':
        with open('stdout.txt') as read:
            lines = read.readlines()
        substring = "Installed MDAs"
        cnt = 0
        for line in lines:
            cnt += 1
            if substring in line:
                info = info.append(line)
    
    return print(info)

