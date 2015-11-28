package com.lifeofpi.lifeband;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.NotificationCompat;
import android.support.v4.app.TaskStackBuilder;
import android.widget.Toast;

import com.google.android.gms.gcm.GcmListenerService;

/**
 * Created by dominikschmidtlein on 11/27/2015.
 */
public class MyGcmListenerService extends GcmListenerService {

    public static final int MESSAGE_NOTIFICATION_ID = 435345;
    public static final String KEY_MESSAGE = "message";

    @Override
    public void onMessageReceived(String from, Bundle data) {
        String message = data.getString(KEY_MESSAGE);
        createNotification(message);
        Toast.makeText(getApplicationContext(), "message received", Toast.LENGTH_SHORT);
    }

    public void createNotification(String body){
        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(this)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("Abnormalities Detected in Pulse")
                .setContentText(body);

        Intent intent = new Intent(this, MainActivity.class);
        TaskStackBuilder stackBuilder = TaskStackBuilder.create(this);
        stackBuilder.addParentStack(MainActivity.class);
        stackBuilder.addNextIntent(intent);
        PendingIntent pendingIntent = stackBuilder.getPendingIntent(0, PendingIntent.FLAG_UPDATE_CURRENT);
        mBuilder.setContentIntent(pendingIntent);
        NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        notificationManager.notify(MESSAGE_NOTIFICATION_ID, mBuilder.build());
    }
}
