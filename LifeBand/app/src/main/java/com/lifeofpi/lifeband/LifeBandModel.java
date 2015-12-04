package com.lifeofpi.lifeband;

import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

/**
 * Created by dominikschmidtlein on 11/30/2015.
 */


public class LifeBandModel {

    public static final int NUMBER_OF_DATA_POINTS = 50;

    private double latestHeartbeat;
    private double latestAcceleration;

    private DataPoint[] heartbeats;
    private DataPoint[] accelerations;

    private LineGraphSeries<DataPoint> heartbeatSeries;
    private LineGraphSeries<DataPoint> accelerationSeries;

    private MainActivity mainActivity;

    private LifeBandListener lifeBandListener;


    public LifeBandModel(MainActivity mainActivity){
        this.mainActivity = mainActivity;
        setHeartbeats(new DataPoint[]{});
        setAccelerations(new DataPoint[]{});
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

    public LineGraphSeries<DataPoint> getAccelerationSeries() {
        return accelerationSeries;
    }

    public LineGraphSeries<DataPoint> getHeartbeatSeries() {
        return heartbeatSeries;
    }

    public void setAccelerationSeries(LineGraphSeries<DataPoint> accelerationSeries) {
        this.accelerationSeries = accelerationSeries;
    }

    public void setHeartbeatSeries(LineGraphSeries<DataPoint> heartbeatSeries) {
        this.heartbeatSeries = heartbeatSeries;
    }

    public void setAccelerations(DataPoint[] accelerations) {
        this.accelerations = accelerations;
        sort(this.accelerations);
        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(this.accelerations);
        series.setColor(mainActivity.getResources().getColor(R.color.ColorPrimary));
        series.setTitle("Max Impact");
        setAccelerationSeries(series);
        updateView();
    }

    public void setHeartbeats(DataPoint[] heartbeats) {
        this.heartbeats = heartbeats;
        sort(this.heartbeats);
        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(this.heartbeats);
        series.setColor(mainActivity.getResources().getColor(R.color.ColorPrimary));
        series.setTitle("Heart Rate");
        setHeartbeatSeries(series);
        updateView();
    }

    private void sort(DataPoint[] series){
        int len = series.length;
        boolean swapped;
        do {
            swapped = false;

            for(int i = 1; i < len; i++){
                if(series[i - 1].getX() > series[i].getX()){
                    DataPoint temp = series[i - 1];
                    series[i - 1] = series[i];
                    series[i] = temp;
                    swapped = true;
                }
            }

        } while (swapped);
    }

    public double getLatestAcceleration() {
        return latestAcceleration;
    }

    public double getLatestHeartbeat() {
        return latestHeartbeat;
    }

    public void setLatestAcceleration(double latestAcceleration) {
        this.latestAcceleration = latestAcceleration;
    }

    public void setLatestHeartbeat(double latestHeartbeat) {
        this.latestHeartbeat = latestHeartbeat;
    }

}
