#!/usr/bin/env python3

import boto3 

ec2 = boto3.resource('ec2') 
volumes = ec2.volumes.all()

for volume in volumes:
    if volume.state == "available":
        print('Volume ID for deletion - {0}'.format(volume.id))
        volume.delete()
        print("Volume {0}".format(volume.id) + " successfully deleted")
    else:
        print("Volume {0}".format(volume.id) + " - Not for deletion!")
