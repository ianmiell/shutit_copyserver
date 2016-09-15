
Original: https://zwischenzugs.wordpress.com/2015/05/24/convert-any-server-to-a-docker-container/

#Step 1
Install ShutIt as root:
```
sudo su -
pip install shutit
```
The pre-requisites are python-pip, git and docker. The exact names of these in your package manager may vary slightly (eg docker-io or docker.io) depending on your distro.

You may need to make sure the docker server is running too, eg with ‘systemctl start docker’ or ‘service docker start’.

#Step 2
Check out the copyserver script:
```
git clone https://github.com/TheBoroer/shutit_copyserver.git
```

#Step 3
Run the copy_server script:
```
cd shutit_copyserver/bin
./copy_server.sh
```

There is a prompt to ask what docker base image you want to use. Make sure you use one as close to the original server as possible.

#Step 4
Run the built image:
```
docker run -ti [username]/copyserver /bin/bash
```
You are now in a practical facsimile of your server within a docker container!
