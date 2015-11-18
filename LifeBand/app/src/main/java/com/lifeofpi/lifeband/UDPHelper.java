package com.lifeofpi.lifeband;

import android.util.Log;

import org.json.JSONObject;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;

/**
 * Created by dominikschmidtlein on 11/17/2015.
 */
public class UDPHelper {

    public final JSONObject getLatestDataJSON = new JSONObject();

    public UDPHelper(){
        try {
            getLatestDataJSON.put("id", "phone");
            getLatestDataJSON.put("command", "getLatestData");
        }catch (Exception e){}
    }

    public static void sendUDP(JSONObject data, String ip, int port) {
        try {
            InetAddress address = InetAddress.getByName(ip);
            byte[] sendData = data.toString().getBytes();
            DatagramSocket socket = new DatagramSocket();
            DatagramPacket packet = new DatagramPacket(sendData, sendData.length, address, port);
            socket.send(packet);
            socket.close();
        }catch (Exception e) {
            Log.e(MainActivity.TAG, "send failed", e);
            System.exit(0);
        }
    }

    public static JSONObject receiveUDP(int port, int time)  {
        DatagramSocket socket = null;
        try {
            byte[] receiveData = new byte[1024];
            socket = new DatagramSocket(port);
            socket.setSoTimeout(time);
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            socket.receive(receivePacket);
            String data = new String(receivePacket.getData(), 0, receivePacket.getLength());
            JSONObject jsonObject = new JSONObject(data);
            socket.close();
            return jsonObject;
        }catch (Exception e){
            try{socket.close();}catch (Exception ee){}
            if(e instanceof SocketTimeoutException)
                return null;
            Log.e(MainActivity.TAG, "receive failed", e);
            System.exit(0);
            return null;
        }
    }

}
