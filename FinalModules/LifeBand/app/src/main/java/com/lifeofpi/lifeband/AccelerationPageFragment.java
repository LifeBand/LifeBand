package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.design.widget.TabLayout;
import android.support.v4.widget.SwipeRefreshLayout;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.jjoe64.graphview.series.PointsGraphSeries;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class AccelerationPageFragment extends PageFragment {

    public static final String NAME = "Acceleration";
    public static final int TAB_INDEX = 2;

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

        graphView = (GraphView) view.findViewById(R.id.acceleration_graph);

        mainActivity.getTabLayout().setOnTabSelectedListener(
                new TabLayout.ViewPagerOnTabSelectedListener(mainActivity.getViewPager()){
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                super.onTabSelected(tab);
                if(tab.getPosition() == TAB_INDEX)
                    updateGraph();
            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {
                super.onTabReselected(tab);
                onTabSelected(tab);
            }
        });

        return view;
    }

    private void updateGraph(){
//        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(lifeBand.getAccelerations());
//        series.setColor(mainActivity.getResources().getColor(R.color.ColorPrimary));
        graphView.removeAllSeries();
        graphView.addSeries(lifeBand.getAccelerationSeries());

    }

}
