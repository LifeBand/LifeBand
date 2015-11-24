package com.lifeofpi.lifeband;

import android.util.Log;
import android.widget.Toast;

import org.json.JSONObject;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;

/**
 * Created by dominikschmidtlein on 11/17/2015.
 */
public class UDPHelper {

    public static final String PROTOCOL_DATA_KEY = "data";
    public static final String PROTOCOL_PULSE_KEY = "pulse";
    public static final String PROTOCOL_RESP_KEY = "resp";
    public static final String PROTOCOL_ACC_KEY = "accell";

    public static final String SEND_FAILED = "Send Failed";
    public static final String RECEIVE_FAILED = "Receive Failed";
    public static final String UPDATE_UNAVAILABLE = "Update Unavailable";
    public static final String DATA_INVALID = "Data Invalid";
    public static final String ERROR_KEY = "error";

    public final JSONObject getLatestDataJSON = new JSONObject();

    public UDPHelper(){
        try {
            getLatestDataJSON.put("id", "phone");
            getLatestDataJSON.put("command", "getLatestData");
        }catch (Exception e){}
    }

    public static boolean sendUDP(JSONObject data, String ip, int port) {
        try {
            InetAddress address = InetAddress.getByName(ip);
            byte[] sendData = data.toString().getBytes();
            DatagramSocket socket = new DatagramSocket();
            DatagramPacket packet = new DatagramPacket(sendData, sendData.length, address, port);
            socket.send(packet);
            socket.close();
            return true;
        }catch (Exception e) {
            return false;
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

            String message = RECEIVE_FAILED;
            if(e instanceof SocketTimeoutException)
                message = UPDATE_UNAVAILABLE;

            JSONObject error = new JSONObject();
            try{error.put(ERROR_KEY, message);}catch (Exception e1){}
            return error;
        }
    }

}
