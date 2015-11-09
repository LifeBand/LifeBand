package com.lifeofpi.lifeband;


import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.util.logging.Handler;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class OverviewPageFragment extends Fragment {
    public static final String NAME = "Overview";
    public static final String ARG_PAGE = "ARG_PAGE";

    private SwipeRefreshLayout swipeRefreshLayout;
    private TextView currentHeartbeatTextView;
    private TextView currentRespirationTextView;
    private TextView currentAccelerationTextView;

    private int mPage;

    public static OverviewPageFragment newInstance(int page) {
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        OverviewPageFragment fragment = new OverviewPageFragment();
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
        View view = inflater.inflate(R.layout.fragment_overview_tab, container, false);
        swipeRefreshLayout = (SwipeRefreshLayout) view;
        currentHeartbeatTextView = (TextView) view.findViewById(R.id.currentHeartbeatTextView);
        currentRespirationTextView = (TextView) view.findViewById(R.id.currentRespirationTextView);
        currentAccelerationTextView = (TextView) view.findViewById(R.id.currentAccelerationTextView);

        swipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                new GetDataTask().execute();
            }
        });

        return view;
    }

    private class GetDataTask extends AsyncTask<Void, Void, String[]> {

        @Override
        protected String[] doInBackground(Void... params) {

            getActivity().runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    currentHeartbeatTextView.setText(Math.round(Math.random() * 40 + 40) + "");
                    currentRespirationTextView.setText(Math.round(Math.random() * 50 + 30) + "");
                    currentAccelerationTextView.setText(Math.round(Math.random() * 10) + "");
                }
            });

            return null;
        }

        @Override
        protected void onPostExecute(String[] strings) {
            super.onPostExecute(strings);
            swipeRefreshLayout.setRefreshing(false);
        }
    }
}