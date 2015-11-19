package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class RespirationPageFragment extends PageFragment {
    public static final String NAME = "Respiration";

    public static RespirationPageFragment newInstance(int page) {
        return (RespirationPageFragment) PageFragment.newInstance(page, new RespirationPageFragment());
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_respiration_tab, container, false);
        TextView textView = (TextView) view;
        textView.setText(NAME + " #" + mPage);
        return view;
    }


}
