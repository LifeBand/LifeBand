package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import org.json.JSONObject;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class OverviewPageFragment extends PageFragment {
    public static final String NAME = "Overview";

    private SwipeRefreshLayout swipeRefreshLayout;
    private TextView currentHeartbeatTextView;
    private TextView currentRespirationTextView;
    private TextView currentAccelerationTextView;

    public static OverviewPageFragment newInstance(int page) {
        return (OverviewPageFragment) PageFragment.newInstance(page, new OverviewPageFragment());
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
                        JSONObject jSONData = null;
                        if (UDPHelper.sendUDP((MainActivity) getActivity(), getLatestDataJSON, MainActivity.SERVER_IP, MainActivity.PORT))
                            jSONData = UDPHelper.receiveUDP((MainActivity) getActivity(), MainActivity.PORT, MainActivity.RECEIVE_PERIOD);
                        if (jSONData != null) {
                            try {
                                JSONObject data = jSONData.getJSONObject("data");
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

    public void updateOverview(final double pulse, final double resp, final double acc) {
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                currentHeartbeatTextView.setText(Math.round(pulse) + "");
                currentRespirationTextView.setText(Math.round(resp) + "");
                currentAccelerationTextView.setText(Math.round(acc) + "");
            }
        });
    }

    public void endRefresh() {
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                swipeRefreshLayout.setRefreshing(false);
            }
        });
    }
}