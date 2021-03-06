package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

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

public class OverviewPageFragment extends PageFragment implements LifeBandListener {

    public static final String NAME = "Overview";

    private TextView currentHeartbeatTextView;
    private TextView currentAccelerationTextView;

    private GraphView heartbeatGraph;
    private GraphView accelerationGraph;

    /*Creates an instance of OverviewPageFragment and can be called statically*/
    public static OverviewPageFragment newInstance(int page) {
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        OverviewPageFragment fragment = new OverviewPageFragment();
        fragment.setArguments(args);
        return fragment;
    }

    /*Method is called when this fragment is created. Method finds all child components and
    * initializes them to private local variables.Method also initializes onRefreshListener which
    * provides support for "pull down to refresh" */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_overview_tab, container, false);

        mainActivity.getLifeBandModel().addView(OverviewPageFragment.this);

        final SwipeRefreshLayout swipeRefreshLayout = (SwipeRefreshLayout) view.findViewById(R.id.swipe_container_overview);
        swipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                UDPHelper udpHelper = new UDPHelper(mainActivity);
                new Thread(new LifeBandRefresher(mainActivity, swipeRefreshLayout, udpHelper)).start();
            }
        });

        currentHeartbeatTextView = (TextView) view.findViewById(R.id.currentHeartbeatTextView);
        currentAccelerationTextView = (TextView) view.findViewById(R.id.currentAccelerationTextView);

        heartbeatGraph = (GraphView) view.findViewById(R.id.heartbeat_graph);
        accelerationGraph = (GraphView) view.findViewById(R.id.acceleration_graph);

        update();

        return view;
    }

    @Override
    public void update() {
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                currentHeartbeatTextView.setText(lifeBand.getLatestHeartbeat() + "");
                currentAccelerationTextView.setText(lifeBand.getLatestAcceleration() + "");

                if(heartbeatGraph != null) {
                    heartbeatGraph.removeAllSeries();
                    heartbeatGraph.addSeries(lifeBand.getHeartbeatSeries());
                }

                if(accelerationGraph != null) {
                    accelerationGraph.removeAllSeries();
                    accelerationGraph.addSeries(lifeBand.getAccelerationSeries());
                }
            }
        });
    }

}