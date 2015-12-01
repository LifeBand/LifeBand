package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class HeartbeatPageFragment extends PageFragment {
    public static final String NAME = "Heartbeat";

    private GraphView graphView;

    public static HeartbeatPageFragment newInstance(int page) {
        return (HeartbeatPageFragment) PageFragment.newInstance(page, new HeartbeatPageFragment());
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_heartbeat_tab, container, false);

        setupRefresh((SwipeRefreshLayout) view);

        graphView = (GraphView) view.findViewById(R.id.heartbeat_graph);
        graphView.getViewport().setScrollable(true);
        graphView.getViewport().setScalable(true);
        return view;
    }

    @Override
    public void update() {
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                graphView.addSeries(new LineGraphSeries<>(lifeBand.getHeartbeats()));
            }
        });
    }
}
