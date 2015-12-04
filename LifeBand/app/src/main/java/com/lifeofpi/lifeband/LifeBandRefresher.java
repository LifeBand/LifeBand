package com.lifeofpi.lifeband;

import android.support.v4.widget.SwipeRefreshLayout;
import android.util.Log;
import android.widget.Toast;

import com.jjoe64.graphview.series.DataPoint;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.Date;
import java.util.Iterator;

/**
 * Created by dominikschmidtlein on 11/30/2015.
 */
public class LifeBandRefresher implements Runnable {

    private MainActivity mainActivity;
    private SwipeRefreshLayout swipeRefreshLayout;
    private UDPHelper udpHelper;


    public LifeBandRefresher(MainActivity mainActivity, SwipeRefreshLayout swipeRefreshLayout, UDPHelper udpHelper){
        this.mainActivity = mainActivity;
        this.swipeRefreshLayout = swipeRefreshLayout;
        this.udpHelper = udpHelper;
    }

    @Override
    public void run() {
        refresh();
    }

    /*The method calls a series of function which request new data, receive the data, check the
    * data, and if it is ok, then the new data is displayed in the ui thread. The method catches
    * errors that were not screened by checkJSONData() and displays a DATA_INVALID message.*/
    private void refresh(){
        requestRefreshData();
        JSONObject jsonData = getRefreshData();
        if(checkJSONData(jsonData))
            unpackJSON(jsonData);
        endRefresh();
    }

    /*The method sends a get latest data request to the server. If the send is unsuccessful
    * because of no internet access, an error message is temporarily displayed on screen. The
    * contents of the message are defined by LifeBand's data transzaZfer protocol*/
    private boolean requestRefreshData(){
        JSONObject latestDataJSON = udpHelper.getLatestDataJSON;
        boolean send = udpHelper.sendUDP(latestDataJSON);
        if(!send)
            mainActivity.displayToast(UDPHelper.SEND_FAILED, Toast.LENGTH_SHORT);
        else
            mainActivity.displayToast("Data Requested", Toast.LENGTH_SHORT);
        return send;
    }

    /*The method calls the receive function and returns the result.
    *   return: the data received from the get latest data request*/
    private JSONObject getRefreshData(){
        return udpHelper.receiveUDP(MainActivity.RECEIVE_PERIOD);
    }

    /*The method checks the JSON data for errors, if an error key exists, the error message is
    * displayed and false is return. If the data is ok, return true*/
    private boolean checkJSONData(JSONObject data){
        String error;
        if((error = getStringFromJSON(data, UDPHelper.ERROR_KEY)) != null) {
            mainActivity.displayToast(error, Toast.LENGTH_SHORT);
            return false;
        }
        return true;
    }

    private void unpackJSON(JSONObject jsonData){
        try {

            JSONObject latest = jsonData.getJSONObject("latest");
            mainActivity.getLifeBandModel().setLatestHeartbeat(latest.getDouble("bpm"));
            mainActivity.getLifeBandModel().setLatestAcceleration(latest.getDouble("forceMag"));

            JSONObject dataDict = jsonData.getJSONObject(UDPHelper.PROTOCOL_DATA_KEY);

            Iterator iterator = dataDict.keys();

            DataPoint[] heartbeats = new DataPoint[dataDict.length()];
            DataPoint[] accelerations = new DataPoint[dataDict.length()];

            for (int index = 0; iterator.hasNext(); index ++) {

                String keyTimeStamp = (String) iterator.next();
                JSONArray bpmForceArray = dataDict.getJSONArray(keyTimeStamp);

                Date date = new Date((long) Double.parseDouble(keyTimeStamp));
                int minutes = date.getMinutes();


//                heartbeats[index] = new DataPoint(Double.parseDouble(Time.keyTimeStamp), bpmForceArray.getDouble(0));
//                accelerations[index] = new DataPoint(Double.parseDouble(keyTimeStamp), bpmForceArray.getDouble(1));

                heartbeats[index] = new DataPoint(minutes, bpmForceArray.getDouble(0));
                accelerations[index] = new DataPoint(minutes, bpmForceArray.getDouble(1));

            }
            Log.d(MainActivity.TAG, heartbeats.length + "");
            mainActivity.getLifeBandModel().setHeartbeats(heartbeats);
            mainActivity.getLifeBandModel().setAccelerations(accelerations);
        } catch (Exception e) {
            e.printStackTrace();
            mainActivity.displayToast(UDPHelper.DATA_INVALID, Toast.LENGTH_SHORT);
        }
    }

    /*The method tries to get from the data with the speficied string key
    *   return: if the get is successful, returns the value otherwise returns null*/
    private String getStringFromJSON(JSONObject data, String key){
        try{
            return data.getString(key);
        }catch (Exception e){
            return null;
        }
    }

    /*The method stops the refresh icon from spinning on the screen. Must be executed by ui thread*/
    private void endRefresh() {
        mainActivity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                swipeRefreshLayout.setRefreshing(false);
            }
        });
    }
}
