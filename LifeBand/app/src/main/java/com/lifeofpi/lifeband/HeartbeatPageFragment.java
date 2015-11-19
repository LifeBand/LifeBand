package com.lifeofpi.lifeband;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class HeartbeatPageFragment extends Fragment {
    public static final String NAME = "Heartbeat";
    public static final String ARG_PAGE = "ARG_PAGE";

    private int mPage;

    public static HeartbeatPageFragment newInstance(int page) {
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        HeartbeatPageFragment fragment = new HeartbeatPageFragment();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mPage = getArguments().getInt(ARG_PAGE);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_heartbeat_tab, container, false);
        TextView textView = (TextView) view;
        textView.setText("Heartbeat #" + mPage);
        return view;
    }


}