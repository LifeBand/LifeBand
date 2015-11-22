package com.lifeofpi.lifeband;

import android.os.Bundle;
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
        graphView = (GraphView) view.findViewById(R.id.heartbeat_graph);

        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(new DataPoint[] {
                new DataPoint(0, 1),
                new DataPoint(1, 5),
                new DataPoint(2, 3),
                new DataPoint(3, 2),
                new DataPoint(4, 6)});
        graphView.getViewport().setScrollable(true);
        graphView.getViewport().setScalable(true);
        graphView.addSeries(series);
        return view;
    }


}
