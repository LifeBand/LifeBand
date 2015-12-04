package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
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
public class AccelerationPageFragment extends PageFragment {
    public static final String NAME = "Acceleration";

    private GraphView graphView;

    public static AccelerationPageFragment newInstance(int page) {
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        AccelerationPageFragment fragment = new AccelerationPageFragment();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_acceleration_tab, container, false);

//        graphView = (GraphView) view.findViewById(R.id.acceleration_graph);
//        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(new DataPoint[]{
//                new DataPoint(5,7),
//                new DataPoint(3,8),
//                new DataPoint(1,6)
//        });
//        graphView.addSeries(series);

        return view;
    }

}
