package com.lifeofpi.lifeband;

import com.jjoe64.graphview.series.DataPoint;

/**
 * Created by dominikschmidtlein on 11/30/2015.
 */


public class LifeBandModel {

    public static final int NUMBER_OF_DATA_POINTS = 50;

    private DataPoint[] heartbeats;
    private DataPoint[] accelerations;

    private MainActivity mainActivity;

    private LifeBandListener lifeBandListener;


    public LifeBandModel(MainActivity mainActivity){
        this.mainActivity = mainActivity;
        heartbeats = new DataPoint[]{};
        accelerations = new DataPoint[]{};
    }

    public void addView(LifeBandListener lifeBandListener){
        this.lifeBandListener = lifeBandListener;
    }

    private void updateView(){
        if(lifeBandListener != null)
            lifeBandListener.update();
    }


    public DataPoint[] getAccelerations() {
        return accelerations;
    }

    public DataPoint[] getHeartbeats() {
        return heartbeats;
    }

    public void setAccelerations(DataPoint[] accelerations) {
        this.accelerations = accelerations;
        updateView();
    }

    public void setHeartbeats(DataPoint[] heartbeats) {
        this.heartbeats = heartbeats;
        updateView();
    }

}
