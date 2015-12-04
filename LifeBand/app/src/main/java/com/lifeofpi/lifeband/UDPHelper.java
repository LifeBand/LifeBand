package com.lifeofpi.lifeband;

import android.content.SharedPreferences;
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

    public static final String PROTOCOL_DATA_KEY = "data";

    public static final String SEND_FAILED = "Send Failed";
    public static final String RECEIVE_FAILED = "Receive Failed";
    public static final String UPDATE_UNAVAILABLE = "Update Unavailable";
    public static final String DATA_INVALID = "Data Invalid";
    public static final String DATA_EMPTY = "Data Empty";
    public static final String ERROR_KEY = "error";


    public final JSONObject getLatestDataJSON = new JSONObject();

    private MainActivity mainActivity;

    public UDPHelper(MainActivity mainActivity) {
        this.mainActivity = mainActivity;

        try {
            getLatestDataJSON.put("id", "phone");
            getLatestDataJSON.put("command", "getPastDataSet");
            getLatestDataJSON.put(PROTOCOL_DATA_KEY,"{\"numPoints\":\"" + LifeBandModel.NUMBER_OF_DATA_POINTS + "\"}");
        }catch (Exception e){}
    }

    public boolean sendUDP(JSONObject data) {
        try {
            InetAddress address = InetAddress.getByName(getIP());
            byte[] sendData = data.toString().getBytes();
            DatagramSocket socket = new DatagramSocket();
            DatagramPacket packet = new DatagramPacket(sendData, sendData.length, address, getSendPort());
            socket.send(packet);
            socket.close();
            return true;
        }catch (Exception e) {
            return false;
        }
    }

    public JSONObject receiveUDP(int time)  {
        DatagramSocket socket = null;
        try {
            byte[] receiveData = new byte[4096];
            socket = new DatagramSocket(getReceivePort());
            socket.setSoTimeout(time);
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            socket.receive(receivePacket);
            String data = new String(receivePacket.getData(), 0, receivePacket.getLength());
            Log.d(MainActivity.TAG, data);
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

    /*The method returns the port from shared preferences with the key "port_key"
     *  return: port */
    private int getSendPort(){
        String key = getStringFromResources(R.string.send_port_key);
        String def = getStringFromResources(R.string.send_port_default);
        return Integer.valueOf(getSharedPreferences(key, def));
    }

    /*The method returns the port from shared preferences with the key "port_key"
     *  return: port */
    private int getReceivePort(){
        String key = getStringFromResources(R.string.receive_port_key);
        String def = getStringFromResources(R.string.receive_port_default);
        return Integer.valueOf(getSharedPreferences(key, def));
    }


    /*The method returns the IP as a string from the shared preferences
    *   return: IP*/
    private String getIP(){
        String key = getStringFromResources(R.string.ip_key);
        String def = getStringFromResources(R.string.ip_default);
        return getSharedPreferences(key, def);
    }

    /*The method provides a short-hand for retrieving strings from the string resources.
    *   input: the id of the string in question
    *   return: the string with the provided id*/
    private String getStringFromResources(int id){
        return mainActivity.getResources().getString(id);
    }

    /*The method provides a short-hand for retreiving shared preferences.
    *   input: key - the key for the desired shared preference
    *   input: value - the default value to be returned if the key does not exist
    *   return: the string value of the shared preference defined by the provided key*/
    private String getSharedPreferences(String key, String value){
        return mainActivity.sharedPreferences.getString(key, value);
    }
}
