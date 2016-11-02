/*
 * Credits:
 * http://www.denisigo.com/2014/08/example-of-bluetooth-communication-between-android-and-linux/
*/

package matthewkleinsmith.jetsonremotecontrol;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.IOException;
import java.lang.*;

public class StartServiceActivity extends AppCompatActivity {

    private EditText mInputView;
    private Button mStartButton;
    private Button mStopButton;
    private Button mGetDataButton;
    private Button mUseModelButton;

    //private BluetoothServer mBluetoothServer;
    /**
     * Bluetooth server events listener.
     */
    private BluetoothServer.IBluetoothServerListener mBluetoothServerListener =
            new BluetoothServer.IBluetoothServerListener() {
                @Override
                public void onStarted() {
                    writeMessage("*** Server has started, waiting for client connection ***");
                    mStartButton.setEnabled(false);
                    mStopButton.setEnabled(true);
                }

                @Override
                public void onConnected() {
                    writeMessage("*** Client has connected ***");
                    mGetDataButton.setEnabled(true);
                    mUseModelButton.setEnabled(true);
                }

                @Override
                public void onData(byte[] data) {
                    writeMessage(new String(data));
                }

                @Override
                public void onError(String message) {
                    writeError(message);
                }

                @Override
                public void onStopped() {
                    writeMessage("*** Server has stopped ***");
                    mStartButton.setEnabled(true);
                    mStopButton.setEnabled(false);
                    mGetDataButton.setEnabled(false);
                    mUseModelButton.setEnabled(false);
                }
            };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_start_service);

        mInputView = (EditText) findViewById(R.id.input);
        mStartButton = (Button) findViewById(R.id.startServiceButton);
        mStopButton = (Button) findViewById(R.id.stopServiceButton);
        mGetDataButton = (Button) findViewById(R.id.getDataButton);
        mUseModelButton = (Button) findViewById(R.id.useModelButton);

        ((cBaseApplication)this.getApplicationContext()).theBluetoothServer = new BluetoothServer();
        ((cBaseApplication)this.getApplicationContext()).theBluetoothServer.setListener(mBluetoothServerListener);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        ((cBaseApplication)this.getApplicationContext()).theBluetoothServer.stop();
        //((cBaseApplication)this.getApplicationContext()).theBluetoothServer = null;
    }

    public void onStartClick(View view) {
        try {
            ((cBaseApplication)this.getApplicationContext()).theBluetoothServer.start();
        } catch (BluetoothServer.BluetoothServerException e) {
            e.printStackTrace();
            writeError(e.getMessage());
        }
    }

    public void onStopClick(View view) {
        ((cBaseApplication)this.getApplicationContext()).theBluetoothServer.stop();
    }

    public void onGetDataClick(View view) {
        Intent intent = new Intent(this, GetDataActivity.class);
        startActivity(intent);
    }

    public void onUseModelClick(View view) {
        Intent intent = new Intent(this, UseModelActivity.class);
        startActivity(intent);
    }

    private void writeMessage(String message) {
        mInputView.setText(message + "\r\n" + mInputView.getText().toString());
    }

    private void writeError(String message) {
        writeMessage("ERROR: " + message);
    }
}
