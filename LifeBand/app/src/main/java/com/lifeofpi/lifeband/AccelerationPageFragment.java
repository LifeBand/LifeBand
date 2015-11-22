package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class AccelerationPageFragment extends PageFragment {
    public static final String NAME = "Acceleration";

    public static AccelerationPageFragment newInstance(int page) {
        return (AccelerationPageFragment) PageFragment.newInstance(page, new AccelerationPageFragment());
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_acceleration_tab, container, false);
        TextView textView = (TextView) view;
        textView.setText(NAME + " #" + mPage);
        return view;
    }


}
