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
    public static final String IP = "172.17.139.169";
    public static final String MESSAGE = "HI";
    public static final String TAG = "THIS";

   /* protected Object doInBackground(Object[] params) {

        try {
            Log.d("THIS", "");
            Log.d(TAG, "Check0");
            DatagramSocket datagramSocket = new DatagramSocket();
            Log.d(TAG, "Check1" + (datagramSocket == null));
            InetAddress inetAddress = InetAddress.getByName(IP);
            Log.d(TAG,  "Check2");
            DatagramPacket datagramPacket = new DatagramPacket(MESSAGE.getBytes(),MESSAGE.length(), inetAddress, PORT);
            Log.d(TAG, "Check3: " + (datagramPacket == null));
            datagramSocket.send(datagramPacket);
            Log.d(TAG, "Check4");
            Log.d(TAG, datagramPacket.toString());
            Log.d(TAG, "Check5");
            Log.d(TAG, PORT + " " + IP + " " + MESSAGE);
            Log.d(TAG, "Check6");
            datagramSocket.close();
        }
        catch (Exception e){
            Log.e(TAG, "exception caught", e);
            //Log.d(TAG, "exception caught: " + e.getMessage());
        }
        return null;
    }*/


    @Override
    public void run() {

        try {
            Log.d("THIS", "");
            Log.d(TAG, "Check0");
            DatagramSocket datagramSocket = new DatagramSocket();
            Log.d(TAG, "Check1" + (datagramSocket == null));
            InetAddress inetAddress = InetAddress.getByName(IP);
            Log.d(TAG, "Check2");
            DatagramPacket datagramPacket = new DatagramPacket(MESSAGE.getBytes(), MESSAGE.length(), inetAddress, PORT);
            Log.d(TAG, "Check3: " + (datagramPacket == null));
            datagramSocket.send(datagramPacket);
            Log.d(TAG, "Check4");
            Log.d(TAG, datagramPacket.toString());
            Log.d(TAG, "Check5");
            Log.d(TAG, PORT + " " + IP + " " + MESSAGE);
            Log.d(TAG, "Check6");
            datagramSocket.close();
        } catch (Exception e) {
            Log.e(TAG, "exception caught", e);
            //Log.d(TAG, "exception caught: " + e.getMessage());
        }

    }
}
