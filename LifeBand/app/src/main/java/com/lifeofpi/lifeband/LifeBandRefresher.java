package com.lifeofpi.lifeband;

import android.support.v4.widget.SwipeRefreshLayout;
import android.util.Log;
import android.widget.Toast;

import com.jjoe64.graphview.series.DataPoint;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.Iterator;

/**
 * Created by dominikschmidtlein on 11/30/2015.
 */
public class LifeBandRefresher implements Runnable {

    private MainActivity mainActivity;
    private SwipeRefreshLayout swipeRefreshLayout;


    public  LifeBandRefresher(MainActivity mainActivity, SwipeRefreshLayout swipeRefreshLayout){
        this.mainActivity = mainActivity;
        this.swipeRefreshLayout = swipeRefreshLayout;
    }

    @Override
    public void run() {
        refresh();
    }

    private void refresh(){
        requestRefreshData();
        JSONObject jsonData = getRefreshData();
        if(checkJSONData(jsonData))
            unpackJSON(jsonData);
        endRefresh();
    }

    /*The method sends a get latest data request to the server. If the send is unsuccessful
    * because of no internet access, an error message is temporarily displayed on screen. The
    * contents of the message are defined by LifeBand's data transfer protocol*/
    private boolean requestRefreshData(){
        JSONObject latestDataJSON = new UDPHelper().getLatestDataJSON;
        boolean send = UDPHelper.sendUDP(latestDataJSON, getIP(), getPort());
        if(!send)
            mainActivity.displayToast(UDPHelper.SEND_FAILED, Toast.LENGTH_SHORT);
        return send;
    }

    /*The method calls the receive function and returns the result.
    *   return: the data received from the get latest data request*/
    private JSONObject getRefreshData(){
        return UDPHelper.receiveUDP(getPort(), MainActivity.RECEIVE_PERIOD);
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
            JSONObject dataDict = jsonData.getJSONObject(UDPHelper.PROTOCOL_DATA_KEY);
            Iterator iterator = dataDict.keys();

            DataPoint[] heartbeats = new DataPoint[UDPHelper.NUMBER_OF_DATA_POINTS];
            DataPoint[] accelerations = new DataPoint[UDPHelper.NUMBER_OF_DATA_POINTS];

            for (int index = 0; iterator.hasNext(); index ++) {

                String keyTimeStamp = (String) iterator.next();
                JSONArray bpmForceArray = dataDict.getJSONArray(keyTimeStamp);

                Log.d(MainActivity.TAG, "key: " + keyTimeStamp + ", value: " + bpmForceArray);

                heartbeats[index] = new DataPoint(Double.parseDouble(keyTimeStamp), bpmForceArray.getDouble(0));
                accelerations[index] = new DataPoint(Double.parseDouble(keyTimeStamp), bpmForceArray.getDouble(1));
            }

            mainActivity.getLifeBandModel().setHeartbeats(heartbeats);
            mainActivity.getLifeBandModel().setAccelerations(accelerations);

        } catch (Exception e) {
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

    /*Method updates all fields in the overview tab with the values passed in
    * input: pulse - the next value to be displayed by the pulse textview
    * input: acc - the new acceleration value
    * return: NA*/
    private void updateOverview(final double pulse, final double acc) {
        /*Any changes to the GUI need to be made on the UI thread. Even though new pulse value
        * is retrieved in another thread, the update of the view must happen in UI thread*/
        mainActivity.runOnUiThread(new Runnable() {
            @Override
            public void run() {

            }
        });
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

    /*The method returns the port from shared preferences with the key "port_key"
     *  return: port */
    private int getPort(){
        String key = getStringFromResources(R.string.port_key);
        String def = getStringFromResources(R.string.port_default);
        return Integer.valueOf(getSharedPreferences(key, def));
    }

    /*The method returns the IP as a string from the shared preferences
    *   return: IP*/
    private String getIP(){
        String key = getStringFromResources(R.string.ip_key);
        String def = getStringFromResources(R.string.ip_default);
        return getSharedPreferences(key, def);
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
