package com.lifeofpi.lifeband;


import android.content.Context;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;

/**
 * Created by dominikschmidtlein on 11/4/2015.
 */
public class FragmentPagerAdapterLB extends FragmentPagerAdapter {
    public static final int PAGE_COUNT = 4;
    private String tabTitles[] = new String[] { OverviewPageFragment.NAME, HeartbeatPageFragment.NAME, RespirationPageFragment.NAME, AccelerationPageFragment.NAME };
    private Context context;

    public FragmentPagerAdapterLB(FragmentManager fm, Context context) {
        super(fm);
        this.context = context;
    }

    @Override
    public int getCount() {
        return PAGE_COUNT;
    }

    @Override
    public Fragment getItem(int position) {
        switch (position){
            case 0:
                return OverviewPageFragment.newInstance(position + 1);
            case 1:
                return HeartbeatPageFragment.newInstance(position + 1);
            case 2:
                return RespirationPageFragment.newInstance(position + 1);
            case 3:
                return AccelerationPageFragment.newInstance(position + 1);
            default:
                return OverviewPageFragment.newInstance(position + 1);
        }
    }

    @Override
    public CharSequence getPageTitle(int position) {
        // Generate title based on item position
        return tabTitles[position];
    }
}