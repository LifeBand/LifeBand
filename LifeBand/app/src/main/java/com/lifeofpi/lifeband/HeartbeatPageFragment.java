package com.lifeofpi.lifeband;

import android.graphics.Paint;
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
public class HeartbeatPageFragment extends PageFragment {

    public static final String NAME = "Heartbeat";
    public static final int TAB_INDEX = 1;

    private GraphView graphView;


    public static HeartbeatPageFragment newInstance(int page) {
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        HeartbeatPageFragment fragment = new HeartbeatPageFragment();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_heartbeat_tab, container, false);

        graphView = (GraphView) view.findViewById(R.id.heartbeat_graph);

        mainActivity.getTabLayout().setOnTabSelectedListener(
                new TabLayout.ViewPagerOnTabSelectedListener(mainActivity.getViewPager()){
                    @Override
                    public void onTabSelected(TabLayout.Tab tab) {
                        super.onTabSelected(tab);
                        if(tab.getPosition() == TAB_INDEX)
                            updateGraph();
                        Log.d(MainActivity.TAG, "tab changed to: " + tab.getPosition());
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
//        Log.d(MainActivity.TAG, "hearbeats length: " + lifeBand.getHeartbeats().length + "");
//        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(lifeBand.getHeartbeats());
//        series.setColor(mainActivity.getResources().getColor(R.color.ColorPrimary));
        graphView.removeAllSeries();
        graphView.addSeries(lifeBand.getHeartbeatSeries());

    }

}
