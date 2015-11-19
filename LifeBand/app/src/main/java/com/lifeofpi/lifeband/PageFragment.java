package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.support.v4.app.Fragment;

/**
 * Created by dominikschmidtlein on 11/18/2015.
 */
public abstract class PageFragment extends Fragment {

    public static final String ARG_PAGE = "ARG_PAGE";

    protected int mPage;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mPage = getArguments().getInt(ARG_PAGE);
    }

    public static PageFragment newInstance(int page, PageFragment fragment){
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        fragment.setArguments(args);
        return fragment;
    }

}
