package com.lifeofpi.lifeband;

import android.app.IntentService;
import android.content.Intent;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.support.v4.content.LocalBroadcastManager;
import android.util.Log;

import com.google.android.gms.gcm.GcmPubSub;
import com.google.android.gms.gcm.GoogleCloudMessaging;
import com.google.android.gms.iid.InstanceID;
import com.google.android.gms.iid.InstanceIDListenerService;

import java.io.IOException;

/**
 * Created by dominikschmidtlein on 11/26/2015.
 */
public class RegistrationIntentService extends IntentService {

    private static final String TAG = "RegIntentService";
    private static final String[] TOPICS = {"global"};

    public RegistrationIntentService(){
        super(TAG);
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        InstanceID instanceID = InstanceID.getInstance(this);
        String senderID = getResources().getString(R.string.gcm_sender_id);
        try {
            String token = instanceID.getToken(senderID, GoogleCloudMessaging.INSTANCE_ID_SCOPE, null);
            Log.d(TAG, "GCM Registration Token: " + token);
            sendRegistrationToServer(token);
            subscribeTopics(token);
            sharedPreferences.edit().putBoolean(MainActivity.SENT_TOKEN_TO_SERVER, true).apply();
        }catch (Exception e){
            Log.d(TAG, "Failed token refresh");
            e.printStackTrace();
            sharedPreferences.edit().putBoolean(MainActivity.SENT_TOKEN_TO_SERVER, false).apply();

        }
        Intent registrationComplete = new Intent(MainActivity.REGISTRATION_COMPLETE);
        LocalBroadcastManager.getInstance(this).sendBroadcast(registrationComplete);
    }
//    https://guides.codepath.com/android/Google-Cloud-Messaging#setup-sender-id
    private void sendRegistrationToServer(String token){

    }

    private void subscribeTopics(String token) throws IOException {
        GcmPubSub pubSub = GcmPubSub.getInstance(this);
        for (String topic : TOPICS) {
            pubSub.subscribe(token, "/topics/" + topic, null);
        }
    }

    public class MyInstanceIDListenerService extends InstanceIDListenerService {

        @Override
        public void onTokenRefresh() {
            Intent intent = new Intent(this, RegistrationIntentService.class);
            startService(intent);
        }
    }
}
