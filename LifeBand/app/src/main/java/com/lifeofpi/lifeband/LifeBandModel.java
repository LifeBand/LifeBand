package com.lifeofpi.lifeband;

import com.jjoe64.graphview.series.DataPoint;

/**
 * Created by dominikschmidtlein on 11/30/2015.
 */
public class LifeBandModel {

    private DataPoint[] heartbeats;
    private DataPoint[] accelerations;

    private LifeBandListener view;

    public LifeBandModel(){

    }

    public void addView(LifeBandListener view){
        this.view = view;
    }

    public void updateView(){
        view.update();
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
