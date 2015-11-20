package com.lifeofpi.lifeband;

import java.io.IOException;
import java.io.InterruptedIOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import android.test.suitebuilder.annotation.LargeTest;

import junit.framework.TestCase;

/**
 * Created by dominikschmidtlein on 11/19/2015.
 */
public class UDPHelperTest extends TestCase {

    private class PseudoServer extends Thread {
        DatagramSocket socket;
        DatagramPacket packet;

        byte[] buffer = new byte[1024];

        boolean alive = true;

        public PseudoServer(int port, InetAddress address){
            try{
                packet = new DatagramPacket(buffer, buffer.length);
                socket = new DatagramSocket(port, address);
            }catch (IOException e){
                throw new RuntimeException("PseudoServer creation failed", e);
            }
        }

        @Override
        public void run() {
            try{
                while(alive){
                    try{
                        packet.setLength(buffer.length);
                        socket.receive(packet);
                        String s = new String(packet.getData(), 0, packet.getLength());

                        try{
                            Thread.sleep(100);
                        }catch (InterruptedException ee){

                        }
                        byte[] bytes = s.toUpperCase().getBytes();
                        System.arraycopy(bytes, 0, packet.getData(), 0, bytes.length);
                        packet.setLength(bytes.length);

                        packet.setAddress(InetAddress.getLocalHost());
                        packet.setPort(2345);

                        socket.send(packet);
                    }catch (InterruptedIOException ex){
                    }
                }
            }catch (IOException ioe){
                ioe.printStackTrace();
            }finally {
                socket.close();
            }
        }
    }

    @LargeTest
    public void testSendUDP() throws Exception {
        PseudoServer server = null;
        DatagramSocket socket = null;

        try{
            server = new PseudoServer(1234, InetAddress.getLocalHost());
            server.start();

            byte[] buffer = new byte[1024];


            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            socket = new DatagramSocket(2345, InetAddress.getLocalHost());

            for (int i = 1; i <= 10; i++) {
                String s = "Hello, Android world #" + i + "!";

                byte[] byteess = s.getBytes();
                System.arraycopy(byteess, 0, packet.getData(), 0, byteess.length);
                packet.setLength(byteess.length);

                packet.setAddress(InetAddress.getLocalHost());
                packet.setPort(1234);

                socket.send(packet);

                try {
                    Thread.sleep(100);
                } catch (InterruptedException ex) {
                    // Ignore.
                }

                packet.setLength(buffer.length);
                socket.receive(packet);

                String t = new String(packet.getData(), 0, packet.getLength());

                assertEquals(s.toUpperCase(), t);
            }

        }finally {
            if(server != null)
                server.alive = false;
            if(socket != null)
                socket.close();
        }
    }
}
