package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.View;

/**
 * Created by dominikschmidtlein on 11/18/2015.
 */
public abstract class PageFragment extends Fragment implements LifeBandListener{

    public static final String ARG_PAGE = "ARG_PAGE";

    protected LifeBandModel lifeBand;
    protected SwipeRefreshLayout swipeRefreshLayout;

    protected int mPage;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mPage = getArguments().getInt(ARG_PAGE);
        lifeBand = ((MainActivity) getActivity()).getLifeBandModel();
        lifeBand.addView(this);
    }

    public static PageFragment newInstance(int page, PageFragment fragment){
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        fragment.setArguments(args);
        return fragment;
    }

    protected void setupRefresh(final SwipeRefreshLayout swipeRefreshLayout){
        this.swipeRefreshLayout = swipeRefreshLayout;

        swipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                new Thread(new LifeBandRefresher((MainActivity) getActivity(), swipeRefreshLayout)).start();
            }
        });
    }

}
