package javadevice;

import java.io.StringWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Scanner;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class JavaDevice {
    
    public static InetAddress MY_IP;
    public static InetAddress OTHER_IP;
    public static final int UDP_PORT = 5005;
    
    public static void main(String[] args) throws Exception {
        MY_IP = InetAddress.getByName("134.117.59.69");
        OTHER_IP = InetAddress.getByName("134.117.59.70");
        
        //scanner for user input
        Scanner scanner = new Scanner(System.in);
        //parser for parsing to json from string
        JSONParser parser = new JSONParser();
        //an object which holds json as a string
        StringWriter stringWriter = new StringWriter();
        //json object
        JSONObject jObj = new JSONObject();
        //socket for UDP
        DatagramSocket socket = new DatagramSocket(UDP_PORT);
        
        //put key value pair in jsonobject
        jObj.put("javakey", "javavalue");
        //create string from json object
        jObj.writeJSONString(stringWriter);
        
        
        while(true){
            System.out.println("Give command s or r: ");
            String in = scanner.nextLine();
            //sending
            if(in.equals("r")){
                byte[] receiveData = new byte[1024];
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                socket.receive(receivePacket);
                //extract data from packet
                String data = new String(receivePacket.getData(),0, receivePacket.getLength());
                //parse string for json object
                JSONObject jsonData = (JSONObject) parser.parse(data);
                System.out.println(jsonData);
            }
            //receiving
            else if(in.equals("s")){
                byte[] sendData = new byte[1024];
                //write data to be sent
                sendData = stringWriter.toString().getBytes();
                //create datagram
                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, OTHER_IP, UDP_PORT);
                socket.send(sendPacket);
                System.out.println(stringWriter);
            }
            
        }
        
        
        
    }
    
}
