package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.LineGraphSeries;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class AccelerationPageFragment extends PageFragment {
    public static final String NAME = "Acceleration";

    private GraphView graphView;

    public static AccelerationPageFragment newInstance(int page) {
        return (AccelerationPageFragment) PageFragment.newInstance(page, new AccelerationPageFragment());
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_acceleration_tab, container, false);
        setupRefresh((SwipeRefreshLayout) view);

        graphView = (GraphView) view.findViewById(R.id.acceleration_graph);
        graphView.getViewport().setScalable(true);
        graphView.getViewport().setScrollable(true);

        return view;
    }

    @Override
    public void update() {
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                graphView.addSeries(new LineGraphSeries<>(lifeBand.getAccelerations()));
            }
        });
    }
}
