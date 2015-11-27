package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */

/*Testing “pull down to refresh”
        If not internet_access:
            display message saying “send failed”
        elif successful send and no response:
            after 3 seconds, display message “updates unavailable”
        elif successful send and data is faulty:
            upon data reception, display “data unreadable”
        elif successful send and data is valid:
            update data on screen accordingly
        elif pull down repeatedly:
            should update as normal*/

public class OverviewPageFragment extends PageFragment {

    public static final String NAME = "Overview";

    private SwipeRefreshLayout swipeRefreshLayout;
    private TextView currentHeartbeatTextView;
    private TextView currentRespirationTextView;
    private TextView currentAccelerationTextView;

    /*Creates an instance of OverviewPageFragment and can be called statically*/
    public static OverviewPageFragment newInstance(int page) {
        return (OverviewPageFragment) PageFragment.newInstance(page, new OverviewPageFragment());
    }

    /*Method is called when this fragment is created. Method finds all child components and
    * initializes them to private local variables.Method also initializes onRefreshListener which
    * provides support for "pull down to refresh" */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_overview_tab, container, false);
        swipeRefreshLayout = (SwipeRefreshLayout) view;
        currentHeartbeatTextView = (TextView) view.findViewById(R.id.currentHeartbeatTextView);
        currentRespirationTextView = (TextView) view.findViewById(R.id.currentRespirationTextView);
        currentAccelerationTextView = (TextView) view.findViewById(R.id.currentAccelerationTextView);

        /*Creates the listener for listening to pull down actions from user. The onRefresh() method
        * defines what will happen when user pulls down to refresh.*/
        swipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        refresh();
                    }
                }).start();
            }
        });
        return view;
    }

    /*The method provides a short-hand for retrieving strings from the string resources.
    *   input: the id of the string in question
    *   return: the string with the provided id*/
    private String getStringFromResources(int id){
        return getActivity().getResources().getString(id);
    }

    /*The method provides a short-hand for retreiving shared preferences.
    *   input: key - the key for the desired shared preference
    *   input: value - the default value to be returned if the key does not exist
    *   return: the string value of the shared preference defined by the provided key*/
    private String getSharedPreferences(String key, String value){
        return ((MainActivity) getActivity()).sharedPreferences.getString(key, value);
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

    /*Method updates all fields in the overview tab with the values passed in
    * input: pulse - the next value to be displayed by the pulse textview
    * input: resp - the new respiration value
    * input: acc - the new acceleration value
    * return: NA*/
    private void updateOverview(final double pulse, final double resp, final double acc) {
        /*Any changes to the GUI need to be made on the UI thread. Even though new pulse value
        * is retrieved in another thread, the update of the view must happen in UI thread*/
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                String emptyString = "";
                currentHeartbeatTextView.setText(Math.round(pulse) + emptyString);
                currentRespirationTextView.setText(Math.round(resp) + emptyString);
                currentAccelerationTextView.setText(Math.round(acc) + emptyString);
            }
        });
    }

    /*The method stops the refresh icon from spinning on the screen. Must be executed by ui thread*/
    private void endRefresh() {
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                swipeRefreshLayout.setRefreshing(false);
            }
        });
    }

    /*The method sends a get latest data request to the server. If the send is unsuccessful
    * because of no internet access, an error message is temporarily displayed on screen. The
    * contents of the message are defined by LifeBand's data transfer protocol*/
    private boolean requestRefreshData(){
        JSONObject latestDataJSON = new UDPHelper().getLatestDataJSON;
        boolean send = UDPHelper.sendUDP(latestDataJSON, getIP(), getPort());
        if(!send)
            ((MainActivity) getActivity()).displayToast(UDPHelper.SEND_FAILED, Toast.LENGTH_SHORT);
        return send;
    }

    /*The method calls the receive function and returns the result.
    *   return: the data received from the get latest data request*/
    private JSONObject getRefreshData(){
        return UDPHelper.receiveUDP(getPort(), MainActivity.RECEIVE_PERIOD);
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

    /*The method checks the JSON data for errors, if an error key exists, the error message is
    * displayed and false is return. If the data is ok, return true*/
    private boolean checkJSONData(JSONObject data){
        String error;
        if((error = getStringFromJSON(data, UDPHelper.ERROR_KEY)) != null) {
            ((MainActivity) getActivity()).displayToast(error, Toast.LENGTH_SHORT);
            return false;
        }
        return true;
    }

    /*The method calls a series of function which request new data, receive the data, check the
    * data, and if it is ok, then the new data is displayed in the ui thread. The method catches
    * errors that were not screened by checkJSONData() and displays a DATA_INVALID message.*/
    private void refresh(){
        requestRefreshData();
        JSONObject jsonData = getRefreshData();
        if(checkJSONData(jsonData)){
            try {
                JSONObject data = jsonData.getJSONObject(UDPHelper.PROTOCOL_DATA_KEY);
                final double pulse = data.getDouble(UDPHelper.PROTOCOL_PULSE_KEY);
                final double resp = data.getDouble(UDPHelper.PROTOCOL_RESP_KEY);
                final double acc = data.getDouble(UDPHelper.PROTOCOL_ACC_KEY);
                updateOverview(pulse, resp, acc);
            } catch (Exception e) {
                ((MainActivity) getActivity()).displayToast(UDPHelper.DATA_INVALID, Toast.LENGTH_SHORT);
            }
        }
        endRefresh();
    }
}