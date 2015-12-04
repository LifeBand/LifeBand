package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.View;

/**
 * Created by dominikschmidtlein on 11/18/2015.
 */
public abstract class PageFragment extends Fragment {

    public static final String ARG_PAGE = "ARG_PAGE";

    protected MainActivity mainActivity;
    protected LifeBandModel lifeBand;

    protected int mPage;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mPage = getArguments().getInt(ARG_PAGE);

        mainActivity = (MainActivity) getActivity();
    }

}
