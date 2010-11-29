import struct
import socket

class Message:
	SCROLLSYNC = 1
	NEWOBJ = 2
	OBJSYNC = 3

class Type:
	SHIP = 1
	BULLET = 2
	TURRET = 3

def sendData( conn, data ):
	size = struct.pack( "I", len( data ) )
	conn.sendall( size + data )

def sendIntData( conn, i ):
	sendData( conn, struct.pack( "i", i ) )

def receiveData( conn, noblock=False ):
	try:
		if noblock:
			conn.setblocking( 0 )
		size, = struct.unpack( "I", conn.recv( 4 ) )
	except socket.error:
		return None
	finally:
		if noblock:
			conn.setblocking( 1 )


	return conn.recv( size )

def receiveIntData( conn, noblock=False ):
	data = receiveData( conn, noblock )
	if data != None:
		return struct.unpack( "i", data )
	return None
