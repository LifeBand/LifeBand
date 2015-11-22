package com.lifeofpi.lifeband;

import android.os.Bundle;
import android.preference.PreferenceFragment;
import android.preference.PreferenceManager;

/**
 * Created by dominikschmidtlein on 11/18/2015.
 */
public class SettingsFragment extends PreferenceFragment {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        addPreferencesFromResource(R.xml.settings_preferences);
    }

}
