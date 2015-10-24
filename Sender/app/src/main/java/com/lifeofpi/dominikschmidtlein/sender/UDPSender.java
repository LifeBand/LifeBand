package com.lifeofpi.dominikschmidtlein.sender;

import android.os.AsyncTask;
import android.util.Log;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

/**
 * Created by dominikschmidtlein on 10/23/2015.
 */


public class UDPSender implements Runnable {
    public static final int PORT = 5005;
    public static final String IP = "134.117.59.71";

    public static final String MESSAGE = "HI";
    public static final String TAG = "THIS";

    @Override
    public void run() {
        try {
            DatagramSocket datagramSocket = new DatagramSocket();
            InetAddress inetAddress = InetAddress.getByName(IP);
            DatagramPacket datagramPacket = new DatagramPacket(MESSAGE.getBytes(), MESSAGE.length(), inetAddress, PORT);
            datagramSocket.send(datagramPacket);
            datagramSocket.close();
            MainActivity.textView.setText("" + Math.random() * 10);
        } catch (Exception e) {
            Log.e(TAG, "exception caught: ", e);
        }
    }

    /*@Override
    public void run() {
        try {
            byte[] receiveData = new byte[8];
            DatagramSocket datagramSocket = new DatagramSocket(PORT);
            DatagramPacket datagramPacket = new DatagramPacket(receiveData, receiveData.length);
            datagramSocket.receive(datagramPacket);
            String dataReceived = new String( datagramPacket.getData(), 0,
                    datagramPacket.getLength() );
        }catch (Exception e){}
    }*/
}
