package com.lifeofpi.lifeband;


import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.widget.SwipeRefreshLayout;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import org.json.JSONObject;
import org.w3c.dom.Text;

import java.util.logging.Handler;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class OverviewPageFragment extends Fragment {
    public static final String NAME = "Overview";
    public static final String ARG_PAGE = "ARG_PAGE";

    private SwipeRefreshLayout swipeRefreshLayout;
    private TextView currentHeartbeatTextView;
    private TextView currentRespirationTextView;
    private TextView currentAccelerationTextView;

    private int mPage;

    public static OverviewPageFragment newInstance(int page) {
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        OverviewPageFragment fragment = new OverviewPageFragment();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mPage = getArguments().getInt(ARG_PAGE);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_overview_tab, container, false);
        swipeRefreshLayout = (SwipeRefreshLayout) view;
        currentHeartbeatTextView = (TextView) view.findViewById(R.id.currentHeartbeatTextView);
        currentRespirationTextView = (TextView) view.findViewById(R.id.currentRespirationTextView);
        currentAccelerationTextView = (TextView) view.findViewById(R.id.currentAccelerationTextView);

        swipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        JSONObject getLatestDataJSON = new UDPHelper().getLatestDataJSON;
                        UDPHelper.sendUDP(getLatestDataJSON, MainActivity.SERVER_IP, MainActivity.PORT);
                        JSONObject data = UDPHelper.receiveUDP(MainActivity.PORT, MainActivity.RECEIVE_PERIOD);
                        if(data != null) {
                            try {
                                final double pulse = data.getDouble("pulse");
                                final double resp = data.getDouble("resp");
                                final double acc = data.getDouble("accell");
                                updateOverview(pulse, resp, acc);
                            } catch (Exception e) {
                                Log.e(MainActivity.TAG, "data extraction failed", e);
                            }
                        }
                        endRefresh();
                    }
                }).start();
            }
        });

        return view;
    }

    public void updateOverview(final double pulse, final double resp, final double acc){
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                currentHeartbeatTextView.setText(Math.round(pulse) + "");
                currentRespirationTextView.setText(Math.round(resp) + "");
                currentAccelerationTextView.setText(Math.round(acc) + "");
            }
        });
    }

    public void endRefresh(){
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                swipeRefreshLayout.setRefreshing(false);
            }
        });
    }

    /*private class GetDataTask extends AsyncTask<Void, Void, String[]> {

        @Override
        protected String[] doInBackground(Void... params) {

            getActivity().runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    updateOverview((int) Math.round(Math.random() * 40 + 40), (int) Math.round(Math.random() * 50 + 30), (int) Math.round(Math.random() * 10));
                }
            });

            return null;
        }

        @Override
        protected void onPostExecute(String[] strings) {
            super.onPostExecute(strings);
            swipeRefreshLayout.setRefreshing(false);
        }
    }*/
}