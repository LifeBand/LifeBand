package com.lifeofpi.lifeband;


import android.support.design.widget.TabLayout;
import android.os.Bundle;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONObject;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;


public class MainActivity extends AppCompatActivity {

    public TextView pulseTextView;
    public TextView respTextView;
    public TextView accTextView;

    public int PORT = 5005;
    public String IP = "172.17.148.20";
    public byte[] sendData;
    InetAddress address;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Get the ViewPager and set it's PagerAdapter so that it can display items
        ViewPager viewPager = (ViewPager) findViewById(R.id.viewpager);
        viewPager.setAdapter(new FragmentPagerAdapterLB(getSupportFragmentManager(),
                MainActivity.this));

        // Give the TabLayout the ViewPager
        TabLayout tabLayout = (TabLayout) findViewById(R.id.sliding_tabs);
        tabLayout.setupWithViewPager(viewPager);
        pulseTextView = (TextView) findViewById(R.id.currentHeartbeatTextView);
        respTextView = (TextView) findViewById(R.id.currentRespirationTextView);
        accTextView = (TextView) findViewById(R.id.currentAccelerationTextView);


        try {
            address = InetAddress.getByName(IP);
            JSONObject jObj = new JSONObject();
            jObj.put("id", "phone");
            jObj.put("command", "getLatestData");
            sendData = jObj.toString().getBytes();
        }catch (Exception e){}

        Button refreshButton = (Button) findViewById(R.id.request_refresh_button);
        refreshButton.setOnClickListener(v -> new Thread(() -> {
            try {
                DatagramSocket socket = new DatagramSocket();
                DatagramPacket packet = new DatagramPacket(sendData, sendData.length, address, PORT);
                socket.send(packet);
                socket.close();
            } catch (Exception e) {
                Log.e("Dom", "exception caught: ", e);
            }
        }).start());

        /*final EditText portEditText = (EditText) findViewById(R.id.port_editText);
        portEditText.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if(!hasFocus)
                    PORT = Integer.valueOf(portEditText.getText().toString());
            }
        });

        final EditText ipEditText = (EditText) findViewById(R.id.ip_editText);
        ipEditText.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View v, boolean hasFocus) {
                if(!hasFocus)
                    IP = ipEditText.getText().toString();
            }
        });*/

        new Thread(() -> {
            try {
                while(true) {
                    byte[] receiveData = new byte[1024];
                    DatagramSocket socket = new DatagramSocket(PORT);
                    DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                    socket.receive(receivePacket);
                    String data = new String(receivePacket.getData(), 0, receivePacket.getLength());
                    JSONObject jsonObject = new JSONObject(data);
                    JSONObject jsonData = (JSONObject) jsonObject.get("data");
                    final double pulse = jsonData.getDouble("pulse");
                    final double resp = jsonData.getDouble("resp");
                    final double accell = jsonData.getDouble("accell");

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            pulseTextView.setText(pulse + "");
                            respTextView.setText(resp + "");
                            accTextView.setText(accell + "");
                        }
                    });
                }
            }catch (Exception e){
                Log.e("Dom", "packet reception failed: ", e);
            }
        }).start();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
