package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import com.jjoe64.graphview.series.DataPoint;

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

    private TextView currentHeartbeatTextView;
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

        setupRefresh((SwipeRefreshLayout) view);

        currentHeartbeatTextView = (TextView) view.findViewById(R.id.currentHeartbeatTextView);
        currentAccelerationTextView = (TextView) view.findViewById(R.id.currentAccelerationTextView);
        return view;
    }

    @Override
    public void updateView() {
        DataPoint[] heartbeats = lifeBand.getHeartbeats();
        DataPoint[] accelerations = lifeBand.getAccelerations();
        currentHeartbeatTextView.setText(heartbeats[heartbeats.length - 1].getY() + "");
        currentAccelerationTextView.setText(accelerations[accelerations.length - 1].getY() + "");
    }
}