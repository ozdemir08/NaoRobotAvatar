from naoqi import ALProxy
from bluetooth import *
import rospy, roslib

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805F9B34FB"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

i = 0


class StoreClass(object):
    last_data_as_json = '{bos bos}'
    number = 0
    firstTime = True
    yaw_start = 0
    pitch_start = 0

    @staticmethod
    def init(a,b):
        print "Init init init"
        rospy.init_node('bizim_listener_node')
        StoreClass.motionProxy = ALProxy("ALMotion", "192.168.1.113", 9559)
        #StoreClass.motionProxy = ALProxy("ALMotion", "127.0.0.1", 44099)
        StoreClass.motionProxy.setStiffnesses("Body", 1.0)
        StoreClass.fractionMaxSpeed = 0.15
        StoreClass.motionProxy.setMoveArmsEnabled(False, False)
        StoreClass.yaw_start = a
        StoreClass.pitch_start = b



names = ['HeadYaw', 'HeadPitch']
try:
    while True:
    	client_sock, client_info = server_sock.accept()
    	print i
    	i += 1
        data = client_sock.recv(4096)
        print i
        print("received [%s]" % data)
        
        yaw, pitch = data.split(',')
        print('data:',data)
	print('angles: ',yaw, pitch)
        if StoreClass.firstTime == True:
            print "init baslangic"
            StoreClass.init(float(yaw), float(pitch))
            StoreClass.firstTime = False
            angles = [0, 0]
            StoreClass.motionProxy.setAngles(names, angles, StoreClass.fractionMaxSpeed)
            print "init bitis"

        angles = [-float(yaw) + StoreClass.yaw_start, -float(pitch) + StoreClass.pitch_start]
        print('angles: ', angles)
	if angles[0] > 3.14:
		angles[0] = angles[0] - 3.14*2
	if angles[0] < -3.14:
		angles[0] = angles[0] + 3.14*2
        if angles[0] >-1.5 and angles[0] < 1.5:
        	StoreClass.motionProxy.setAngles(names, angles, StoreClass.fractionMaxSpeed)


except IOError:
	print "IO Error"
	pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
